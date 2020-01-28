from graphql_handler.graphqlHandler import GraphQLRequests
from Data.app_properties import JAVA_server_url

graph_handler = GraphQLRequests(JAVA_server_url)
pet_type_dictionary = {}
pet_types = graph_handler.import_pet_types()
for pet_type in pet_types:
    pet_type_dictionary[pet_type.description] = pet_type


def get_pet_type(pet_type):
    if pet_type in pet_type_dictionary.keys():
        return pet_type_dictionary[pet_type]
    elif pet_type is None or pet_type == "none":
        return
    raise KeyError(pet_type)
