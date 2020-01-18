from graphqlHandler import GraphQLRequests, GraphQlMutation
from generations.generateHeatmap import generate_heat_map
from challenges.firstChallenge import send_drones
from generations.conversions import ParseFromEntities, ParseToEntities

if __name__ == '__main__':
    global JAVA_server_url
    events = []
    graph_query_handler = GraphQLRequests(JAVA_server_url)
    graph_mutation_handler = GraphQlMutation(JAVA_server_url)
    from_entities_parser = ParseFromEntities()
    to_entities_parser = ParseToEntities()
    adopters = graph_query_handler.import_adopters()
    adopters_as_dictionary = from_entities_parser.adopters_dictionary(adopters)
    drones = graph_query_handler.import_quads()
    free_drones, busy_drones = from_entities_parser.free_drones(drones), from_entities_parser.busy_drones(drones)
    drones_to_send = send_drones(generate_heat_map(), adopters_as_dictionary, free_drones, busy_drones, 1, 1)
    for drone in drones_to_send.items():
        events.append(graph_mutation_handler.create_event(int(drone[0]), drone[1][0], drone[1][1]))
    print(events)
