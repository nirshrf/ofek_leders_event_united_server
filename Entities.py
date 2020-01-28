# Module: Entities.py
class Adopter:
    def __init__(self, args):
        if len(args) == 3:
            self.name = args[0]
            if type(args[1]) == PetType:
                self.preferred = args[1]
            else:
                self.preferred = PetType(*args[1].values())
            self.secondpreferred = None
            self.valid = str(args[2]).lower()
        else:
            self.name = args[0]
            if type(args[1]) == PetType:
                self.preferred = args[1]
            else:
                self.preferred = PetType(*args[1].values())
            if type(args[2]) == PetType or args[2] is None:
                self.secondpreferred = args[2]
            else:
                self.secondpreferred = PetType(*args[2].values())
            self.valid = str(args[3]).lower()

    def for_mutation(self):
        if self.secondpreferred is None:
            return self.name, self.preferred.code, self.valid
        return self.name, self.preferred.code, self.secondpreferred.code, self.valid

    def __str__(self):
        return "\nAdopter{" + "\nname : " + str(self.name) + "\npreferred : " + str(self.preferred )+ \
               "\nSecond Preferred : " + str(self.secondpreferred) + "\n}"

    def __repr__(self):
        return "\nAdopter{" + "\nname : " + str(self.name) + "\npreferred : " + str(self.preferred )+ \
               "\nSecond Preferred : " + str(self.secondpreferred) + "\n}"


class Coordinate:
    def __init__(self, longitude, latitude):
        self.longitude = longitude
        self.latitude = latitude

    def __repr__(self):
        return "\nCoordinate{" + "\nLongitude : " + str(self.longitude) + "\nLatitude : " + str(self.longitude) + "\n}"

    def __str__(self):
        return "\nCoordinate{" + "\nLongitude : " + str(self.longitude) + "\nLatitude : " + str(self.longitude) + "\n}"


class Quadcopter:
    def __init__(self, id, name, launchtime, isfree, x, y):
        self.id = id
        self.name = name
        self.launchtime = launchtime
        self.isfree = isfree
        self.x = x
        self.y = y

    def __repr__(self):
        return "\nQuadcopter{" + "\nName : " + str(self.name) + "\n}"

    def __str__(self):
        return "\nQuadcopter{" + "\nName : " + str(self.name) + "\n}"


class PetType:
    def __init__(self, code, description):
        self.code = int(code)
        self.description = description

    def to_dictionary(self):
        return dict(code=self.code,
                    description=self.description)

    def __repr__(self):
        return "\nPetType{" + "\nCode : " + str(self.code) + "\nDescription : " + str(self.description) + "\n}"

    def __str__(self):
        return "\nPetType{" + "\nCode : " + str(self.code) + "\nDescription : " + str(self.description) + "\n}"


class History:
    def __init__(self, cell_x ,cell_y, petType, amount):
        self.cell_x = cell_x
        self.cell_y = cell_y
        if type(petType) == PetType:
            self.petType = petType
        else:
            self.petType = PetType(*petType.values())
        self.amount = amount

    def for_mutation(self):
        return self.cell_x, self.cell_y, self.petType.code, self.amount

    def __repr__(self):
        return "\nHistory{" + str(self.petType) + "\nAmount : " + str(self.amount) + "\n}"

    def __str__(self):
        return "\nHistory{" + str(self.petType) + "\nAmount : " + str(self.amount) + "\n}"


class GridCell:
    def __init__(self, args):
        self.x = args[0]
        self.y = args[1]
        self.lastPictureUrl = args[2]
        if type(args[3]) == PetType or args[3] is None:
            self.pet_type = args[3]
        else:
            self.pet_type = PetType(*args[3].values())

    def for_mutation(self):
        if self.pet_type is None:
            return self.x, self.y, self.lastPictureUrl, 0
        return self.x, self.y, self.lastPictureUrl, self.pet_type.code

    def __repr__(self):
        return "\nGridCell{" + "\nX : " + str(self.x) + "\nY : " + str(self.y) + str(self.pet_type) + "\n}"

    def __str__(self):
        return "\nGridCell{" + "\nX : " + str(self.x) + "\nY : " + str(self.y) + "\n}"


class EventStatus:
    def __init__(self, code, description):
        self.code = code
        self.description = description

    def __repr__(self):
        return "\nEventStatus{" + "\nCode : " + str(self.code) + "\nDescription : " + str(self.description) + "\n}"

    def __str__(self):
        return "\nEventStatus{" + "\nCode : " + str(self.code) + "\nDescription : " + str(self.description) + "\n}"


class Event:
    def __init__(self, quadcopter, grid_cell, event_time, event_status):
        if type(quadcopter) == Quadcopter:
            self.quadcopter = quadcopter
        else:
            self.quadcopter = Quadcopter(*quadcopter.values())
        self.grid_cell = grid_cell
        self.event_time = event_time
        if type(event_status) == EventStatus:
            self.event_status = event_status
        else:
            self.event_status = EventStatus(*event_status.values())

    def __repr__(self):
        return "\nEvent{" + "\nQuadcopter : " + str(self.quadcopter) + "\nEvent Status : " + str(self.event_status) + "\n}"

    def __str__(self):
        return "\nEvent{" + "\nQuadcopter : " + str(self.quadcopter) + "\nEvent Status : " + str(self.event_status) + "\n}"


class AdoptionStatus:
    def __init__(self, code, description):
        self.code = code
        self.description = description

    def __repr__(self):
        return "\nAdoptionStatus{" + "\nCode : " + str(self.code) + "\nDescription : " + str(self.description) + "\n}"

    def __str__(self):
        return "\nAdoptionStatus{" + "\nCode : " + str(self.code) + "\nDescription : " + str(self.description) + "\n}"


class Adoptee:
    def __init__(self, pet_type, x, y, image_before_url, image_after_url, adoption_status):
        if type(pet_type) == PetType:
            self.pet_type = pet_type
        else:
            self.pet_type = PetType(*pet_type.values())
        self.x = x
        self.y = y
        self.image_before_url = image_before_url
        self.image_after_url = image_after_url
        if type(adoption_status) == AdoptionStatus:
            self.adoption_status = adoption_status
        else:
            self.adoption_status = AdoptionStatus(*adoption_status.values())

    def for_mutation(self):
        return self.pet_type.code, self.x, self.y, self.image_before_url, self.image_after_url, self.adoption_status.code

    def __repr__(self):
        return "\nAdoptee{" + "\nPet Type : " + str(self.pet_type) + "\nAdoption Status : " + str(self.adoption_status) + "\n}"

    def __str__(self):
        return "\nAdoptee{" + "\nPet Type : " + str(self.pet_type) + "\nAdoption Status : " + str(self.adoption_status) + "\n}"


class AiStatus:
    def __init__(self, drone_AI, pets_AI, adoption_AI, bda_AI):
        self.drone_AI = drone_AI
        self.pets_AI = pets_AI
        self.adoption_AI = adoption_AI
        self.bda_AI = bda_AI

    def __repr__(self):
        return "\nAiStatus{" + "\ndrone_AI : " + str(self.drone_AI) + "\npets_AI : " + str(self.pets_AI) + "\nadoption_AI : " + str(self.adoption_AI) + "\nbda_AI : " + str(self.bda_AI) + "\n}"

    def __str__(self):
        return "\nAiStatus{" + "\ndrone_AI : " + str(self.drone_AI) + "\npets_AI : " + str(self.pets_AI) + "\nadoption_AI : " + str(self.adoption_AI) + "\nbda_AI : " + str(self.bda_AI) + "\n}"


class Plot:
    def __init__(self,cell_x, cell_y, timestamp, x, y, z):
        self.cell_x = cell_x
        self.cell_y = cell_y
        self.timestamp = timestamp
        self.x = x
        self.y = y
        self.z = z

    def to_tuple(self):
        return self.timestamp, self.x, self.y, self.z

    def for_mutation(self):
        return self.cell_x, self.cell_y, self.timestamp, self.x, self.y, self.z

    def __repr__(self):
        return "\nPlot{" + "\nTime : " + str(self.timestamp) + "\nx : " + str(self.x) + "\ny : " + str(self.y) + "\nz : " + str(self.z) + "\n}"

    def __str__(self):
        return "\nPlot{" + "\nTime : " + str(self.timestamp) + "\nx : " + str(self.x) + "\ny : " + str(self.y) + "\nz : " + str(self.z) + "\n}"


class Heatmap:
    def __init__(self, dog_percentage, cat_percentage, rabbit_percentage, parrot_percentage):
        self.dog_percentage = dog_percentage
        self.cat_percentage = cat_percentage
        self.rabbit_percentage = rabbit_percentage
        self.parrot_percentage = parrot_percentage

    def to_tuple(self):
        return self.dog_percentage, self.cat_percentage, self.rabbit_percentage, self.parrot_percentage

    def to_dictionary(self):
        return dict(dog=self.dog_percentage,
                    cat=self.cat_percentage,
                    rabbit=self.rabbit_percentage,
                    parrot=self.parrot_percentage)

    def __repr__(self):
        return "\nHeatmap{" + "\nDog : " + str(self.dog_percentage) + "\nCat : " + str(self.cat_percentage) + "\nRabbit : " + str(self.rabbit_percentage) + "\nParrot : " + str(self.parrot_percentage) + "\n}"

    def __str__(self):
        return "\nHeatmap{" + "\nDog : " + str(self.dog_percentage) + "\nCat : " + str(self.cat_percentage) + "\nRabbit : " + str(self.rabbit_percentage) + "\nParrot : " + str(self.parrot_percentage) + "\n}"


