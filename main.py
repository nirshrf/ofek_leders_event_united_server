from http.server import SimpleHTTPRequestHandler
import socketserver
import json
import requests
from graphqlHandler import GraphQLRequests, GraphQlMutation
from Entities import Plot
import bytes

JAVA_server_url = 'http://localhost:9000/graphql'


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
    #   test
    graphqlrequests = GraphQLRequests(JAVA_server_url)
    graphqlmutation = GraphQlMutation(JAVA_server_url)
    print(graphqlrequests.import_AI_status())
    print(graphqlmutation.set_plot(Plot(55, 'hello', 1, 2, 3)))
    #   end test
    run_server("", 8080, ServerHandler)


