# Module: Entities.py

JSON_dictionary = dict(Quadcopter='{id, name, launchtime, isfree, x, y}',
                       PetType='{id, code, description}',
                       EventStatus='{id, code, description}',
                       Coordinate='{longitude, latitude}',
                       AdoptionStatus='{id, code, description}',
                       History='{id, petType{id, code, description}, amount}',
                       GridCell='{id, x, y, lastPictureUrl, history{id, petType{id, code, description}, amount}}',
                       Adopter='{id, name, preferred{id, code, description}, secondpreferred{id, code, description}, isvalid}',
                       Event='{id, quadcopter{id, name, launchtime, isfree, x, y}, gridCell{id, x, y, lastPictureUrl, history{id, petType{id, code, description}, amount}}, eventTime, eventStatus{id, code, description}}',
                       Adoptee='{id, petType{id, code, description}, x, y, imageBeforeURL, imageAfterURL, adoptionStatus{id, code, description}}',
                       AiStatus='{toggleDroneAI, togglePetsAI, toggleAdoptionAI, toggleBdaAI}',
                       Plot='{timestamp, x, y, z}')


class Adopter:
    def __init__(self, id=None, name=None, preferred=None, secondpreferred=None, valid=None):
        self.id = id
        self.name = name
        if type(preferred) == PetType:
            self.preferred = preferred
        else:
            self.preferred = PetType(*preferred.values())
        if type(secondpreferred) == PetType:
            self.secondpreferred = secondpreferred
        else:
            self.secondpreferred = PetType(*secondpreferred.values())
        self.valid = valid

    def to_dictionary(self):
        return {self.id, [self.preferred.description, self.secondpreferred.description]}

    def __str__(self):
        return "Adopter{" + "\nid : " + str(self.id) + "\nname : " + str(self.name) + "\npreferred : " + str(self.preferred )+ \
               "\nSecond Preferred : " + str(self.secondpreferred) + "}\n"

    def __repr__(self):
        return "Adopter{" + "\nid : " + str(self.id) + "\nname : " + str(self.name) + "\npreferred : " + str(self.preferred )+ \
               "\nSecond Preferred : " + str(self.secondpreferred) + "}\n"


class Coordinate:
    def __init__(self, longitude, latitude):
        self.longitude = longitude
        self.latitude = latitude

    def __repr__(self):
        return "Coordinate{" + "\nLongitude : " + str(self.longitude) + "\nLatitude : " + str(self.longitude) + "}\n"

    def __str__(self):
        return "Coordinate{" + "\nLongitude : " + str(self.longitude) + "\nLatitude : " + str(self.longitude) + "}\n"


class Quadcopter:
    def __init__(self, id,name, launchtime, isfree, x, y):
        self.id = id
        self.name = name
        self.launchtime = launchtime
        self.isfree = isfree
        self.x = x
        self.y = y

    def to_tuple(self):
        return self.id, self.x, self.y

    def __repr__(self):
        return "Quadcopter{" + "\nId : " + str(self.id) + "\nName : " + str(self.name) + "}\n"

    def __str__(self):
        return "Quadcopter{" + "\nId : " + str(self.id) + "\nName : " + str(self.name) + "}\n"


class PetType:
    def __init__(self, id, code, description):
        self.id = id
        self.code = code
        self.description = description

    def __repr__(self):
        return "PetType{" + "\nId : " + str(self.id) + "\nCode : " + str(self.code) + "\nDescription : " + str(self.description) + "}\n"

    def __str__(self):
        return "PetType{" + "\nId : " + str(self.id) + "\nCode : " + str(self.code) + "\nDescription : " + str(self.description) + "}\n"


class History:
    def __init__(self, id, petType, amount):
        self.id = id
        if type(petType) == PetType:
            self.petType = petType
        else:
            self.petType = PetType(*petType.values())
        self.amount = amount

    def __repr__(self):
        return "History{" + "\nId : " + str(self.id) + "\nType : " + str(self.petType) + "\nAmount : " + str(self.amount) + "}\n"

    def __str__(self):
        return "History{" + "\nId : " + str(self.id) + "\nType : " + str(self.petType) + "\nAmount : " + str(self.amount) + "}\n"


class GridCell:
    def __init__(self, id, x, y, lastPictureUrl, history):
        self.id = id
        self.x = x
        self.y = y
        self.lastPictureUrl = lastPictureUrl
        if type(history[0]) == History:
            self.history = history
        else:
            self.history = [History(*h.values()) for h in history]

    def __repr__(self):
        return "GridCell{" + "\nX : " + str(self.x) + "\nY : " + str(self.y) + "\nHistory : " + str(self.history) + "}\n"

    def __str__(self):
        return "GridCell{" + "\nX : " + str(self.x) + "\nY : " + str(self.y) + "\nHistory : " + str(self.history) + "}\n"


class EventStatus:
    def __init__(self, id, code, description):
        self.id = id
        self.code = code
        self.description = description

    def __repr__(self):
        return "EventStatus{" + "\nId : " + str(self.id) + "\nCode : " + str(self.code) + "\nDescription : " + str(self.description) + "}\n"

    def __str__(self):
        return "EventStatus{" + "\nId : " + str(self.id) + "\nCode : " + str(self.code) + "\nDescription : " + str(self.description) + "}\n"


class Event:
    def __init__(self, id, quadcopter, gridCell, eventTime, eventStatus):
        self.id = id
        if type(quadcopter) == Quadcopter:
            self.quadcopter = quadcopter
        else:
            self.quadcopter = Quadcopter(*quadcopter.values())
        self.gridCell = gridCell
        self.eventTime = eventTime
        if type(eventStatus) == EventStatus:
            self.eventStatus = eventStatus
        else:
            self.eventStatus = EventStatus(*eventStatus.values())

    def __repr__(self):
        return "Event{" + "\nId : " + str(self.id) + "\nQuadcopter : " + str(self.quadcopter) + "\nEvent Status : " + str(self.eventStatus) + "}\n"

    def __str__(self):
        return "Event{" + "\nId : " + str(self.id) + "\nQuadcopter : " + str(self.quadcopter) + "\nEvent Status : " + str(self.eventStatus) + "}\n"


class AdoptionStatus:
    def __init__(self, id, code, description):
        self.id = id
        self.code = code
        self.description = description

    def __repr__(self):
        return "AdoptionStatus{" + "\nId : " + str(self.id) + "\nCode : " + str(self.code) + "\nDescription : " + str(self.description) + "}\n"

    def __str__(self):
        return "AdoptionStatus{" + "\nId : " + str(self.id) + "\nCode : " + str(self.code) + "\nDescription : " + str(self.description) + "}\n"


class Adoptee:
    def __init__(self, id, petType, x, y, imageBeforeURL, imageAfterURL, adoptionStatus):
        self.id = id
        if type(petType) == PetType:
            self.petType = petType
        else:
            self.petType = PetType(*petType.values())
        self.x = x
        self.y = y
        self.imageBeforeURL = imageBeforeURL
        self.imageAfterURL = imageAfterURL
        if type(adoptionStatus) == AdoptionStatus:
            self.adoptionStatus = adoptionStatus
        else:
            self.adoptionStatus = AdoptionStatus(*adoptionStatus.values())

    def __repr__(self):
        return "Adoptee{" + "\nId : " + str(self.id) + "\nPet Type : " + str(self.petType) + "\nAdoption Status : " + str(self.adoptionStatus) + "}\n"

    def __str__(self):
        return "Adoptee{" + "\nId : " + str(self.id) + "\nPet Type : " + str(self.petType) + "\nAdoption Status : " + str(self.adoptionStatus) + "}\n"


class AiStatus:
    def __init__(self, drone_AI, pets_AI, adoption_AI, bda_AI):
        self.drone_AI = drone_AI
        self.pets_AI = pets_AI
        self.adoption_AI = adoption_AI
        self.bda_AI = bda_AI

    def __repr__(self):
        return "AiStatus{" + "\ndrone_AI : " + str(self.drone_AI) + "\npets_AI : " + str(self.pets_AI) + "\nadoption_AI : " + str(self.adoption_AI) + "\nbda_AI : " + str(self.bda_AI) + "}\n"

    def __str__(self):
        return "AiStatus{" + "\ndrone_AI : " + str(self.drone_AI) + "\npets_AI : " + str(self.pets_AI) + "\nadoption_AI : " + str(self.adoption_AI) + "\nbda_AI : " + str(self.bda_AI) + "}\n"


class Plot:
    def __init__(self, timestamp, x, y, z):
        self.timestamp = timestamp
        self.x = x
        self.y = y
        self.z = z

    def to_tuple(self):
        return self.timestamp, self.x, self.y, self.z

    def __repr__(self):
        return "Plot{" + "\nTime : " + str(self.timestamp) + "\nx : " + str(self.x) + "\ny : " + str(self.y) + "\nz : " + str(self.z) + "}\n"

    def __str__(self):
        return "Plot{" + "\nTime : " + str(self.timestamp) + "\nx : " + str(self.x) + "\ny : " + str(self.y) + "\nz : " + str(self.z) + "}\n"


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
        return "Heatmap{" + "\nDog : " + str(self.dog_percentage) + "\nCat : " + str(self.cat_percentage) + "\nRabbit : " + str(self.rabbit_percentage) + "\nParrot : " + str(self.parrot_percentage) + "}\n"

    def __str__(self):
        return "Heatmap{" + "\nDog : " + str(self.dog_percentage) + "\nCat : " + str(self.cat_percentage) + "\nRabbit : " + str(self.rabbit_percentage) + "\nParrot : " + str(self.parrot_percentage) + "}\n"


