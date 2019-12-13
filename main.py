from http.server import  SimpleHTTPRequestHandler
import socketserver
import json
import requests
from .Entities import *
import bytes


class Coordinate:
    def __init__(self, longitude, latitude):
        self.longitude = longitude
        self.latitude = latitude

    def __repr__(self):
        return "Longitude : " + str(self.longitude) + "\nLatitude : " + str(self.longitude)

    def __str__(self):
        return "Longitude : " + str(self.longitude) + "\nLatitude : " + str(self.longitude)

class ServerHandler(SimpleHTTPRequestHandler):

    def do_POST(self):
        serviceUrl = "http://localhost:9000/graphql"
        contentLen = int(self.headers['Content-Length'])
        postBody = self.rfile.read(contentLen)
        coordinates = self.parseToCoordinates(postBody)
        requestHandler = GraphQLRequests(serviceUrl)
        print(requestHandler.importAdopters())


    def convertPostMessageToDictionary(self, postBody):
        return json.loads(postBody)

    def parseToCoordinates(self, postBody):
        coordinatesDictionary = self.convertPostMessageToDictionary(postBody)
        if self.validateMoreThanOneAnimalPassed(coordinatesDictionary) > 1:
            return [Coordinate(*pair) for pair in coordinatesDictionary['coordinates']]
        return coordinatesDictionary['coordinates']

    def validateMoreThanOneAnimalPassed(self, coordinatesDictionary):
        return len(coordinatesDictionary['coordinates']) > 1

class AnimalsFromMap:
    def __init__(self, coordinates, url):
        self.coordinates = coordinates
        self.url = url
        self.isList = len(self.coordinates) > 1

    def get(self):
        if self.isList:
            return [self.getAnimalFromDB(coordinate) for coordinate in self.coordinates]
        return self.getAnimalFromDB(self.coordinates)

    def getAnimalFromDB(self ,coordinate):
        #Get animal from DB with coordinate
        return requests.post(self.url ,json = {"query": '{adopters{id, name, prefered, secondpreffered}}'}).json()

class GraphQLRequests:
    def __init__(self, url):
        self.url = url

    def importAdopters(self):
        requestData = requests.post(self.url,json = {"query": '{adopters{id, name, prefered, secondpreffered}}'}).json()
        return self.parseAdoptersFromJson(requestData)

    def parseAdoptersFromJson(self,JSON):
        if self.validateMoreThanOneAdopter(JSON) > 1:
            return [Adopter(*adopter) for adopter in JSON['data']['adopters']]
        return JSON['data']['adopters']

    def validateMoreThanOneAdopter(self,adoptersDictionary):
        return len(adoptersDictionary['data']['adopters']) > 1


def runServer(path, port, handler=ServerHandler):
    httpd = socketserver.TCPServer((path, port), handler)
    print("serving at port", port)
    httpd.serve_forever()

if __name__ == '__main__':
    runServer("",8080,ServerHandler)

