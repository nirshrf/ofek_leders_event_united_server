
#Module: Entities.py


class Adopter:

    def __init__(self, id=None, name=None, preferred=None, secondpreferred=None):
        self.id = id
        self.name = name
        self.preferred = preferred
        self.secondpreferred = secondpreferred

    def __str__(self):
        return "id : " + self.id + "name : " + self.name + "preferred : " + self.preferred + "Second Preferred : " + self.secondpreferred

    def __repr__(self):
        return "id : " + self.id + "name : " + self.name + "preferred : " + self.preferred + "Second Preferred : " + self.secondpreferred

