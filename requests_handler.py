from graphql_handler.graphqlHandler import GraphQLRequests, GraphQlMutation
from generations.generateHeatmap import generate_heat_map
from team1_solution import send_drones
from generations.conversions import from_entity_parser
from team2_ai_solution.team2_ai_solution import compute_features_df
from Data.app_properties import JAVA_server_url
from model import *


def execute_drones():
    events = []
    graph_query_handler = GraphQLRequests(JAVA_server_url)
    graph_mutation_handler = GraphQlMutation(JAVA_server_url)
    adopters = graph_query_handler.import_adopters()
    adopters_as_dictionary = from_entity_parser.adopters_dictionary(adopters)
    drones = graph_query_handler.import_quads()
    free_drones, busy_drones = from_entity_parser.free_drones(drones), from_entity_parser.busy_drones(drones)
    drones_to_send = send_drones(generate_heat_map(), adopters_as_dictionary, free_drones, busy_drones, 1, 1)
    for drone in drones_to_send.items():
        events.append(graph_mutation_handler.create_event(int(drone[0]), drone[1][0], drone[1][1]))
    print(events)

##############################################################################
########     when you want to classify an animal using it's graph  ###########
##############################################################################


def classify_animal(plots):
    '''
    plots - > [(ts_1,x_1,y_1,z_1),.....,(ts_n,x_n,y_n,z_n)]
    0<=n<60
    return value:
    item from list - ["none", "cat", "dog", "parrot", "rabbit"]
    '''
    features_df = compute_features_df(plots)
    model_predictions = list(model.predict(features_df))
    return model_predictions


def classify_animal_from_grid_cell(x, y):
    graph_handler = GraphQLRequests(JAVA_server_url)
    plots_as_entities = graph_handler.import_gridcell_plots(x, y)
    plots_as_list = [tuple([plot.timestamp, plot.x, plot.y, plot.z]) for plot in plots_as_entities]
    plots_as_list.sort(key=lambda tup: tup[0])
    return classify_animal([plots_as_list])[0]
