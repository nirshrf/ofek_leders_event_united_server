# Module: Entities.py


class Adopter:
    def __init__(self, id=None, name=None, preferred=None, secondpreferred=None):
        self.id = id
        self.name = name
        self.preferred = PetType(*preferred.values())
        self.secondpreferred = PetType(*secondpreferred.values())

    def __str__(self):
        return "\nid : " + self.id + "\nname : " + str(self.name) + "\npreferred : " + str(self.preferred )+ \
               "\nSecond Preferred : " + str(self.secondpreferred) + "\n"

    def __repr__(self):
        return "\nid : " + self.id + "\nname : " + self.name + "\npreferred : " + str(self.preferred )+ \
               "\nSecond Preferred : " + str(self.secondpreferred) + "\n"


class Coordinate:
    def __init__(self, longitude, latitude):
        self.longitude = longitude
        self.latitude = latitude

    def __repr__(self):
        return "\nLongitude : " + str(self.longitude) + "\nLatitude : " + str(self.longitude) + "\n"

    def __str__(self):
        return "\nLongitude : " + str(self.longitude) + "\nLatitude : " + str(self.longitude) + "\n"


class Quadcopter:
    def __init__(self, id,name, launchtime, isfree, x, y):
        self.id = id
        self.name = name
        self.launchtime = launchtime
        self.isfree = isfree
        self.x = x
        self.y = y

    def __repr__(self):
        return "\nId : " + str(self.id) + "\nName : " + str(self.name)

    def __str__(self):
        return "\nId : " + str(self.id) + "\nName : " + str(self.name) + "\n"


class PetType:
    def __init__(self, id, code, description):
        self.id = id
        self.code = code
        self.description = description

    def __repr__(self):
        return "\nId : " + str(self.id) + "\nCode : " + str(self.code) + "\nDescription : " + str(self.description)

    def __str__(self):
        return "\nId : " + str(self.id) + "\nCode : " + str(self.code) + "\nDescription : " + str(self.description)


class History:
    def __init__(self, id, petType, amount):
        self.id = id
        self.petType = PetType(*petType)
        self.amount = amount

    def __repr__(self):
        return "\nId : " + str(self.id) + "\nType : " + str(self.petType) + "\nAmount : " + str(self.amount)

    def __str__(self):
        return "\nId : " + str(self.id) + "\nType : " + str(self.petType) + "\nAmount : " + str(self.amount)


class GridCell:
    def __init__(self, id, x, y, lastPictureUrl, history):
        self.id = id
        self.x = x
        self.y = y
        self.lastPictureUrl = lastPictureUrl
        self.history = [History(*h.values()) for h in history]

    def __repr__(self):
        return "\nX : " + str(self.x) + "\nY : " + str(self.y) + "\nHistory : " + str(self.history)

    def __str__(self):
        return "\nX : " + str(self.x) + "\nY : " + str(self.y) + "\nHistory : " + str(self.history)


