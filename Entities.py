#Module: Entities.py

class Adopter:

    def __init__(self, id=None, name=None, preferred=None, secondpreferred=None):
        self.id = id
        self.name = name
        self.preferred = preferred
        self.secondpreferred = secondpreferred

    def __str__(self):
        return "\nid : " + self.id + "\nname : " + self.name + "\npreferred : " + self.preferred + "\nSecond Preferred : " + self.secondpreferred + "\n"

    def __repr__(self):
        return "\nid : " + self.id + "\nname : " + self.name + "\npreferred : " + self.preferred + "\nSecond Preferred : " + self.secondpreferred + "\n"


class Coordinate:
    def __init__(self, longitude, latitude):
        self.longitude = longitude
        self.latitude = latitude

    def __repr__(self):
        return "\nLongitude : " + str(self.longitude) + "\nLatitude : " + str(self.longitude) + "\n"

    def __str__(self):
        return "\nLongitude : " + str(self.longitude) + "\nLatitude : " + str(self.longitude) + "\n"


