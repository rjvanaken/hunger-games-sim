from enum import Enum


class Resource:

    class Type(Enum):
        WATER_SOURCE = 1
        WATER_CONTAINER = 2
        FOOD = 3
        MEDICAL = 4
        WEAPON = 5
        BACKPACK_SMALL = 6
        BACKPACK_LARGE = 7


    def __init__(self, id, pos, type, value=1):
        self.id = id
        self.value = value
        self.pos = pos
        self.type = type
        self.isTaken = False

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, value):
        self._pos = value


    def addResource(self, pos, type, list, value=1):
        resource = Resource(self.next_resource_id, pos, type)
        list.append(resource)
        self.next_resource_id += 1

        # how do I pick up backpack and pick it up