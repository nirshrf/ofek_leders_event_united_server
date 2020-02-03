import requests
from Entities import Adopter, Quadcopter, GridCell, Event, AdoptionStatus, Adoptee, Plot, PetType
from graphql_handler import get_entity_as_json
from generations.generatePlot import generate_random_plot


class GraphQLRequests:
    def __init__(self, url):
        self.url = url

    def import_adopters(self):
        request_data = requests.post(self.url, json={"query": '{adopters'+get_entity_as_json("Adopter")+'}'}).json()
        return self.parse_adopters_from_json(request_data)

    def parse_adopters_from_json(self, query_response):
        if self.validate_more_than_one_adopter(query_response):
            return [Adopter(list(adopter.values())) for adopter in query_response['data']['adopters']]
        return [Adopter(list(query_response['data']['adopters'][0].values()))]

    def validate_more_than_one_adopter(self, adopters_dictionary):
        return len(adopters_dictionary['data']['adopters']) > 1

    def import_quads(self):
        request_data = requests.post(self.url, json={"query": '{allQuadcopters'+get_entity_as_json("Quadcopter")+'}'}).json()
        return self.parse_quads_from_json(request_data)

    def parse_quads_from_json(self, query_response):
        if self.validate_more_than_one_quad(query_response):
            return [Quadcopter(*quad.values()) for quad in query_response['data']['allQuadcopters']]
        return [Quadcopter(*query_response['data']['allQuadcopters'][0].values())]

    def validate_more_than_one_quad(self, quads_dictionary):
        return len(quads_dictionary['data']['allQuadcopters']) > 1

    def import_gridcell_plots(self, x, y):
        json_body = '{mapData(x:'+str(x)+',y:'+str(y)+')'+get_entity_as_json("GridCell_plots")+'}'
        request_data = requests.post(self.url, json={"query": json_body}).json()
        return self.parse_gridcell_plots_from_json(request_data, x, y)

    def parse_gridcell_plots_from_json(self, query_response, x, y):
        if query_response['data']['mapData']['plot'] == []:
            return [Plot(x, y, *plot) for plot in generate_random_plot()]
        return [Plot(x, y, *plot.values()) for plot in query_response['data']['mapData']['plot']]

    def import_gridcell(self, x, y):
        json_body = '{mapData(x:'+str(x)+',y:'+str(y)+')'+get_entity_as_json("GridCell")+'}'
        request_data = requests.post(self.url, json={"query": json_body}).json()
        return self.parse_gridcell_from_json(request_data)

    def parse_gridcell_from_json(self, query_response):
        print(query_response['data']['mapData'])
        return GridCell([*query_response['data']['mapData'].values()])

    def import_events(self, isOpen):
        json_body = '{openEvents(isOpen:'+str(isOpen).lower()+')'+get_entity_as_json("Event")+'}'
        request_data = requests.post(self.url, json={"query": json_body}).json()
        return self.parse_events_from_json(request_data)

    def parse_events_from_json(self, query_response):
        if self.validate_more_than_one_event(query_response):
            return [Event(*event.values()) for event in query_response['data']['openEvents']]
        return [Event(*query_response['data']['openEvents'][0].values())]

    def validate_more_than_one_event(self, events_dictionary):
        return len(events_dictionary['data']['openEvents']) > 1

    def import_adoptionStatus(self):
        json_body = '{allAdoptionStatus' + get_entity_as_json("AdoptionStatus") + '}'
        request_data = requests.post(self.url, json={"query": json_body}).json()
        return self.parse_adoption_status_from_json(request_data)

    def parse_adoption_status_from_json(self, query_response):
        if self.validate_more_than_one_adoption_status(query_response):
            return [AdoptionStatus(*adoption_status.values()) for adoption_status in query_response['data']['allAdoptionStatus']]
        return AdoptionStatus(*query_response['data']['allAdoptionStatus'][0].values())

    def validate_more_than_one_adoption_status(self, adoption_status_dictionary):
        return len(adoption_status_dictionary['data']['allAdoptionStatus']) > 1

    def import_adoptees(self, adoption_status_code):
        json_body = '{allAdoptees(adoptionStatusCode:'+str(adoption_status_code)+')'+get_entity_as_json("Adoptee")+'}'
        request_data = requests.post(self.url, json={"query": json_body}).json()
        return self.parse_adoptees_from_json(request_data)

    def parse_adoptees_from_json(self, query_response):
        if self.validate_more_than_one_adoptee(query_response):
            return [Adoptee(*adoptee.values()) for adoptee in query_response['data']['allAdoptees']]
        return [Adoptee(*query_response['data']['allAdoptees'][0].values())]

    def validate_more_than_one_adoptee(self, adoptee_dictionary):
        return len(adoptee_dictionary['data']['allAdoptees']) > 1

    def import_pet_types(self):
        json_body = '{allPetTypes'+get_entity_as_json("PetType")+'}'
        request_data = requests.post(self.url, json={"query": json_body}).json()
        return self.parse_pet_types_from_json(request_data)

    def parse_pet_types_from_json(self, query_response):
        return [PetType(*petType.values()) for petType in query_response['data']['allPetTypes']]


'''
    def import_AI_status(self):
        request_data = Requests.post(self.url, json={"query": get_entity_as_json('AiStatus') }).json()
        return self.parse_status_from_json(request_data)

    def parse_status_from_json(self, query_response):
        return AiStatus(*query_response['data'].values())
'''


class GraphQlMutation:

    def __init__(self, url):
        self.url = url

    def set_plot(self, plot):
        for dataset in plot:
            #data = requests.post(self.url, json={"query": "mutation setPlot "+'{setPlot(cellX: %d, cellY: %d, timestamp: %d,x: %f,y: %f,z: %f)' % dataset.for_mutation() + '}'}).json()
            F = open("p.txt", "a")
            F.write("mutation setPlot "+'{setPlot(cellX: %d, cellY: %d, timestamp: %d,x: %f,y: %f,z: %f)' % dataset.for_mutation() + '}\r')
            F.close()
        return None

    def set_grid_plots(self, grid_plots):
        for plot in grid_plots:
            self.set_plot(plot)
        return None

    def create_event(self, drone_id, drone_x, drone_y):
        drone_properties = (drone_id, drone_x, drone_y)
        requests.post(self.url, json={"query": "mutation createEvent "+'{createEvent(quadId: %d,x: %d,y: %d)' % drone_properties + '{id}}'}).json()
        print("mutation createEvent "+'{createEvent(quadId: %d,x: %d,y: %d)' % drone_properties + '{id}}')
        return None

    def set_history(self, history):
        #data = requests.post(self.url, json={"query": "mutation setHistory "+'{setHistory(cellX: %d, cellY: %d,petTypeCode: %d,amount: %d)' % history.for_mutation() +'}'}).json()
        F = open("h.txt", "a")
        F.write("mutation setHistory "+'{setHistory(cellX: %d, cellY: %d,petTypeCode: %d,amount: %d)' % history.for_mutation() +'}\r')
        F.close()
        return None

    def set_cell_history(self, histories):
        for history in histories:
            self.set_history(history)
        return None

    def set_grid_history(self, grid_histories):
        for line in grid_histories:
            for cell in line:
                self.set_cell_history(cell)
        return None

    def set_adopter(self, adopter):
        if adopter.secondpreferred is None:
            requests.post(self.url, json={"query": "mutation setAdopters "+'{setAdopters(name: \"%s\",preferredCode: %d,isValid: %s)' % adopter.for_mutation() +'}'}).json()
        else:
            requests.post(self.url, json={"query": "mutation setAdopters "+'{setAdopters(name: \"%s\", preferredCode: %d, secondPreferredCode: %d, isValid: %s)' % adopter.for_mutation() +'}'}).json()
        return None

    def set_adopters(self, adopters):
        for adopter in adopters:
            self.set_adopter(adopter)
        return None

    def set_adoptee(self, adoptee):
        if adoptee.pet_type.description != "none":
            #data = requests.post(self.url, json={"query": "mutation setAdoptee " + '{setAdoptee(petTypeCode: %d, x: %d, y: %d, imageBeforeUrl: \"%s\", imageAfterUrl: \"%s\", adoptionStatusCode: %d)' % adoptee.for_mutation() + '}'}).json()
            F = open("anim.txt", "a")
            F.write("mutation setAdoptee " + '{setAdoptee(petTypeCode: %d, x: %d, y: %d, imageBeforeUrl: \"%s\", imageAfterUrl: \"%s\", adoptionStatusCode: %d)' % adoptee.for_mutation() + '}\r')
            F.close()
        return None

    def set_adoptees(self, adoptees):
        for adoptee in adoptees:
            self.set_adoptee(adoptee)
        return None

    def set_grid_cell(self, grid_line):
        for grid_cell in grid_line:
            #data = requests.post(self.url, json={"query": "mutation setGridCell "+'{setGridCell(x: %d, y: %d, lastPictureUrl: \"%s\", petTypeCode: %d)' % grid_cell.for_mutation() +'}'}).json()
            F = open("g_cells.txt", "a")
            F.write("mutation setGridCell "+'{setGridCell(x: %d, y: %d, lastPictureUrl: \"%s\", petTypeCode: %d)' % grid_cell.for_mutation() +'}\r')
            F.close()
        return None

    def set_grid(self, grid):
        for grid_line in grid:
            self.set_grid_cell(grid_line)
        return None

    def set_quads(self, quads):
        for quad in quads:
            requests.post(self.url, json={"query": "mutation setQuadcopter "+'{setQuadcopter(name: \"%s\", x: %d, y: %d)}' % (quad.name, quad.x, quad.y)}).json()
        return None

    def adopt(self, adopterId, adopteeX, adopteeY):
        requests.post(self.url, json={"query": "mutation adopt " + '{adopt(adopterId: %s, adopteeX: %d, adopteeY: %d)}' % (adopterId, adopteeX, adopteeY)}).json()
        return None

    def close_event(self, event_id, pet_type_code):
        requests.post(self.url, json={"query": "mutation closeEvent " + '{closeEvent(eventId: %s, petTypeCode: %d)}' % (event_id, pet_type_code)}).json()
        return None
