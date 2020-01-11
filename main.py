from http.server import SimpleHTTPRequestHandler
import socketserver
import json
import requests
from graphqlHandler import GraphQLRequests
from Entities import Coordinate, Adopter
import bytes


class ServerHandler(SimpleHTTPRequestHandler):
    def do_POST(self):
        content_len = int(self.headers['Content-Length'])
        post_body = self.rfile.read(content_len)

#       Check the graphql query
        service_url = "http://localhost:9000/graphql"
        request_handler = GraphQLRequests(service_url)
        print(request_handler.import_adopters())
        print(request_handler.import_quads())
        print(request_handler.import_gridcell(1, 1))
        print(request_handler.import_events(True))
        print(request_handler.import_adoptionStatus())
        print(request_handler.import_adoptees(1))
        print(request_handler.import_AI_status())


def run_server(path, port, handler=ServerHandler):
    httpd = socketserver.TCPServer((path, port), handler)
    print("serving at port", port)
    httpd.serve_forever()


if __name__ == '__main__':
    run_server("", 8080, ServerHandler)

