from http.server import SimpleHTTPRequestHandler
import socketserver
from graphqlHandler import GraphQLRequests, GraphQlMutation
from generations.generateAll import *

JAVA_server_url = 'http://localhost:9000/graphql'


class ServerHandler(SimpleHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html/json')
        self.end_headers()

    def do_POST(self):
        self._set_headers()
        content_len = int(self.headers['Content-Length'])
        post_body = self.rfile.read(content_len)
        if str(post_body)[2:-1] == '\"Generate_Data\"':
            exec(open("generations/generateAll.py").read())
        elif str(post_body)[2:-1] == '\"Send_Drones\"':
            exec(open("requests/sendUnallocatedDrones.py").read())
        self.end_headers()
        return


def run_server(path, port, handler=ServerHandler):
    httpd = socketserver.TCPServer((path, port), handler)
    print("serving at port", port)
    httpd.serve_forever()


if __name__ == '__main__':
    graphqlrequests = GraphQLRequests(JAVA_server_url)
    graphqlmutation = GraphQlMutation(JAVA_server_url)
#   test
    #print(graphqlrequests.import_gridcell(1, 1))
#   end test
    run_server("", 8080, ServerHandler)


