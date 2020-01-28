from Entities import Adopter
from petTypeDictionary import get_pet_type
from faker import Faker
from generations.generate_adopter_request import generate_adopter_request


def generate_adopters(adopter_number):
    fake = Faker(['en_US', 'en_CA'])
    adopters = []
    for adopter in range(adopter_number):
        adopter_requests = generate_adopter_request()
        if len(adopter_requests) == 2:
            adopters.append(Adopter([fake.name(), get_pet_type(adopter_requests[0]), get_pet_type(adopter_requests[1]), True]))
        else:
            adopters.append(Adopter([fake.name(), get_pet_type(adopter_requests[0]), True]))
    return adopters
