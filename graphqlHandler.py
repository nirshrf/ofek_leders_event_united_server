import requests
from Entities import Coordinate, Adopter


class GraphQLRequests:
    def __init__(self, url):
        self.url = url

    def import_adopters(self):
        request_data = requests.post(self.url, json={"query": '{adopters{id, name, prefered, secondpreffered}}'}).json()
        return self.parse_adopters_from_json(request_data)

    def parse_adopters_from_json(self, query_response):
        if self.validate_more_than_one_adopter(query_response):
            return [Adopter(*adopter.values()) for adopter in query_response['data']['adopters']]
        return Adopter(*query_response['data']['adopters'][0].values())

    def validate_more_than_one_adopter(self, adopters_dictionary):
        return len(adopters_dictionary['data']['adopters']) > 1

