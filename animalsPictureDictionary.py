import json
import random
animals_json = open("Data/animalsData.json")
json_content = animals_json.read()
animals_dictionary = json.loads(json_content)


def get_animal_picture_url(animal):
    if animal in animals_dictionary.keys():
        return random.sample(animals_dictionary[animal], 1)[0]
    raise KeyError
