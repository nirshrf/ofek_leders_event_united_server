from numpy.random import choice
from copy import deepcopy


def generate_animal(x,y, heat_map):
    """
    this function generates an animal on the x,y rectangle on the grid, based on the given heat_map (heat map was already
    produced earlier)
    """
    animals_probs = deepcopy(heat_map[x][y])
    animals_probs["none"] = 1.0 - sum(animals_probs.values())
    return choice(list(animals_probs.keys()), 1, p=list(animals_probs.values()))[0]