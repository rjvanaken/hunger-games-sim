
"""
gameplay_handler.py - houses all the action handling functions that will need to be shared by both the training
process and running the agent against the model.

"""

import random
from Resource import Resource
from config import *
import numpy as np



def handleMove (tribute, arena):
    """
    Can be used in manual mode and for testing to jump to any location on the grid
    """

    row = int(input ("Enter the destination row: "))
    col = int(input("Enter the destination column: "))

    if row < arena.size or col < arena.size:
        if arena.arena_grid[row][col] == 0:
            arena.moveTribute(tribute, row, col)
            return True
        else:
            print ("spot is not free") # temp debug
    else:
        print("Invalid row or column") # temp debug


def handleSingleMove (tribute, direction, arena):
    """
    Handles the move logic and executes the tribute's singleMove function with the passed in direction
    Returns True if successful, otherwise False
    """

    if direction.lower() == 'u' or direction.lower() == 'up':
       move = tribute.singleMove('u', arena)
    elif direction.lower() == 'd' or direction.lower() == 'down':
        move = tribute.singleMove('d', arena)
    elif direction.lower() == 'l' or direction.lower() == 'left':
        move = tribute.singleMove('l', arena)
    elif direction.lower() == 'r' or direction.lower() == 'right':
        move = tribute.singleMove('r', arena)
    
    if move == True:
        return True
    else:
        return False

def handleAttack (tribute, arena, print_moves):
    """
    Handles the attack logic and executes the tribute's attack function appropriately
    Returns True if successful, otherwise False
    """

    target = arena.getTarget(tribute, True)
    if not target:
        return False
    if (-1 <= tribute.pos[0] - target.pos[0] <= 1) and (-1 <= tribute.pos[1] - target.pos[1] <= 1):
        tribute.attack(target, print_moves)
        target.recently_attacked = 1
        return True
    else:
        print("cannot attack, too far away") # temp debug
        return False


def handleEatFood (tribute):
    """
    Handles the eat logic and executes the tribute's eatFood function appropriately
    Returns True if successful, otherwise False
    """

    if tribute.hunger != 100:
        if tribute.getFood() >= 1:
            tribute.eatFood()
            return True
        else:
            print("no food units left to use") # temp debug
            return False
    return False


def handleDrinkWater (tribute, arena):
    """
    Handles the logic for drinking water executes the tribute's drinkWater function appropriately
    Returns True if successful, otherwise False
    """

    if tribute.thirst != 100:
        if checkNeighborsFor(tribute, arena, 1) == True:
            tribute.thirst = 100
            ("near water")
            return True
        elif tribute.water_supply >= 1:
            tribute.drinkWater()
            return True
        # allow drink water if at water source, and fully max water
        else:
            print("no water units left to use") # temp debug
            return False
    return False

def handleUseMedical (tribute):
    """
    Handles the heal logic and executes the tribute's useMedical function appropriately
    Returns True if successful, otherwise False
    """

    if tribute.health != 100:
        if tribute.getMedical() >= 1:
            tribute.useMedical()
            return True
        else:
            print("no medical units left to use") # temp debug
            return False
    return False

def handleRefillWater(tribute, arena):
    """
    Handles the logic for refilling water at water sources, and executes the tribute's refill function appropriately
    Returns True if successful, otherwise False
    """

    if tribute.max_water != 0:
        if tribute.water_supply < tribute.max_water:
            if checkNeighborsFor(tribute, arena, 1):
                tribute.refillWater()
                return True
    return False

def handlePickup(tribute, arena):
    """
    Handles the logic for picking up resources and weapons, and executes the tribute's pickup function appropriately
    Returns 1 if successful, 2 if pickup failed, and 0 if there is no room in the tribute's inventory
    """

    resource = arena.getResourceAt(tribute.pos)
    if resource is None:
        print("No resource at your position.")
        return 0

    if len(tribute.inventory) == tribute.capacity:
        if resource.type.value != 6 and resource.type.value != 7:
            print("no more room in inventory")
            return 0

    if resource.type.value == 3:
        if not wasFoodPickedUp(tribute):
            return 2

    pickup = tribute.pickUpResource(resource)
    if pickup == True:
        arena.removeResource(resource)
        return 1
    return 0

    

# def handleMuttAttack(tribute, arena):
    
#     mutt = arena.getTarget(tribute) # if mutt on square, attack before tribute's next turn

#     if hasattr(mutt, 'isDormant'):
#         if mutt != None and not mutt.isDormant:
#             mutt.attack(tribute)


def getRandomValidMove(tribute, arena):
    """
    Of the possible directions the tribute can choose to go, returns a random option
    """

    dirs = []
    if moveMask(tribute, 'up'):
        dirs.append('up')
    if moveMask(tribute, 'down'):
        dirs.append('down')
    if moveMask(tribute, 'left'):
        dirs.append('left')
    if moveMask(tribute, 'right'):
        dirs.append('right')
    
    if not dirs:
        return None
    move = random.choice(dirs)
    tribute.last_move = tribute.move_map[move]
    return move



def removeResource(self, resource):
    """
    Run after pickup resource. 
    Removes the resource from the resources list, grid, and 
    changes id and pos to None
    """
    self.resources.remove(resource)
    self.arena_grid[resource.pos[0]][resource.pos[1]] = 0
    resource.pos = None
    resource.id = None


def wasFoodPickedUp(tribute):
    """
    Adds a skill check to the tribute's food pickup success.
    No longer used for simplicity (but risky to remove without thorough testing)
    """

    # requires_skill_check = random.randint(0, 100)
    # # 70% chance of getting a skill check
    # if requires_skill_check > 30:
    #     # if chance is greater than skill, return food check as a fail
    #     if random.randint(1, 100) >= tribute.hunting_skill:
    #         return False 
    
    # # either no check or successful pickup check, return true
    return True


def checkNeighborsFor(tribute, arena, type_num=-1, find_tribute=False):
    """
    Checks neighboring cells for a resource of a given type or a living tribute.
    If find_tribute=True, returns the found tribute (or None).
    If find_tribute=False, returns True if a resource matching type_num is found, otherwise False.
    """
    
    tRow = tribute.pos[0]
    tCol = tribute.pos[1]

    if find_tribute:
        neighbors = [
        (tRow + 1, tCol),
        (tRow - 1, tCol),
        (tRow, tCol + 1),
        (tRow, tCol - 1)
    ]
        for row, col in neighbors:
            if 0 <= row < arena.size and 0 <= col < arena.size:
                cell = arena.arena_grid[row][col]
                if isinstance(cell, str):
                    for target in arena.tributes:
                        if target.pos == (row, col) and target != tribute and target.isAlive:
                            return target
                    

    else:
        neighbors = [
            arena.getResourceAt((tRow + 1, tCol)),
            arena.getResourceAt((tRow - 1, tCol)),
            arena.getResourceAt((tRow, tCol + 1)),
            arena.getResourceAt((tRow, tCol - 1))
        ]
        
        for item in neighbors:
            if item != None and item.type.value == type_num:
                return True
        return False




# ACTION MASKS
    
def moveMask(tribute, direction):

    """
    If there is an available location for the tribute to move to, returns True.
    Otherwise, False

    Used for action masking. Value is passed to another function to determine the direction
    """


    # is the space free from obstacles or water sources?
    posR = tribute.pos[0]
    posC = tribute.pos[1]
    if direction.lower() == 'u' or direction.lower() == 'up':
       if tribute.canMoveTo((posR - 1, posC)):
           return True
    elif direction.lower() == 'd' or direction.lower() == 'down':
       if tribute.canMoveTo((posR + 1, posC)):
           return True
    elif direction.lower() == 'l' or direction.lower() == 'left':
       if tribute.canMoveTo((posR, posC - 1)):
           return True
    elif direction.lower() == 'r' or direction.lower() == 'right':
       if tribute.canMoveTo((posR, posC + 1)):
           return True
    return False

def attackMask(arena, tribute):
    """
    If there is a tribute available to attack, returns True
    Otherwise, False

    Used for action masking
    """

    if checkNeighborsFor(tribute, arena, find_tribute=True):
        return True
    for mutt in arena.mutts:
        if mutt.pos == tribute.pos:
            return True
    return False

def pickupMask(tribute, arena):
    """
    If there is a resource or weapon available for pickup (in adjacent spots), returns True
    Otherwise, False

    Used for action masking
    """

    resource = arena.getResourceAt(tribute.pos)
    if resource is None:
        return False
    if resource.type == Resource.Type.BACKPACK_SMALL or resource.type == Resource.Type.BACKPACK_LARGE:
        if tribute.capacity > 2:
            return False
    if resource.type == Resource.Type.WEAPON:
        if tribute.countInInventory(Resource.Type.WEAPON.value) > 0:
            return False
    if len(tribute.inventory) < tribute.capacity:
        return True
    if resource.type == Resource.Type.BACKPACK_SMALL or resource.type == Resource.Type.BACKPACK_LARGE or resource.type == Resource.Type.WEAPON:
        return True
    return False

def eatMask(tribute):
    """
    If the tribute is hungry and has food in their inventory, return True
    Otherwise, False

    Used for action masking
    """
    # is hunger under 100 and do you have food
    if tribute.hunger != 100 and tribute.getFood() > 0:
        return True
    return False

def drinkMask(tribute, arena):
    """
    If the tribute is thirsty and has water in their inventory OR is next to a water source, return True
    Otherwise, False

    Used for action masking
    """

    # is thirst under 100 and do you have water (or by water source)
    if tribute.thirst != 100 and (tribute.water_supply > 0 or checkNeighborsFor(tribute, arena, 1)):
        return True
    return False


def healMask(tribute):
    """
    If the tribute is not fully healed and there is a medical item in their inventory, return True
    Otherwise, False

    Used for action masking
    """

    # is health under 100 and do you have medical
    if tribute.health != 100 and tribute.getMedical() > 0:
        return True
    return False
    

def refillMask(tribute, arena):
    """
    If there is a water source next to the tribute and the tribute has a canteen, return True
    Otherwise, False

    Used for action masking
    """

    # is there no water near you or do you not have a canteen?
    if tribute.water_supply < tribute.max_water and checkNeighborsFor(tribute, arena, 1) and tribute.countInInventory(2) > 0:
        return True
    return False






# ROBOT PLAY FUNCTIONS

def setupActionMap(tribute, arena, game):

    """
    Builds out the action map for the tribute using the action masks to only display the actions
    that the tribute can actually perform that turn based on various conditions
    """
    
    valid_actions = set()
    up = moveMask(tribute, 'up')
    down = moveMask(tribute, 'down')
    left = moveMask(tribute, 'left')
    right = moveMask(tribute, 'right')
    mutt = arena.getTarget(tribute)
    preventMove = hasattr(mutt, 'isDormant') and mutt.isAlive and not mutt.isDormant

    if not preventMove:
        if up or down or left or right:
            valid_actions.add(0)
    if attackMask(arena, tribute) and not (game.day_count == 0 and tribute.turn_count < 3):
    # add attack to valid actions
        valid_actions.add(1)
    if pickupMask(tribute, arena):
        valid_actions.add(2)
    if eatMask(tribute):
        valid_actions.add(3)
    if drinkMask(tribute, arena):
        valid_actions.add(4)
    if healMask(tribute):
        valid_actions.add(5)
    # if sleepMask(tribute):
    #     valid_actions.add(6)
    if refillMask(tribute, arena):
        valid_actions.add(6)
    
    return valid_actions

def getLocalView(tribute, arena, radius=2):

    """
    Gets the tribute's local view for the observation
    """

    size = radius * 2 + 1
    view = np.zeros((size, size), dtype=np.int32)

    for dr in range(-radius, radius + 1):
        for dc in range(-radius, radius + 1):
            r = tribute.pos[0] + dr
            c = tribute.pos[1] + dc
            row_i = dr + radius
            col_i = dc + radius
            
            if 0 <= r < arena.size and 0 <= c < arena.size:
                cell = arena.arena_grid[r][c]
                if isinstance(cell, str):  # tribute letter
                    view[row_i][col_i] = 10  # TRIBUTE
                else:
                    view[row_i][col_i] = cell # number already there
            else:
                view[row_i][col_i] = 8  # out of bounds is an obstacle

    return view

def getKnownWater(tribute):
    
    """
    Returns the locations of the water sources the tribute has visited
    """

    for r in range(len(tribute.arenaKnowledge)):
        for c in range(len(tribute.arenaKnowledge[r])):
            if tribute.arenaKnowledge[r][c] == 1: 
                return r, c
    return 0, 0  # none yet


def setValuesBeforeTurn(tribute, arena):
    """
    Sets up the starter values prior to the start of a turn round such as:
    - applying stat decay
    - updating the segment data for bomb functionality
    """

    tribute.near_hazard = False
    tribute.hazard_warning_zone = False
    tribute.segment = arena.getSegmentFromPos(tribute.pos)
    segment = tribute.segment
    arena.updateSegmentData(tribute, segment)
    tribute.updateStatsBeforeTurn() # right now, recalcs strength - mutt logic to be added either here or there
    # if tribute.isAlive:
    #     applyHazardDamage(tribute, arena)
    #     if not tribute.isAlive:
    #         tribute.hazard_death = True
    if tribute.isAlive:
        tribute.updateKnowledge(arena)
        # handleMuttAttack(tribute, arena)
    
      

# def applyHazardDamage(tribute, arena):
#     full_damage = False
#     row, col = tribute.pos
#     full = [(row + 1, col), (row - 1, col), (row, col + 1), (row, col - 1)]
#     warning_zone = [(row + 2, col), (row - 2, col), (row, col + 2), (row, col - 2)]  

#     all_hazard_positions = set(arena.hazard.positions)
#     for hazard in arena.hazards:
#         if hazard.pos is not None:
#             all_hazard_positions.add(hazard.pos)
#     full_damage = any(pos in all_hazard_positions for pos in full)

#     if full_damage:
#         if arena.hazard.isDeployed:
#             tribute.health -= HAZARD_DAMAGE
#             print(f"full damage applied to {tribute.letter}")
#         tribute.near_hazard = True

#     warning = not full_damage and any(pos in all_hazard_positions for pos in warning_zone)
#     if warning:
#         tribute.hazard_warning_zone = True



def cleanUpAfterTurn(game, arena):

    """
    After a tribute's turn, clear the dead tributes (and mutts, if that feature were implemented) and resets the tributes' turn counts
    """
    
    arena.clearDeadTributes(game)
    arena.clearDeadMutts()
    if len(arena.tributes) <= 1:
        return
    if all(t.turn_count == TURNS_PER_DAY for t in arena.tributes):
        for t in arena.tributes:
            t.turn_count = 0

        

def getRewardStarters(tribute):

    """
    Returns the current observation values prior to calculating rewards for eval mode
    """

    return {
        "health": tribute.health,
        "kills": tribute.num_kills,
        "food": tribute.getFood(),
        "very_hungry": tribute.hunger <= HUNGER_WARNING_THRESHOLD,
        "very_thirsty": tribute.thirst <= THIRST_WARNING_THRESHOLD,
        "very_low_health": tribute.health <= HEALTH_THRESHOLD,
        "weapon" : tribute.weapon_value,
        "capacity" : tribute.capacity,
        "was_near_hazard": tribute.near_hazard,
        "was_in_warning": tribute.hazard_warning_zone
    }


# EVAL FUNCTIONS

def calculateRewards(game, tribute, action, starters):

    """
    Calculates and returns the reward for a tribute's action in eval mode.
    Rewards are based on action type, stat changes (health, kills, hunger, etc.), and penalties for low stats or death. 
    
    Mirrors the reward logic in GameEnv.
    """

    health_before, kills_before, food_before, very_hungry, very_thirsty, very_low_health, weapon_before, capacity_before, was_near_hazard, was_in_warning = starters.values()
    reward = 0
    
    # if len(game.arena.tributes) <= TRIBUTE_PROXIMITY_TRIGGER:
    #     if isNearAnyTribute(tribute, game.arena): 
    #         reward += NEAR_TRIBUTE_REWARD

    if action == 0:
        reward += MOVE_REWARD
    elif action == 1:
        if tribute.recently_attacked:
            reward += CONTINUE_FIGHT_REWARD
            tribute.recently_attacked = 0
            game.retaliation_count += 1
        if tribute.num_kills > kills_before:
            reward += KILL_REWARD
        if tribute.health >= health_before:
            reward += WIN_ATTACK_REWARD
        reward += ATTACK_REWARD
    elif action == 2:
        reward += PICKUP_REWARD
        if tribute.getFood() > food_before:
            if very_hungry:
                reward += FOOD_PICKUP_REWARD
                game.desperate_resource_uses += 1
        if tribute.capacity > capacity_before:
            if tribute.capacity - capacity_before == LARGE_CAPACITY:
                reward += LARGE_BACKPACK_REWARD
            elif tribute.capacity - capacity_before == SMALL_CAPACITY:
                reward += SMALL_BACKPACK_REWARD
        elif tribute.weapon_value > weapon_before:
            if tribute.weapon_value - weapon_before == STRONG_WEAPON:
                reward += STRONG_WEAPON_REWARD
            elif tribute.weapon_value - weapon_before == WEAK_WEAPON:
                reward += WEAK_WEAPON_REWARD
    elif action == 3:
        reward += EAT_REWARD
        if very_hungry:
            reward += VERY_HUNGRY_BONUS
            game.desperate_resource_uses += 1
    elif action == 4:
        reward += DRINK_REWARD
        if very_thirsty:
            reward += VERY_THIRSTY_BONUS
            game.desperate_resource_uses += 1
    elif action == 5:
        reward += MEDICAL_REWARD
        if very_low_health:
            reward += VERY_LOW_HEALTH_BONUS
            game.desperate_resource_uses += 1
    elif action == 6:
        reward += REFILL_REWARD


    if tribute.hunger <= HUNGER_WARNING_THRESHOLD:
        reward -= LOW_HUNGER_PENALTY
    if tribute.thirst <= THIRST_WARNING_THRESHOLD:
        reward -= LOW_THIRST_PENALTY
    if tribute.health <= HEALTH_THRESHOLD:
        reward -= LOW_HEALTH_PENALTY

    # if tribute.hazard_warning_zone and not was_in_warning:
    #     reward -= ENTERED_WARNING_ZONE_PENALTY
    # if tribute.near_hazard and was_in_warning:
    #     reward -= ENTERED_HAZARD_PENALTY
    # if tribute.hazard_warning_zone and was_near_hazard:
    #     reward += MOVED_AWAY_FROM_HAZARD_REWARD
    # if tribute.near_hazard and was_near_hazard:
    #     reward -= STAYED_NEAR_HAZARD_PENALTY


    if not tribute.isAlive:
        reward -= DEATH_PENALTY

    game.game_rewards += reward
