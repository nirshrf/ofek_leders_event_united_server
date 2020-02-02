from http.server import SimpleHTTPRequestHandler
import socketserver
from requests_handler import execute_drones, match_adopters, classify_animal_from_grid_cell, classify_animals_from_events
from generateAll import generate_all_data
from generations.generateQuacopters import generate_quadcopters
import json
from Data.app_properties import model
from flask import Flask, request

app = Flask(__name__)


def parse_x_y_from_body(post_body):
    json_as_string = str(post_body)[2:-1]
    json_as_dict = json.loads(json_as_string)
    return json_as_dict['x'], json_as_dict['y']


def parse_drones_amount_from_body(post_body):
    json_as_string = str(post_body)[2:-1]
    json_as_dict = json.loads(json_as_string)
    return json_as_dict['amount']


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
        if self.path[1:] == "generate_drones":
            drones_amount = parse_drones_amount_from_body(post_body)
            print("generating %d drones.." % drones_amount)
            generate_quadcopters(parse_drones_amount_from_body(drones_amount))
        elif self.path[1:] == "classify_animal":
            print("classify animal")
            x, y = parse_x_y_from_body(post_body)
            animal = classify_animal_from_grid_cell(x, y, model)
            self.wfile.write(animal.encode('utf-8'))
        self.end_headers()
        return


def run_server(path, port, handler=ServerHandler):
    httpd = socketserver.TCPServer((path, port), handler)
    print("serving at port", port)
    httpd.serve_forever()


@app.route('/')
def hello():
    if request.method == 'GET':
        return "Hello _GET"
    elif request.method == 'POST':
        return "Hello _POST"
    else:
        return None


@app.route('/send_drones')
def send_quadcopters():
    if request.method == 'POST':
        print("Sending Drones...")
        execute_drones()
        return "Drones sent!"
    return "In order to deploy the drones send a POST request to this endpoint"


@app.route('/close_events')
def close_events():
    if request.method == 'POST':
        classify_animals_from_events(model)
        return "closed events!"
    return "In order to close the events send a POST request to this endpoint"


@app.route('/match_animals')
def match_animals():
    if request.method == 'POST':
        print("Beginning to match adoptees to adopters")
        match_adopters()
        return "matched adopters!"
    return "In order to match the animals send a POST request to this endpoint"


if __name__ == '__main__':
    #run_server("", 8080, ServerHandler)
    app.run()

