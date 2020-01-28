from generations.generateAnimal import generate_animal
from generations.generateHistory import generate_cell_animals_history
from generations.generatePlot import generate_plots
from Entities import Plot, History, Heatmap, Adoptee
from animalsPictureDictionary import get_animal_picture_url
from adoptionStatusDictionary import get_adoption_status
from petTypeDictionary import get_pet_type


class ParseToEntities:
    def __init__(self):
        pass

    def heatmap(self, heatmap_as_list):
        heatmap_as_entities = [[Heatmap(*cell.values()) for cell in heatmap] for heatmap in heatmap_as_list]
        return heatmap_as_entities

    def plots(self, x, y, plots_as_list):
        plots_as_entities = [Plot(x, y, *plot) for plot in plots_as_list]
        return plots_as_entities

    def generate_animals(self, heatmap_as_dictionary):
        animals_as_entities = []
        for y in range(100):
            for x in range(100):
                animal = generate_animal(x, y, heatmap_as_dictionary)
                if animal != 'none':
                    animals_as_entities.append(Adoptee(get_pet_type(animal), x, y, get_animal_picture_url(animal), get_animal_picture_url(animal), get_adoption_status('not_adopted')))
        return animals_as_entities

    def history(self,x,y,history_as_tuple):
        return History(x, y, get_pet_type(history_as_tuple[0]), history_as_tuple[1])

    def generate_animals_history(self, heatmap_as_dictionary, sample_size):
        animals_history = []
        animals_line = []
        animal_history = []
        for y in range(100):
            for x in range(100):
                for h in generate_cell_animals_history(x, y, sample_size, heatmap_as_dictionary).items():
                    animal_history.append(self.history(x+10, y+10,h))
                animals_line.append(animal_history)
                animal_history = []
            animals_history.append(animals_line)
            animals_line = []
        return animals_history

    def generate_grid_plots(self, animals_as_entities):
        plots = []
        for animal in animals_as_entities:
            if animal.pet_type.description != 'none':
                plots.append(self.plots(animal.x, animal.y, generate_plots(animal.pet_type.description)))
        return plots


class ParseFromEntities:
    def __init__(self):
        pass

    def heatmap(self, heatmap):
        heatmap_as_dictionary = [[cell_distribution.to_dictionary() for cell_distribution in h_map] for h_map in heatmap]
        return heatmap_as_dictionary

    def plots(self, plots_as_entities):
        plots_as_tuples = [plot.to_tuple() for plot in plots_as_entities]
        return plots_as_tuples

    def adopters_dictionary(self, adopters_as_entities):
        adopters_dictionary = {}
        for adopter in adopters_as_entities:
            if adopter.secondpreferred is None:
                adopters_dictionary[adopter.name] = ["None"]
            else:
                adopters_dictionary[adopter.name] = [adopter.preferred.description, adopter.secondpreferred.description]
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


to_entity_parser = ParseToEntities()
from_entity_parser = ParseFromEntities()


