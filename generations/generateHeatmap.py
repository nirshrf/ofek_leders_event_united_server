import numpy as np
from numpy.random import choice


animals_distribution = {"dog": 480, "cat": 450, "rabbit": 340, "parrot": 230} #total animals = 1500
total_non_animals = 8500
decay_factor = 0.87 # animal that is x distance from it's focal of it's community has decay_factor**x prob to be found there
start_prob = 0.82
focals_dists_from_center = 10 # distance of the focals from the center of the grid
focals_locations = {"dog": (50 - focals_dists_from_center, 50 - focals_dists_from_center),
                    "cat": (50 + focals_dists_from_center, 50 - focals_dists_from_center),
                    "rabbit": (50 - focals_dists_from_center, 50 + focals_dists_from_center),
                    "parrot": (50 + focals_dists_from_center, 50 + focals_dists_from_center)}
min_probs = {"dog": 0.03, "cat": 0.025, "rabbit": 0.005, "parrot": 0}


def cut_probs_to_fit_distribution(current_dist, cum_dist, req_dist):
    """
    the function will change curr_dist such that cum_dist + current_dist <= req_dist, making
    upper bound as necessary
    """
    return {animal: min(current_dist[animal], req_dist[animal]-cum_dist[animal]) for animal in current_dist}


def generate_heat_map():
    """
    the function will return a 100*100 grid, with each rectangle containing probabilities for animal appearances in it
    (represents by a dictionary of the form: {"cat":probability_for_cat,....})) - i.e. an heat map.
    this heat map can be used for generating animals on the grid or generating animals history in a rectangle.
    the probabilties in the heatmap represents the story that was given in the background.
    those probabilities agrees with the aniaml distribution (this heat_map won't create distribution which is very different
    to the given animals distribution)
    """
    total_animals_so_far = {"dog": 0, "cat": 0, "rabbit": 0, "parrot": 0}
    animals_grid = [[{"dog":0, "cat":0, "rabbit":0, "parrot":0} for j in range(100)] for i in range(100)]
    for radius in range(0, 100):
        for animal, focal in focals_locations.items():
            for x in range(max(0,focal[0]-radius), min(focal[0]+radius+1,100)):
                for y in range(max(0,focal[1]-radius), min(focal[1]+radius+1, 100)):
                    if((x==focal[0]-radius) or (x==focal[0]+radius) or
                        (y==focal[1]-radius) or (y==focal[1]+radius)): # go to the rectangle outer shell
                            # set lower bounds of probabilities - so the distribution generated could be closer to the animals
                            # distribution we need:
                            animal_prob = max(start_prob*(decay_factor**radius), min_probs[animal])
                            # cut probabilities if they exceed the number of animals in the distribution for the animal:
                            animal_prob = min(animals_distribution[animal] - total_animals_so_far[animal], animal_prob)
                            animals_grid[x][y][animal] = animal_prob
                            total_animals_so_far[animal] += animal_prob
                            if(sum(animals_grid[x][y].values()) > 1):
                                raise Exception("sum of probabilities in ({0}, {1}) is equal to {2}".format(x, y, sum(animals_grid[x][y].values())))
    if(total_animals_so_far != animals_distribution):
        print("heat map doesn't agree with the animals distribution.")
    return animals_grid

    # now its time to randomize the animals according to the distribution. for each rectangle - if the sum of probabilities
    # for animals in it exceeds one throw an informative exception so you will be able to tweak the parameters to be suitable
    # according to the rules (this could be handled by making focals more distant than each other or
    # increasing the decay factor)
    # in addition if you passed throught the board and couldn't allocate all animals on it too - again throw an informative
    # exception about it (for this you may want to decrease the decay factor, or making the focals closer to the board center)

