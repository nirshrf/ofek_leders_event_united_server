from generations.generateHeatmap import generate_heat_map
from generations.generateAdopters import generate_adopters
from generations.conversions import to_entity_parser, from_entity_parser
from graphql_handler.graphqlHandler import GraphQLRequests, GraphQlMutation
from generations.generate_grid_cell import generate_grid_cell
import timeit as time
from Data.app_properties import JAVA_server_url


def generate_all_data():
    graph_mutation_handler = GraphQlMutation(JAVA_server_url)
    heat_map = to_entity_parser.heatmap(generate_heat_map())
    h_map = from_entity_parser.heatmap(heat_map)
    print("generating animals..", time.time.ctime())
    animals = to_entity_parser.generate_animals(h_map)
    print("generating grid..", time.time.ctime())
    grid = generate_grid_cell(animals, 100)
    print("generating plots..", time.time.ctime())
    plots = to_entity_parser.generate_grid_plots(animals)
    print("generating history..", time.time.ctime())
    all_history = to_entity_parser.generate_animals_history(h_map, 1000)
    print("generating adopter..", time.time.ctime())
    adopters = generate_adopters(50)
    print("generations finished!", time.time.ctime())
    print("starting grid..", time.time.ctime())
    graph_mutation_handler.set_grid(grid)
    print("starting plots..", time.time.ctime())
    graph_mutation_handler.set_grid_plots(plots)
    print("starting history..", time.time.ctime())
    graph_mutation_handler.set_grid_history(all_history)
    print("starting adopter..", time.time.ctime())
    graph_mutation_handler.set_adopters(adopters)
    print("starting animals..", time.time.ctime())
    graph_mutation_handler.set_adoptees(animals)
    print("Data finished!", time.time.ctime())

