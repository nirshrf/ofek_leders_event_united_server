import requests
import graphene
from Entities import Adopter, Quadcopter, GridCell, Event, AdoptionStatus, Adoptee, AiStatus, JSON_dictionary, Plot, PetType


class GraphQLRequests:
    def __init__(self, url):
        self.url = url

    def import_adopters(self):
        request_data = requests.post(self.url, json={"query": '{adopters'+JSON_dictionary["Adopter"]+'}'}).json()
        return self.parse_adopters_from_json(request_data)

    def parse_adopters_from_json(self, query_response):
        if self.validate_more_than_one_adopter(query_response):
            return [Adopter(*adopter.values()) for adopter in query_response['data']['adopters']]
        return [Adopter(*query_response['data']['adopters'][0].values())]

    def validate_more_than_one_adopter(self, adopters_dictionary):
        return len(adopters_dictionary['data']['adopters']) > 1

    def import_quads(self):
        request_data = requests.post(self.url, json={"query": '{allQuadcopters'+JSON_dictionary["Quadcopter"]+'}'}).json()
        return self.parse_quads_from_json(request_data)

    def parse_quads_from_json(self, query_response):
        if self.validate_more_than_one_quad(query_response):
            return [Quadcopter(*quad.values()) for quad in query_response['data']['allQuadcopters']]
        return [Quadcopter(*query_response['data']['allQuadcopters'][0].values())]

    def validate_more_than_one_quad(self, quads_dictionary):
        return len(quads_dictionary['data']['allQuadcopters']) > 1

    def import_gridcell(self, x, y):
        json_body = '{mapData(x:'+str(x)+',y:'+str(y)+')'+JSON_dictionary["GridCell"]+'}'
        request_data = requests.post(self.url, json={"query": json_body}).json()
        return self.parse_gridcell_from_json(request_data)

    def parse_gridcell_from_json(self, query_response):
        return GridCell(*query_response['data']['mapData'].values())

    def import_events(self, isOpen):
        json_body = '{openEvents(isOpen:'+str(isOpen).lower()+')'+JSON_dictionary["Event"]+'}'
        request_data = requests.post(self.url, json={"query": json_body}).json()
        return self.parse_events_from_json(request_data)

    def parse_events_from_json(self, query_response):
        if self.validate_more_than_one_event(query_response):
            return [Event(*event.values()) for event in query_response['data']['openEvents']]
        return [Event(*query_response['data']['openEvents'][0].values())]

    def validate_more_than_one_event(self, events_dictionary):
        return len(events_dictionary['data']['openEvents']) > 1

    def import_adoptionStatus(self):
        json_body = '{allAdoptionStatus' + JSON_dictionary["AdoptionStatus"] + '}'
        request_data = requests.post(self.url, json={"query": json_body}).json()
        return self.parse_adoption_status_from_json(request_data)

    def parse_adoption_status_from_json(self, query_response):
        if self.validate_more_than_one_adoption_status(query_response):
            return [AdoptionStatus(*adoption_status.values()) for adoption_status in query_response['data']['allAdoptionStatus']]
        return AdoptionStatus(*query_response['data']['allAdoptionStatus'][0].values())

    def validate_more_than_one_adoption_status(self, adoption_status_dictionary):
        return len(adoption_status_dictionary['data']['allAdoptionStatus']) > 1

    def import_adoptees(self, adoption_status_code):
        json_body = '{allAdoptees(adoptionStatusCode:'+str(adoption_status_code)+')'+JSON_dictionary["Adoptee"]+'}'
        request_data = requests.post(self.url, json={"query": json_body}).json()
        return self.parse_adoptees_from_json(request_data)

    def parse_adoptees_from_json(self, query_response):
        if self.validate_more_than_one_adoptee(query_response):
            return [Adoptee(*adoptee.values()) for adoptee in query_response['data']['allAdoptees']]
        return [Adoptee(*query_response['data']['allAdoptees'][0].values())]

    def validate_more_than_one_adoptee(self, adoptee_dictionary):
        return len(adoptee_dictionary['data']['allAdoptees']) > 1

    def import_pet_types(self):
        json_body = '{allPetTypes'+JSON_dictionary["PetType"]+'}'
        request_data = requests.post(self.url, json={"query": json_body}).json()
        return self.parse_pet_types_from_json(request_data)

    def parse_pet_types_from_json(self, query_response):
        return [PetType(*petType) for petType in query_response['data']['allPetTypes']]


'''
    def import_AI_status(self):
        request_data = requests.post(self.url, json={"query": JSON_dictionary['AiStatus']}).json()
        return self.parse_status_from_json(request_data)

    def parse_status_from_json(self, query_response):
        return AiStatus(*query_response['data'].values())
'''


class GraphQlMutation:

    def __init__(self, url):
        self.url = url

    def set_plot(self, plot):
        request_data = requests.post(self.url, json={"query": "mutation setPlot "+'{setPlot(timestamp: \"%s\",x: %d,y: %d,z: %d)' % plot.to_tuple() +
                                                                                    JSON_dictionary['Plot'] +
                                                                                    '}'}).json()

        return self.parse_plot_from_json(request_data)

    def parse_plot_from_json(self, query_response):
        return Plot(*query_response['data']['setPlot'].values())

    def create_event(self, drone_id, drone_x, drone_y):
        drone_properties = (drone_id, drone_x, drone_y)
        request_data = requests.post(self.url, json={"query": "mutation createEvent "+'{createEvent(quadId: \"%d\",x: %d,y: %d)' % drone_properties +
                                                                                    JSON_dictionary['Event'] +
                                                                                    '}'}).json()

        return self.parse_event_from_json(request_data)

    def parse_event_from_json(self, query_response):
        return Event(*query_response['data']['createEvent'].values())


