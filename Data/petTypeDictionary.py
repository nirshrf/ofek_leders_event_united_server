from graphqlHandler import GraphQLRequests
from main import JAVA_server_url
from Entities import PetType

graph_handler = GraphQLRequests(JAVA_server_url)
pet_type_dictionary = {}
pet_types = graph_handler.import_pet_types()
for pet_type in pet_types:
    pet_type_dictionary[pet_type.description] = pet_type


def get_pet_type(pet_type):
    if pet_type in pet_type_dictionary.keys():
        return pet_type_dictionary[pet_type]
    raise KeyError(pet_type)
