from graphql_handler.graphqlHandler import GraphQLRequests
from Data.app_properties import JAVA_server_url
from Entities import PetType

graph_handler = GraphQLRequests(JAVA_server_url)
cat = PetType(1, "cat")
dog = PetType(2, "dog")
parrot = PetType(3, "parrot")
rabbit = PetType(4, "rabbit")
pet_type_dictionary = dict(cat=cat, dog=dog, parrot=parrot, rabbit=rabbit)


def get_pet_type(pet_type):
    if pet_type in pet_type_dictionary.keys():
        return pet_type_dictionary[pet_type]
    elif pet_type is None or pet_type == "none":
        return
    raise KeyError(pet_type)
