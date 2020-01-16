from generations.generatePlot import generate_plot
from generations.generateHeatmap import generate_heat_map
from generations.generateAnimal import generate_animal
from generations.generateHistory import generate_cell_animals_history
from Entities import Plot, History, Heatmap
from generations.conversions import ParseToEntities, ParseFromEntities
from graphqlHandler import GraphQLRequests

if __name__ == '__main__':
    graph_handler = GraphQLRequests("http://localhost:9000/graphql")
    to_entity_parser = ParseToEntities()
    from_entity_parser = ParseFromEntities()
    heat_map = to_entity_parser.heatmap(generate_heat_map())
    print(heat_map)
    for hm in heat_map:
        print("heat map : ", hm)
    h_map = from_entity_parser.heatmap(heat_map)
    animals = to_entity_parser.generate_animals(h_map)
    print(animals)
    for animal in animals:
        print("animals : ", animal)
    plots = to_entity_parser.generate_plots(animals)
    print(plots)
    for plot in plots:
        print("plots : ", plot)
    all_history = to_entity_parser.generate_animals_history(h_map, 100)
    for h in all_history:
        print("History : ", h)

