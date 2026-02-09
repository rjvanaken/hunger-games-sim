# Constants
WATER_VALUE = 6
FOOD_VALUE = 30
MEDICAL_VALUE = 50

class Tribute:
    def __init__(self, id, pos):
        # self.strength = strength #num
        # self.pos = pos # set {}
        # self.inventory = 0
        # self.maxWeight = 0 # certain multiplier based on strength?
        self.pos = pos
        self.id = id
        self.letter = chr(65 + id)
        self.district = (id // 2) + 1
        self.health = 100
        self.thirst = 100
        self.hunger = 100
        self.water_supply = 0
        self.max_water = 0
        self.food = 0
        self.medical = 0
        self.capacity = 2
        self.strength = 0
        self.inventory = 0
        self.weapon_value = 0

        if id % 2 == 0:
            self.gender = 'male'
        else:
            self.gender = 'female'
        

    def generateStrength():
        # use randomization based on district to get their strength
        pass




# GAME ACTIONS

    def pickUpResource(self, resource):
    # need to have all pickups in case they get things from sponsors
    # TODO factor in sponsor logic eventually
        if self.inventory == self.capacity:
            return "storage capacity reached. cannot pick up new item"

        elif resource.type == 0:
            self.water_supply = self.max_water
            self.thirst = 100
        
        elif resource.type == 1:
            self.food += 1
            self.inventory += 1
        
        elif resource.type == 2:
            self.max_water += resource.value
            self.inventory += 1

        elif resource.type == 3:
            self.food += 1
            self.inventory += 1

        elif resource.type == 4:
            self.medical += 1
            self.inventory += 1
        
        elif resource.type == 5:
            self.inventory += 1
            if resource.value > self.weapon_value:
                self.weapon_value = resource.value
                # update strength to difference when changing best weapon
                self.strength += resource.value - self.weapon_value

        # TODO: confirm and adjust backpack sizes in testing
        elif resource.type == 6:
            self.capacity += 5
            self.food += 2
            self.max_water += 15
            self.inventory += 3
            
        elif resource.type == 6:
            self.capacity += 10
            self.food += 3
            self.medical += 1
            self.max_water += 15
            self.inventory += 5

        else:
            return "debug - item error"
        

    def eatFood(self):
        if self.hunger != 100:
            self.food -= 1
            self.inventory -= 1
            if self.hunger + FOOD_VALUE > 100:
                self.hunger == 100
            else:
                self.hunger += FOOD_VALUE    

    def drinkWater(self):
        # TODO: confirm and adjust water unit value as needed in testing
        if self.thirst != 100:
            self.water_supply -= 1
            if self.thirst + WATER_VALUE > 100:
                self.thirst == 100
            else:
                self.thirst += WATER_VALUE

    def useMedical(self):
        if self.health != 100:
            self.medical -= 1
            self.inventory -= 1
            if self.health + MEDICAL_VALUE > 100:
                self.health == 100
            else:
                self.thirst += MEDICAL_VALUE
    
    
    # movement function logic is temporary so they can move
    # TODO: update so they navigate in that general direction once tribute agent is working

    def move(self, pos):
        self.pos = pos
            
    