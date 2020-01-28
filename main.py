from http.server import SimpleHTTPRequestHandler
import socketserver
from requests_handler import classify_animal_from_grid_cell, execute_drones


def parse_x_y_from_body(post_body):
    return int(str(post_body)[-7:-5]), int(str(post_body)[-4:-2])


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
#           generator.generate_all_data()
            print("Data generated!")
        elif str(post_body)[2:-1] == '\"Send_Drones\"':
            print("Sending Drones...")
            execute_drones()
            print("Drones sent!")
        elif str(post_body)[2:-1] == '\"Generate_Drones\"':
#           generator.generate_quadcopters(10)
            pass
        elif str(post_body)[2:-8] == '\"Classify_Animal':
            print("classify animal")
            x, y = parse_x_y_from_body(post_body)
            animal = classify_animal_from_grid_cell(x, y)
            self.wfile.write(animal.encode('utf-8'))
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


