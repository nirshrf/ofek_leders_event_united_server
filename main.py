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
        return None


def run_server(path, port, handler=ServerHandler):
    httpd = socketserver.TCPServer((path, port), handler)
    print("serving at port", port)
    httpd.serve_forever()


if __name__ == '__main__':
    run_server("", 8080, ServerHandler)

