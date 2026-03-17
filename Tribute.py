import random
import math
from Resource import Resource

# Constants
from config import *
class Tribute:
    def __init__(self, id, pos):
        self.pos = pos
        self.id = id

        if id % 2 == 0:
            self.gender = 'male'
        else:
            self.gender = 'female'

        self.letter = chr(65 + id)
        self.district = (id // 2) + 1
        self.age = self.getRandomAge()
        self.hunting_skill = self.getHuntingSkill()
        self.base_strength = self.getRandomStrength()
        self.strength = self.base_strength
        self.max_strength = self.strength
        self.max_speed = self.getRandomSpeed()
        self.speed = self.max_speed
        self.health = 100
        self.thirst = 100
        self.hunger = 100
        self.water_supply = 0
        self.max_water = 0
        self.capacity = 2
        self.inventory = []
        self.weapon_value = 0
        self.isAlive = True
        self.isAsleep = False
        self.isWalking = False
        self.arenaKnowledge = []
        self.segment = None
        
    @property
    def health(self):
        return self._health

    @health.setter
    def health(self, value):
        self._health = value
        if self._health <= 0:
            self._health = 0
            self.isAlive = False

        # need to figure out a tribute success heuristic
        # somehow need to figure out how strength will be impacted by low health and how that will change, etc.

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, value):
        self._pos = value
        # clear old pos in grid
        # add new pos to grid
        # set new self.pos afterwards

        # somehow need to figure out how strength will be impacted by low health and how that will change, etc.

      

    def getRandomStrength(self):

        min, max = STRENGTH_BY_AGE[self.age]
        raw_strength = random.randint(min, max)

        if self.district == 1 or self.district == 2 or self.district == 4:
            raw_strength += CAREER_BONUS
        if self.gender == 'male':
            raw_strength += MALE_BONUS

        return raw_strength
    

    def getRandomSpeed(self):
        return random.randint(BASE_SPEED, BASE_SPEED + 2)
        
    def getHuntingSkill(self):
        return random.randint(1, 100)
        

    def getRandomAge(self):
        return random.randint(12, 18)


    def updateStatsBeforeTurn(self):
        self.hunger -= HUNGER_DECAY
        self.thirst -= THIRST_DECAY
        self.hunger = max(0, self.hunger)
        self.thirst = max(0, self.thirst)
        # subtract full penalty if under 0, partial if only below threshold
        if self.hunger <= 0:
            self.health -= HUNGER_HEALTH_PENALTY
        elif self.hunger <= HUNGER_WARNING_THRESHOLD:
            self.health -= HUNGER_WARNING_PENALTY
        
        # subtract full penalty if under 0, partial if only below threshold
        if self.thirst <= 0:
            self.health -= THIRST_HEALTH_PENALTY
        elif self.thirst <= THIRST_WARNING_THRESHOLD:
            self.health -= THIRST_WARNING_PENALTY

        self.strength = self.base_strength * (self.health / 100)
        

    def getFood(self):
        food = 0
        for item in self.inventory:
            if item.type.value == 3:
                food += 1
        return food
    
    def getMedical(self):
        medical = 0
        for item in self.inventory:
            if item.type.value == 4:
                medical += 1
        return medical

# GAME ACTIONS

    def pickUpResource(self, resource):
    # need to have all pickups in case they get things from sponsors
    # TODO factor in sponsor logic eventually


        if resource.type == Resource.Type.BACKPACK_SMALL:
            self.capacity += 5
            canteen = Resource(None, None, Resource.Type(2))
            self.inventory.append(canteen)
            for i in range(2):
                food = Resource(None, None, Resource.Type(3))
                self.inventory.append(food)
            self.max_water += CANTEEN_VALUE
            return True
        
        elif resource.type == Resource.Type.BACKPACK_LARGE:
            self.capacity += 10
            canteen = Resource(None, None, Resource.Type(2))
            medical = Resource(None, None, Resource.Type(4))
            self.inventory.append(canteen)
            self.inventory.append(medical)
            for i in range(3):
                food = Resource(None, None, Resource.Type(3))
                self.inventory.append(food)
            self.max_water += CANTEEN_VALUE
            return True
        
        elif len(self.inventory) == self.capacity and resource.type != Resource.Type.WATER_SOURCE:
            print("storage capacity reached. cannot pick up new item")
            return False
        
        
        elif resource.type == Resource.Type.WATER_CONTAINER:
            self.max_water += CANTEEN_VALUE
            self.inventory.append(resource)
            return True

        elif resource.type == Resource.Type.FOOD:
            self.inventory.append(resource)
            return True

        elif resource.type == Resource.Type.MEDICAL:
            self.inventory.append(resource)
            return True
        
        elif resource.type == Resource.Type.WEAPON:
            has_weapon = False
            for item in self.inventory:
                if item.type == Resource.Type.WEAPON:
                    if item.value < resource.value:
                        self.inventory.append(resource)
                        self.inventory.remove(item)
                        self.strength = self.base_strength + resource.value
                        self.weapon_value = resource.value
                        has_weapon = True
                        break
            if not has_weapon:
                self.inventory.append(resource)
                self.weapon_value = resource.value
                self.strength = self.base_strength + resource.value
                

            # return true either way, checking item still counts for turn
            return True

        else:
            return "debug - item error"
        

    def eatFood(self):
        for item in self.inventory:
            if item.type.value == 3:
                self.inventory.remove(item)
                break
        self.hunger = min(100, self.hunger + FOOD_VALUE) 
                

    def drinkWater(self):
        # TODO: confirm and adjust water unit value as needed in testing
        self.water_supply -= 1
        self.thirst = min(100, self.thirst + WATER_VALUE)

    def useMedical(self):
        for item in self.inventory:
            if item.type.value == 4:
                self.inventory.remove(item)
                break
        self.health = min(100, self.health + MEDICAL_VALUE) 

    def refillWater(self):
        self.water_supply = self.max_water
        self.thirst = 100
    
    # movement function logic is temporary so they can move
    # TODO: update so they navigate in that general direction once tribute agent is working

    def move(self, row, col):
        self.pos = ((row, col))

    def singleMove(self, direction):
        # handle logic is here instead simply because otherwise we would be checking this twice

        if direction.lower() == 'u' or direction.lower() == 'up':
            new_pos = ((self.pos[0] - 1, self.pos[1])) 
        elif direction.lower() == 'd' or direction.lower() == 'down':
            new_pos = ((self.pos[0] + 1, self.pos[1]))
        elif direction.lower() == 'l' or direction.lower() == 'left':
            new_pos = ((self.pos[0], self.pos[1] - 1))
        elif direction.lower() == 'r' or direction.lower() == 'right':
            new_pos = ((self.pos[0], self.pos[1] + 1))

        if self.canMoveTo(new_pos):
            self.pos = new_pos

        

    def canMoveTo(self, pos):
        if int(self.arenaKnowledge[pos[0]][pos[1]]) not in [8, 1]:
            return True


    def attack(self, target):
        difference = max(target.strength, self.strength) - min(target.strength, self.strength)
        if self.strength > target.strength:
            attacker = (50 + difference) / 100
        else:
            attacker = (50 - difference) / 100

        if random.random() >= attacker:
            target.health -= (BASE_DAMAGE + int(math.ceil((self.strength * DAMAGE_MULTIPLIER))))
            print("Tribute wins attack, target health decreased")
        else:
            self.health -= (BASE_DAMAGE + int(math.ceil((target.strength * DAMAGE_MULTIPLIER))))
            print("Target wins attack, tribute health decreased")

    def sleep(self, num_turns):
        self.isAsleep = True
        


    # def act - implement AI tribute logic here - begin games

    