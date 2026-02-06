

class Tribute:
    def __init__(self, id, pos):
        # self.strength = strength #num
        # self.pos = pos # set {}
        # self.inventory = 0
        # self.maxWeight = 0 # certain multiplier based on strength?
        self.pos = pos
        self.id = id
        self.letter = chr(65 + id)
        self.health = 100
        self.thirst = 100
        self.hunger = 100
        self.water_supply = 0
        self.max_water = 0
        self.storage = 2
        self.district = (id // 2) + 1
        self.strength = 0

        if id % 2 != 0:
            self.gender = 'male'
        else:
            self.gender = 'female'
        

    def generateStrength():
        # use randomization based on district to get their strength
        pass



