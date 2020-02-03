from requests_handler import execute_drones, match_adopters, classify_animals_from_events, create_adopter
from Data.app_properties import model, thread_flags
from flask import Flask, request
import threading


drones_executor = threading.Thread(target=execute_drones, daemon=True)
classifier = threading.Thread(target=classify_animals_from_events, args=(model,), daemon=True)
match_maker = threading.Thread(target=match_adopters, daemon=True)
adopter_creator = threading.Thread(target=create_adopter, daemon=True)

threads = dict(drones_executor=drones_executor,
               classifier=classifier,
               match_maker=match_maker,
               adopter_creator=adopter_creator)

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def hello():
    if request.method == 'GET':
        return "Hello _GET"
    elif request.method == 'POST':
        return "Hello _POST"
    else:
        return None


@app.route('/send_drones', methods=['POST', 'GET'])
def send_quadcopters():
    if request.method == 'POST':
        thread = threads['drones_executor']
        if thread.is_alive():
            thread_flags['drones_executor_flag'] = False
            print("finished Drones...")
            thread.join()
        else:
            thread_flags['drones_executor_flag'] = True
            print("Sending Drones...")
            thread.start()
        return "Drones are sent!"
    return "In order to deploy the drones send a POST request to this endpoint"


@app.route('/close_events', methods=['POST', 'GET'])
def close_events():
    if request.method == 'POST':
        thread = threads['classifier']
        if thread.is_alive():
            thread_flags['classifier_flag'] = False
            print("finished closing events...")
            thread.join()
        else:
            thread_flags['classifier_flag'] = True
            print("closing events...")
            thread.start()
        return "closed events!"
    return "In order to close the events send a POST request to this endpoint"


@app.route('/match_animals', methods=['POST', 'GET'])
def match_animals():
    if request.method == 'POST':
        thread = threads['match_maker']
        if thread.is_alive():
            thread_flags['match_maker_flag'] = False
            print("finished to match adoptees to adopters")
            thread.join()
        else:
            thread_flags['match_maker_flag'] = True
            print("Beginning to match adoptees to adopters")
            thread.start()
        return "matched adopters!"
    return "In order to match the animals send a POST request to this endpoint"


if __name__ == '__main__':
    print("creating adopters")
    threads['adopter_creator'].start()
    print("starting app")
    app.run()

