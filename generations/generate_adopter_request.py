import random


def generate_adopter_request():
    """
    the function will generate a request for adopter, i.e. an animal list of size between 1 and 2.
    each animal has 25% chance to be inside the list.
    70% chance for adopters list of size 1, 30% chance for adopters list of size 2
    """
    animals_list = ["dog", "cat", "rabbit", "parrot"]
    if(random.random() < 0.7):
        return random.sample(animals_list, 1)
    else:
        return random.sample(animals_list, 2)