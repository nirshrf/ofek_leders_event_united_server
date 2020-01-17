from generations.generatePlot import generate_plot
from generations.generateHeatmap import generate_heat_map
from generations.generateAnimal import generate_animal
from generations.generateHistory import generate_cell_animals_history
from Entities import Plot, History, Heatmap
from generations.conversions import ParseToEntities, ParseFromEntities
from graphqlHandler import GraphQLRequests
from challenges.firstChallenge import send_drones


if __name__ == '__main__':
    global JAVA_server_url
    graph_handler = GraphQLRequests(JAVA_server_url)
    to_entity_parser = ParseToEntities()
    from_entity_parser = ParseFromEntities()
    heat_map = to_entity_parser.heatmap(generate_heat_map())
    h_map = from_entity_parser.heatmap(heat_map)
    animals = to_entity_parser.generate_animals(h_map)
    plots = to_entity_parser.generate_plots(animals)
    all_history = to_entity_parser.generate_animals_history(h_map, 100)

