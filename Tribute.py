import random
import math
from Resource import Resource
import gameplay_handler as gh

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
        self.arenaKnowledge = []
        self.segment = None
        self.num_kills = 0
        self.turn_count = 0
        self.last_move = None
        
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
        self.strength = math.ceil((self.base_strength + self.weapon_value) * (self.health / 100))
        

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
            if self.capacity <= 2:
                self.capacity += SMALL_CAPACITY
                canteen = Resource(None, None, Resource.Type(2))
                self.inventory.append(canteen)
                for i in range(SMALL_BACKPACK_FOOD):
                    food = Resource(None, None, Resource.Type(3))
                    self.inventory.append(food)
                for i in range(SMALL_BACKPACK_MED):
                    medical = Resource(None, None, Resource.Type(4))
                    self.inventory.append(medical)
                self.max_water += CANTEEN_VALUE
                return True
            return False
        
        elif resource.type == Resource.Type.BACKPACK_LARGE:
            if self.capacity <= 2:
                self.capacity += LARGE_CAPACITY
                canteen = Resource(None, None, Resource.Type(2))
                self.inventory.append(canteen)
                for i in range(LARGE_BACKPACK_MED):
                    medical = Resource(None, None, Resource.Type(4))
                    self.inventory.append(medical)
                for i in range(LARGE_BACKPACK_FOOD):
                    food = Resource(None, None, Resource.Type(3))
                    self.inventory.append(food)
                self.max_water += CANTEEN_VALUE
                return True
            return False
        
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
            if self.countInInventory(Resource.Type.WEAPON.value) == 0:
                self.inventory.append(resource)
                self.weapon_value = resource.value
                self.strength = self.base_strength + resource.value
                self.max_strength = (self.base_strength + resource.value)
                return True
            return False

        else:
            return "debug - item error"
        

    def eatFood(self):
        for item in self.inventory:
            if item.type.value == 3:
                self.inventory.remove(item)
                break
        self.hunger = min(100, self.hunger + FOOD_VALUE) 
                

    def drinkWater(self):
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
    
    # debug quickmove
    def move(self, row, col):
        self.pos = ((row, col))

    def singleMove(self, direction, arena):
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
            old_pos = self.pos
            self.pos = new_pos
            arena.restoreOldCellData(self, old_pos)
            return True
        else:
            return False

        

    def canMoveTo(self, pos):
        if pos[0] < 0 or pos[0] >= len(self.arenaKnowledge) or pos[1] < 0 or pos[1] >= len(self.arenaKnowledge[0]):
                return False
        cell = self.arenaKnowledge[pos[0]][pos[1]]
        if isinstance(cell, str):
            return True  # tribute on cell, walkable
        if int(cell) not in [8, 1]:
            return True
        return False
        


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
        
        if not target.isAlive:
            self.num_kills += 1

    def sleep(self):
        # handler handles the "tired enough" case
        self.health += SLEEP_VALUE
            
        

    def countInInventory(self, resource_type):
        return len([item for item in self.inventory if item.type.value == resource_type])
    

    def updateKnowledge(self, arena, radius=2):
        row, col = self.pos
        for r in range(row - radius, row + radius + 1):
            for c in range(col - radius, col + radius + 1):
                if 0 <= r < arena.size and 0 <= c < arena.size:
                    self.arenaKnowledge[r][c] = arena.arena_grid[r][c]

    # def act - implement AI tribute logic here - begin games
