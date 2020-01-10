import requests
from Entities import Coordinate, Adopter, Quadcopter, GridCell


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

    def validate_more_than_one_quad(self, adopters_dictionary):
        return len(adopters_dictionary['data']['allQuadcopters']) > 1

    def import_gridcell(self, x, y):
        json_body = '{mapData(x:'+str(x)+',y:'+str(y)+'){id, x, y, lastPictureUrl, history{id, petType{id, code, description},amount}}}'
        request_data = requests.post(self.url, json={"query": json_body}).json()
        return self.parse_gridcell_from_json(request_data)

    def parse_gridcell_from_json(self, query_response):
        return GridCell(*query_response['data']['mapData'].values())

