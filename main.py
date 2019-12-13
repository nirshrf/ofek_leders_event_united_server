from http.server import  SimpleHTTPRequestHandler
import socketserver
import json
from graphqlHandler import *
import bytes


class ServerHandler(SimpleHTTPRequestHandler):

    def do_POST(self):
        serviceUrl = "http://localhost:9000/graphql"
        contentLen = int(self.headers['Content-Length'])
        postBody = self.rfile.read(contentLen)
        coordinates = self.parseToCoordinates(postBody)
        print(coordinates)
        requestHandler = GraphQLRequests(serviceUrl)
        print(requestHandler.importAdopters())


    def convertPostMessageToDictionary(self, postBody):
        return json.loads(postBody)

    def parseToCoordinates(self, postBody):
        coordinatesDictionary = self.convertPostMessageToDictionary(postBody)
        if self.validateMoreThanOneAnimalPassed(coordinatesDictionary):
            return [Coordinate(*pair) for pair in coordinatesDictionary['coordinates']]
        return Coordinate(*coordinatesDictionary['coordinates'])

    def validateMoreThanOneAnimalPassed(self, coordinatesDictionary):
        return isinstance(coordinatesDictionary['coordinates'][0], list)

class AnimalsFromMap:
    def __init__(self, coordinates, url):
        self.coordinates = coordinates
        self.url = url
        self.isList = len(self.coordinates) > 1

    def get(self):
        if self.isList:
            return [self.getAnimalFromDB(coordinate) for coordinate in self.coordinates]
        return self.getAnimalFromDB(self.coordinates)

    def getAnimalFromDB(self, coordinate):
        #Get animal from DB with coordinate
        return requests.post(self.url, json={"query": '{adopters{id, name, prefered, secondpreffered}}'}).json()

def runServer(path, port, handler=ServerHandler):
    httpd = socketserver.TCPServer((path, port), handler)
    print("serving at port", port)
    httpd.serve_forever()

if __name__ == '__main__':
    runServer("", 8080, ServerHandler)

