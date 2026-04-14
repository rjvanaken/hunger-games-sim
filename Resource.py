"""
Resource.py - defines the Resource class
Resources are dispersed around the arena and can be interacted with under appropriate conditions

"""

from enum import Enum


class Resource:

    """
    Represents the resources in the arena. Resource type is displayed in the arena and determines how the tribute can
    interact with it in its action space.
    
    """

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
        self.value = value # value representing the quality of a resource or weapon. Determines backpack capacity and weapon level
        self.pos = pos
        self.type = type
        self.isTaken = False

    @property
    def pos(self):
        """Grid position of the resource as a (row, col) tuple, or None if removed from arena."""
        return self._pos

    @pos.setter
    def pos(self, value):
        """Sets the grid position of the resource."""
        self._pos = value


    def addResource(self, pos, type, list, value=1):

        """
        Creates a new resource instance and adds it to the appropriate list.
        Used in creation of cornucopia for the arena
        """
        
        resource = Resource(self.next_resource_id, pos, type)
        list.append(resource)
        self.next_resource_id += 1

