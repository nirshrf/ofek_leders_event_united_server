from http.server import SimpleHTTPRequestHandler
import socketserver
from graphqlHandler import GraphQLRequests, GraphQlMutation
import Requests
import generations as generator

JAVA_server_url = 'http://cto.southcentralus.cloudapp.azure.com:9000/graphql'


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
            print("Generating Data...")
            #generator.generate_all_data()
            print("Data generated!")
        elif str(post_body)[2:-1] == '\"Send_Drones\"':
            print("Sending Drones...")
            Requests.execute_drones()
            print("Drones sent!")
        elif str(post_body)[2:-1] == '\"get_pet_types\"':
            exec(open("Data/petTypeDictionary.py").read())
        elif str(post_body)[2:-1] == '\"Generate_Drones\"':
            generator.generate_quadcopters(10)
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


