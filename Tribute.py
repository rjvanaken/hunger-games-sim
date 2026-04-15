"""
Tribute.py - defines the Fighter, Mutt, and Tribute classes.
Fighter is the parent class for Tribute and Mutt, both of which can engage in combat in the arena.
"""

import random
import math
from Resource import Resource
import gameplay_handler as gh

# Constants
from config import *


class Fighter:
    """
    Represents the Fighter class, the parent class for the Tributes and Mutts, both of whih 
    can attack in the arena.
    """
    def __init__(self, id, pos):
        self.id = id
        self.pos = pos
        self.health = 100
        self.strength = 0 # set by subclass
        self.isAlive = True
        self.num_kills = 0

    @property
    def health(self):
        """Current health of the fighter (0-100). Setting to 0 or below marks the fighter as dead."""

        return self._health

    @health.setter
    def health(self, value):
        self._health = value
        if self._health <= 0:
            self._health = 0
            self.isAlive = False


    @property
    def pos(self):
        """Current position of the fighter as a (row, col) tuple."""

        return self._pos

    @pos.setter
    def pos(self, value):
        self._pos = value


    def attack(self, target, print_moves=False):
        """
        Executes an attack between this fighter and a target.
        Uses relative strength to determine the probability of winning the exchange.
        The loser takes damage based on the winner's strength. Increments kill count if target dies.
        """
        difference = max(target.strength, self.strength) - min(target.strength, self.strength)
        if self.strength > target.strength:
            attacker = (50 + difference) / 100
        else:
            attacker = (50 - difference) / 100

        if random.random() >= attacker:
            target.health -= (BASE_DAMAGE + int(math.ceil((self.strength * DAMAGE_MULTIPLIER))))
            if isinstance(target, Mutt):
                if print_moves:
                    print("Tribute wins an attack against a mutt")
            else:
                if print_moves:
                    print(f"Tribute {self.letter} wins attack, tribute {str(target.letter)} health decreased")
        else:
            self.health -= (BASE_DAMAGE + int(math.ceil((target.strength * DAMAGE_MULTIPLIER))))
            if isinstance(target, Mutt):
                if print_moves:
                    print("A mutt won an attack on a tribute, tribute health decreased")
            else:
                if print_moves:
                    print(f"Target ({str(target.letter)}) wins attack, tribute {self.letter} health decreased")
        if not isinstance(target, Mutt):
            if not target.isAlive:
                self.num_kills += 1


class Mutt(Fighter):
    """
    Represents a Mutt, a gamemaker-deployed creature that can attack tributes.
    Begins dormant and must be activated before it can engage in combat.

    (currently disabled)
    """
    def __init__(self, id, pos):
        super().__init__(id, pos)
        self.strength = MUTT_STRENGTH
        self.isDormant = True


    def activateMutt(self):
        self.isDormant = False


class Tribute(Fighter):
    """
    Represents a tribute competing in the Hunger Games arena.
    Manages survival stats, inventory, movement, and combat actions.
    Inherits combat logic from Fighter.
    """

    def __init__(self, id, pos):

        super().__init__(id, pos)

        if id % 2 == 0:
            self.gender = 'male'
        else:
            self.gender = 'female'

        self.letter = chr(65 + id)
        self.district = (id // 2) + 1
        self.age = self.getRandomAge()
        self.hunting_skill = self.getHuntingSkill()
        self.max_speed = self.getRandomSpeed()
        self.base_strength = self.getRandomStrength()
        self.strength = self.base_strength
        self.max_strength = self.strength
        self.speed = self.max_speed
        self.thirst = 100
        self.hunger = 100
        self.water_supply = 0
        self.max_water = 0
        self.capacity = 2
        self.inventory = []
        self.weapon_value = 0
        self.arenaKnowledge = []
        self.segment = None
        self.turn_count = 0
        self.last_move = None
        self.recently_attacked = 0
        self.move_map = {'up' : 0, 'down' : 1, 'left' : 2, 'right' : 3}
        self.hazard_death = False
        self.near_hazard = False
        self.hazard_warning_zone = False
        

        # somehow need to figure out how strength will be impacted by low health and how that will change, etc.

      

    def getRandomStrength(self):
        """Returns a randomized strength value based on age, district, and gender."""

        min, max = STRENGTH_BY_AGE[self.age]
        raw_strength = random.randint(min, max)

        if self.district == 1 or self.district == 2 or self.district == 4:
            raw_strength += CAREER_BONUS
        if self.gender == 'male':
            raw_strength += MALE_BONUS
    

    def getRandomSpeed(self):
        """Returns a randomized speed value within the base speed range."""
        return random.randint(BASE_SPEED, BASE_SPEED + 2)
        
    def getHuntingSkill(self):
        """Returns a randomized hunting skill value between 1 and 100."""

        return random.randint(1, 100)
        

    def getRandomAge(self):
        """Returns a randomized age between 12 and 18."""

        return random.randint(12, 18)


    def updateStatsBeforeTurn(self): #atm does not handle mutt attack before turn
        """Applies stat decay and recalculates strength before the tribute's turn."""

        self.updateDailyStats()
        self.strength = math.ceil((self.base_strength + self.weapon_value) * (self.health / 100))

    def updateDailyStats(self):
        """Decrements hunger and thirst each turn and applies health penalties if below warning thresholds."""

        self.hunger -= HUNGER_DECAY
        self.thirst -= THIRST_DECAY
        self.hunger = max(0, self.hunger)
        self.thirst = max(0, self.thirst)
        # subtract full penalty if under 0, partial if only below threshold
        if self.hunger <= 0:
            self.health -= HUNGER_HEALTH_PENALTY
        elif self.hunger <= HUNGER_WARNING_THRESHOLD:
            penalty = HUNGER_WARNING_PENALTY * (1 - self.hunger / HUNGER_WARNING_THRESHOLD)
            self.health -= penalty
        
        # subtract full penalty if under 0, partial if only below threshold
        if self.thirst <= 0:
            self.health -= THIRST_HEALTH_PENALTY
        elif self.thirst <= THIRST_WARNING_THRESHOLD:
            penalty = THIRST_WARNING_PENALTY * (1 - self.thirst / THIRST_WARNING_THRESHOLD)
            self.health -= penalty

        self.health = max(0, self.health)  # clamp health
        if self.health <= 0:
            self.isAlive = False


    def getFood(self):
        """Returns the number of food items in the tribute's inventory."""

        food = 0
        for item in self.inventory:
            if item.type.value == 3:
                food += 1
        return food
    
    def getMedical(self):
        """Returns the number of medical items in the tribute's inventory."""

        medical = 0
        for item in self.inventory:
            if item.type.value == 4:
                medical += 1
        return medical

# GAME ACTIONS

    def pickUpResource(self, resource):
        """
        Attempts to add a resource to the tribute's inventory.
        Handles backpacks, weapons, food, water containers, and medical items differently.
        Returns True if successful, False if not.
        """


        if resource.type == Resource.Type.BACKPACK_SMALL:
            if self.capacity <= 2:
                self.capacity += SMALL_CAPACITY
                # canteen = Resource(None, None, Resource.Type(2))
                # self.inventory.append(canteen)
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
                # canteen = Resource(None, None, Resource.Type(2))
                # self.inventory.append(canteen)
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
        """Consumes one food item from inventory and restores hunger."""

        for item in self.inventory:
            if item.type.value == 3:
                self.inventory.remove(item)
                break
        self.hunger = min(100, self.hunger + FOOD_VALUE) 
                

    def drinkWater(self):
        """Consumes one unit of water supply and restores thirst."""

        self.water_supply -= 1
        self.thirst = min(100, self.thirst + WATER_VALUE)

    def useMedical(self):
        for item in self.inventory:
            if item.type.value == 4:
                self.inventory.remove(item)
                break
        self.health = min(100, self.health + MEDICAL_VALUE) 

    def refillWater(self):
        """Consumes one medical item from inventory and restores health."""

        self.water_supply = self.max_water
    
    # debug quickmove
    def move(self, row, col):
        """Debug utility to teleport the tribute directly to a given position."""

        self.pos = ((row, col))

    def singleMove(self, direction, arena):
        """
        Moves the tribute one cell in the given direction if the destination is valid.
        Returns True if successful, False otherwise.
        """
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
        """
        Returns True if the given position is a valid, unobstructed cell the tribute can move to.
        """
        if pos[0] < 0 or pos[0] >= len(self.arenaKnowledge) or pos[1] < 0 or pos[1] >= len(self.arenaKnowledge[0]):
                return False
        cell = self.arenaKnowledge[pos[0]][pos[1]]
        if isinstance(cell, str):
            return True  # tribute on cell, walkable
        if int(cell) not in [8, 1, 2]:
            return True
        return False
        


    def countInInventory(self, resource_type):
        """Returns the count of items of a given resource type in the tribute's inventory."""

        return len([item for item in self.inventory if item.type.value == resource_type])
    

    def updateKnowledge(self, arena, radius=2):
        """Updates the tribute's arena knowledge within a given radius of their current position."""

        row, col = self.pos
        for r in range(row - radius, row + radius + 1):
            for c in range(col - radius, col + radius + 1):
                if 0 <= r < arena.size and 0 <= c < arena.size:
                    self.arenaKnowledge[r][c] = arena.arena_grid[r][c]

    # def act - implement AI tribute logic here - begin games
