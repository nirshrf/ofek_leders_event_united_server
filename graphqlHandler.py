import requests
from Entities import Coordinate, Adopter, Quadcopter, GridCell, EventStatus, Event, PetType, AdoptionStatus, Adoptee, AiStatus


class GraphQLRequests:
    def __init__(self, url):
        self.url = url

    def import_adopters(self):
        request_data = requests.post(self.url, json={"query": '{adopters{id, name, preferred{id, code, description}, secondpreferred{id, code, description}}}'}).json()
        return self.parse_adopters_from_json(request_data)

    def parse_adopters_from_json(self, query_response):
        if self.validate_more_than_one_adopter(query_response):
            return [Adopter(*adopter.values()) for adopter in query_response['data']['adopters']]
        return Adopter(*query_response['data']['adopters'][0].values())

    def validate_more_than_one_adopter(self, adopters_dictionary):
        return len(adopters_dictionary['data']['adopters']) > 1

    def import_quads(self):
        request_data = requests.post(self.url, json={"query": '{allQuadcopters{id, name, launchtime, isfree, x, y}}'}).json()
        return self.parse_quads_from_json(request_data)

    def parse_quads_from_json(self, query_response):
        if self.validate_more_than_one_quad(query_response):
            return [Quadcopter(*quad.values()) for quad in query_response['data']['allQuadcopters']]
        return Quadcopter(*query_response['data']['allQuadcopters'][0].values())

    def validate_more_than_one_quad(self, quads_dictionary):
        return len(quads_dictionary['data']['allQuadcopters']) > 1

    def import_gridcell(self, x, y):
        json_body = '{mapData(x:'+str(x)+',y:'+str(y)+'){id, x, y, lastPictureUrl, history{id, petType{id, code, description},amount}}}'
        request_data = requests.post(self.url, json={"query": json_body}).json()
        return self.parse_gridcell_from_json(request_data)

    def parse_gridcell_from_json(self, query_response):
        return GridCell(*query_response['data']['mapData'].values())

    def import_events(self, isOpen):
        json_quadcopter = '{id, name, launchtime, isfree, x, y}'
        json_eventStatus = '{id, code, description}'
        json_body = '{openEvents(isOpen:'+str(isOpen).lower()+'){id, quadcopter' + json_quadcopter + ', x, y, eventTime, eventStatus'+json_eventStatus+'}}'
        request_data = requests.post(self.url, json={"query": json_body}).json()
        return self.parse_events_from_json(request_data)

    def parse_events_from_json(self, query_response):
        if self.validate_more_than_one_event(query_response):
            return [Event(*event.values()) for event in query_response['data']['openEvents']]
        return Event(*query_response['data']['openEvents'][0].values())

    def validate_more_than_one_event(self, events_dictionary):
        return len(events_dictionary['data']['openEvents']) > 1

    def import_adoptionStatus(self):
        json_adoptionStatus = '{id, code, description}'
        json_body = '{allAdoptionStatus' + json_adoptionStatus + '}'
        request_data = requests.post(self.url, json={"query": json_body}).json()
        return self.parse_adoptionstatus_from_json(request_data)

    def parse_adoptionstatus_from_json(self, query_response):
        if self.validate_more_than_one_adoption_status(query_response):
            return [AdoptionStatus(*adoption_status.values()) for adoption_status in query_response['data']['allAdoptionStatus']]
        return Event(*query_response['data']['allAdoptionStatus'][0].values())

    def validate_more_than_one_adoption_status(self, adoption_status_dictionary):
        return len(adoption_status_dictionary['data']['allAdoptionStatus']) > 1

    def import_adoptees(self, adoption_status_code):
        json_adoptionStatus = 'adoptionStatus{id, code, description}'
        json_petType = 'petType{id, code, description}'
        json_body = '{allAdoptees(adoptionStatusCode:' + str(adoption_status_code) + '){id,' + json_petType + ', x, y, imageBeforeURL, imageAfterURL,' + json_adoptionStatus+'}}'
        request_data = requests.post(self.url, json={"query": json_body}).json()
        return self.parse_adoptees_from_json(request_data)

    def parse_adoptees_from_json(self, query_response):
        if self.validate_more_than_one_adoptee(query_response):
            return [Adoptee(*adoptee.values()) for adoptee in query_response['data']['allAdoptees']]
        return Event(*query_response['data']['allAdoptees'][0].values())

    def validate_more_than_one_adoptee(self, adoptee_dictionary):
        return len(adoptee_dictionary['data']['allAdoptees']) > 1

    def import_AI_status(self):
        json_body = '{toggleDroneAI, togglePetsAI, toggleAdoptionAI, toggleBdaAI}'
        request_data = requests.post(self.url, json={"query": json_body}).json()
        return self.parse_status_from_json(request_data)

    def parse_status_from_json(self, query_response):
        return AiStatus(*query_response['data'].values())
