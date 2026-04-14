from enum import Enum
from config import BOMB_HALF_DAMAGE

"""
Intervention.py - defines the Intervention class, representing gamemaker interventions
(hazards and bombs) that can be deployed into the arena during a game.
"""

class Intervention:

    """
    Represents a gamemaker intervention event such as a hazard or bomb.
    Tracks its type, affected positions, damage, and deployment state.
    """

    class Type(Enum):
        HAZARD = 2
        BOMB = 4


    def __init__(self, type, positions=[], damage=None, pos=None):
        self.type = type
        # list of grid positions affected by this intervention
        self.positions = positions
        self.damage = damage
        self.isDeployed = False
        self.segment = None
        self.wasDeployedToday = False
        self.day_deployed = None
        self.pos = pos
        

