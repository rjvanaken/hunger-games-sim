import random
import math

# Constants
from config import BASE_DAMAGE, DAMAGE_MULTIPLIER, WATER_VALUE, FOOD_VALUE, MEDICAL_VALUE, CANTEEN_VALUE, CAREER_BONUS, MALE_BONUS, STRENGTH_BY_AGE, BASE_SPEED

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
        self.strength = self.getRandomStrength()
        self.max_strength = self.strength
        self.max_speed = self.getRandomSpeed()
        self.speed = self.max_speed
        self.health = 100
        self.thirst = 100
        self.hunger = 100
        self.water_supply = 0
        self.max_water = 0
        self.food = 0
        self.medical = 0
        self.capacity = 2
        self.inventory = 0
        self.weapon_value = 0
        self.isAlive = True
        self.isAsleep = False
        self.isWalking = False
        self.arenaKnowledge = []
        
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
        base_strength = random.randint(min, max)

        if self.district == 1 or self.district == 2 or self.district == 4:
            base_strength += CAREER_BONUS
        if self.gender == 'male':
            base_strength += MALE_BONUS

        return base_strength
    

    def getRandomSpeed(self):
        return random.randint(BASE_SPEED, BASE_SPEED + 2)
        

    def getRandomAge(self):
        return random.randint(12, 18)



# GAME ACTIONS

    def pickUpResource(self, resource):
    # need to have all pickups in case they get things from sponsors
    # TODO factor in sponsor logic eventually
        if self.inventory == self.capacity and resource.type != 1:
            return "storage capacity reached. cannot pick up new item"

        elif resource.type == 1:
            self.water_supply = self.max_water
            self.thirst = 100
        
        
        elif resource.type == 2:
            self.max_water += CANTEEN_VALUE
            self.inventory += 1

        elif resource.type == 3:
            for i in range(resource.value):
                if self.inventory < self.capacity:
                    self.food += int(resource.value)
                    self.inventory += 1

        elif resource.type == 4:
            self.medical += 1
            self.inventory += 1
        
        elif resource.type == 5:
            self.inventory += 1
            if int(resource.value) > self.weapon_value:
                # Update strength by the difference
                self.strength += (int(resource.value) - self.weapon_value)
                self.weapon_value = int(resource.value)  # Update weapon value too!
            # If new weapon is worse, don't pick it up (or just don't update anything)

        # TODO: confirm and adjust backpack sizes in testing
        elif resource.type == 6:
            self.capacity += 5
            self.food += 2
            self.max_water += CANTEEN_VALUE
            self.inventory += 3
            
        elif resource.type == 7:
            self.capacity += 10
            self.food += 3
            self.medical += 1
            self.max_water += CANTEEN_VALUE
            self.inventory += 5

        else:
            return "debug - item error"
        

    def eatFood(self):
        self.food -= 1
        self.inventory -= 1
        if self.hunger + FOOD_VALUE > 100:
            self.hunger = 100
        else:
            self.hunger += FOOD_VALUE    

    def drinkWater(self):
        # TODO: confirm and adjust water unit value as needed in testing
        self.water_supply -= 1
        if self.thirst + WATER_VALUE > 100:
            self.thirst = 100
        else:
            self.thirst += WATER_VALUE

    def useMedical(self):
        self.medical -= 1
        self.inventory -= 1
        if self.health + MEDICAL_VALUE > 100:
            self.health = 100
        else:
            self.health += MEDICAL_VALUE

    
    # movement function logic is temporary so they can move
    # TODO: update so they navigate in that general direction once tribute agent is working

    def move(self, row, col):
        self.pos = ((row, col))

    def singleMove(self, direction):
        
        if direction.lower() == 'u' or direction.lower() == 'up':
            self.pos = ((self.pos[0] - 1, self.pos[1]))
        if direction.lower() == 'd' or direction.lower() == 'down':
            self.pos = ((self.pos[0] + 1, self.pos[1]))
        if direction.lower() == 'l' or direction.lower() == 'left':
            self.pos = ((self.pos[0], self.pos[1] - 1))
        if direction.lower() == 'r' or direction.lower() == 'right':
            self.pos = ((self.pos[0], self.pos[1] + 1))
        
    # note: checking the path happens in the validation. This simply does the action. separation of concerns

            


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

    