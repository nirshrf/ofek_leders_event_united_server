from generations.generateHeatmap import generate_heat_map
from generations.generateAnimal import generate_animal
from generations.generateHistory import generate_cell_animals_history
from generations.generatePlot import generate_plot
from Entities import Plot, History, Heatmap, Quadcopter


class ParseToEntities:

    def __init__(self):
        pass

    def heatmap(self, heatmap_as_list):
        heatmap_as_entities = [[Heatmap(*cell.values()) for cell in heatmap] for heatmap in heatmap_as_list]
        return heatmap_as_entities

    def plots(self, plots_as_list):
        plots_as_entities = [Plot(*plot) for plot in plots_as_list]
        return plots_as_entities

    def history(self, id, animal_history, pet_types):
        history = [History(id, pet_types[h[0]], h[1]) for h in animal_history.items()]

    def generate_animals(self, heatmap_as_dictionary):
        animals_as_entities = [[generate_animal(x, y, heatmap_as_dictionary) for y in range(100)] for x in range(100)]
        return animals_as_entities

    def generate_animals_history(self, heatmap_as_dictionary, sample_size):
        animals_history = [[generate_cell_animals_history(x, y, sample_size, heatmap_as_dictionary) for y in range(100)] for x in range(100)]
        return animals_history

    def generate_plots(self, animals_as_list):
        plots = []
        plots_line = []
        x, y = 0, 0
        for animal_line in animals_as_list:
            for animal in animal_line:
                if animal != 'None':
                    plots_line.append(self.plots(generate_plot(animal)))
                else:
                    plots_line.append(None)
            plots.append(plots_line)
            plots_line = []
        return plots


class ParseFromEntities:
    def __init__(self):
        pass

    def heatmap(self, heatmap):
        heatmap_as_dictionary = [[cell.to_dictionary() for cell in h_map] for h_map in heatmap]
        return heatmap_as_dictionary

    def plots(self, plots_as_entities):
        plots_as_tuples = [plot.to_tuple() for plot in plots_as_entities]
        return plots_as_tuples

    def adopters_dictionary(self, adopters_as_entities):
        adopters_dictionary = {}
        for adopter in adopters_as_entities:
            adopters_dictionary[adopter.id] = [adopter.preferred.description, adopter.secondpreferred.description]
        return adopters_dictionary

    def free_drones(self, drones_as_entities):
        free_drones = {}
        for drone in drones_as_entities:
            if drone.isfree:
                free_drones[drone.id] = (drone.x, drone.y)
        return free_drones

    def busy_drones(self, drones_as_entities):
        busy_drones = {}
        for drone in drones_as_entities:
            if not drone.isfree:
                busy_drones[drone.id] = (drone.x, drone.y)
        return busy_drones
