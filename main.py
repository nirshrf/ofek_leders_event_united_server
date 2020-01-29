from http.server import SimpleHTTPRequestHandler
import socketserver
from requests_handler import execute_drones, match_adopters, classify_animal_from_grid_cell
from generateAll import generate_all_data
from generations.generateQuacopters import generate_quadcopters
import json
from Data.app_properties import model


def parse_x_y_from_body(post_body):
    json_as_string = str(post_body)[2:-1]
    json_as_dict = json.loads(json_as_string)
    return json_as_dict['x'], json_as_dict['y']


class ServerHandler(SimpleHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html/json')
        self.end_headers()

    def do_POST(self):
        self._set_headers()
        content_len = int(self.headers['Content-Length'])
        post_body = self.rfile.read(content_len)
        print(self.path[1:], post_body)
        if self.path[1:] == "generate_data":
            print("Generating Data...")
            #generate_all_data()
            print("Data generated!")
        elif self.path[1:] == "send_drones":
            print("Sending Drones...")
            execute_drones()
            print("Drones sent!")
        elif self.path[1:] == "generate_drones":
            generate_quadcopters(5)
        elif self.path[1:] == "classify_animal":
            print("classify animal")
            x, y = parse_x_y_from_body(post_body)
            animal = classify_animal_from_grid_cell(x, y, model)
            self.wfile.write(animal.encode('utf-8'))
        elif self.path[1:] == "adopt":
            print("Beginning to match adoptees to adopters")
            match_adopters()
            print("matched!")
        self.end_headers()
        return


def run_server(path, port, handler=ServerHandler):
    httpd = socketserver.TCPServer((path, port), handler)
    print("serving at port", port)
    httpd.serve_forever()


if __name__ == '__main__':
#   test
#   print(graphqlrequests.import_gridcell(1, 1))
#   end test
    run_server("", 8080, ServerHandler)


