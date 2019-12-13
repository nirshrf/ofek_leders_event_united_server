import requests
from Entities import *

class GraphQLRequests:
    def __init__(self, url):
        self.url = url

    def importAdopters(self):
        requestData = requests.post(self.url, json={"query": '{adopters{id, name, prefered, secondpreffered}}'}).json()
        return self.parseAdoptersFromJson(requestData)

    def parseAdoptersFromJson(self, queryResponse):
        if self.validateMoreThanOneAdopter(queryResponse):
            return [Adopter(*adopter.values()) for adopter in queryResponse['data']['adopters']]
        return Adopter(*queryResponse['data']['adopters'][0].values())

    def validateMoreThanOneAdopter(self, adoptersDictionary):
        return len(adoptersDictionary['data']['adopters']) > 1

