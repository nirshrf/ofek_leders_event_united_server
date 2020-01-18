from Entities import PetType

pet_type_dictionary = dict(none=PetType(0, 0, 'none'),
                           dog=PetType(1, 1, 'dog'),
                           cat=PetType(2, 2, 'cat'),
                           rabbit=PetType(3, 3, 'rabbit'),
                           parrot=PetType(4, 4, 'parrot'))


def get_pet_type(pet_type):
    if pet_type in pet_type_dictionary.keys():
        return pet_type_dictionary[pet_type]
    raise KeyError
