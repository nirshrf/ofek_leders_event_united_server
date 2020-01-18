from Entities import Adopter
from Data.petTypeDictionary import get_pet_type
from faker import Faker
from generations.generate_adopter_request import generate_adopter_request


def generate_adopters(adopter_number):
    fake = Faker(['en_US', 'en_CA'])
    adopters = []
    for adopter in range(1, adopter_number+1):
        adopter_requests = generate_adopter_request(2)
        adopters.append(Adopter(adopter, fake.name(), get_pet_type(adopter_requests[0]), get_pet_type(adopter_requests[1]), True))
    return adopters
