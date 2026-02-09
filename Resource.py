from enum import Enum


class Resource:

    class Type(Enum):
        WATER_SOURCE = 0
        FOOD_SOURCE = 1
        WATER_CONTAINER = 2
        FOOD = 3
        MEDICAL = 4
        WEAPON = 5
        BACKPACK_SMALL = 6
        BACKPACK_LARGE = 7


    def __init__(self, id, pos, type, value=None):
        self.id = id
        self.value = value
        self.pos = pos
        self.type = type


    def addResource(self, pos, type, list, value=None):
        resource = Resource(self.next_resource_id, pos, type)
        list.append(resource)
        self.next_resource_id += 1

        # how do I pick up backpack and pick it up