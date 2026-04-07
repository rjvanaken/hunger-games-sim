from enum import Enum
from config import BOMB_HALF_DAMAGE


class Intervention:

    class Type(Enum):
        HAZARD = 2
        BOMB = 4
        # wall is not an intervention, the act just sets things to 0 since it stays that way for rest of games


    def __init__(self, type, positions=[], damage=None, pos=None):
        self.type = type
        self.positions = positions
        self.damage = damage
        self.isDeployed = False
        self.segment = None
        self.wasDeployedToday = False
        self.day_deployed = None
        self.pos = pos
        

