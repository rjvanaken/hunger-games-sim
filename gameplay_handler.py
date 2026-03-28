import random
from Resource import Resource
from config import SLEEP_VALUE, TURNS_PER_DAY
import numpy as np

def handleMove (tribute, arena):
    # only used by manual - AI mode will use pathfinding

    # OR I could make this change with a flag, if manual run the generic move and if not run the algorithm for going to that spot?
    # unless the AI handles that? Still unsure. Will keep this for now

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

def handleAttack (tribute, arena):
    target = arena.getTarget(tribute, True)
    if not target:
        return False
    if (-1 <= tribute.pos[0] - target.pos[0] <= 1) and (-1 <= tribute.pos[1] - target.pos[1] <= 1):
        tribute.attack(target)
        return True
    else:
        print("cannot attack, too far away") # temp debug
        return False


def handleEatFood (tribute):
    if tribute.hunger != 100:
        if tribute.getFood() >= 1:
            tribute.eatFood()
            return True
        else:
            print("no food units left to use") # temp debug
            return False
    return False


def handleDrinkWater (tribute, arena):
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
    if tribute.health != 100:
        if tribute.getMedical() >= 1:
            tribute.useMedical()
            return True
        else:
            print("no medical units left to use") # temp debug
            return False
    return False

def handleRefillWater(tribute, arena):
    if tribute.max_water != 0:
        if tribute.water_supply < tribute.max_water:
            if checkNeighborsFor(tribute, arena, 1):
                tribute.refillWater()
                return True
    return False

def handlePickup(tribute, arena):

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
    print(f"resource type: {resource.type}, pickup result: {pickup}")
    if pickup == True:
        arena.removeResource(resource)
        return 1
    return 0


def handleSleep(tribute):
    if tribute.health <= 100 - SLEEP_VALUE:
        tribute.sleep()
        return True
    else:
        print("You are not tired")
        return False
    

def handleMuttAttack(tribute, arena):
    mutt = arena.getTarget(tribute) # if mutt on square, attack before tribute's next turn

    if hasattr(mutt, 'isDormant'):
        if mutt != None and not mutt.isDormant:
            mutt.attack(tribute)


def getRandomValidMove(tribute, arena):
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
    tribute.last_move = move
    
    return move



def removeResource(self, resource):
    '''
    Run after pickup resource. 
    Removes the resource from the resources list, grid, and 
    changes id and pos to None
    '''
    self.resources.remove(resource)
    self.arena_grid[resource.pos[0]][resource.pos[1]] = 0
    resource.pos = None
    resource.id = None

def wasFoodPickedUp(tribute):
    # requires_skill_check = random.randint(0, 100)
    # # 70% chance of getting a skill check
    # if requires_skill_check > 30:
    #     # if chance is greater than skill, return food check as a fail
    #     if random.randint(1, 100) >= tribute.hunting_skill:
    #         return False 
    
    # # either no check or successful pickup check, return true
    return True


def checkNeighborsFor(tribute, arena, type_num=-1, find_tribute=False):
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
    # is the space free from obstacles or water sources?
    posR = tribute.pos[0]
    posC = tribute.pos[1]
    if direction.lower() == 'u' or direction.lower() == 'up':
       if tribute.canMoveTo((posR - 1, posC)):
           if tribute.last_move == 1:
               return False
           return True
    elif direction.lower() == 'd' or direction.lower() == 'down':
       if tribute.canMoveTo((posR + 1, posC)):
           if tribute.last_move == 0:
               return False
           return True
    elif direction.lower() == 'l' or direction.lower() == 'left':
       if tribute.canMoveTo((posR, posC - 1)):
           if tribute.last_move == 3:
               return False
           return True
    elif direction.lower() == 'r' or direction.lower() == 'right':
       if tribute.canMoveTo((posR, posC + 1)):
           if tribute.last_move == 2:
               return False
           return True
    return False

def attackMask(arena, tribute):
    if checkNeighborsFor(tribute, arena, find_tribute=True):
        return True
    for mutt in arena.mutts:
        if mutt.pos == tribute.pos:
            return True
    return False

def pickupMask(tribute, arena):
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
    # is hunger under 100 and do you have food
    if tribute.hunger != 100 and tribute.getFood() > 0:
        return True
    return False

def drinkMask(tribute, arena):
    # is thirst under 100 and do you have water (or by water source)
    if tribute.thirst != 100 and (tribute.water_supply > 0 or checkNeighborsFor(tribute, arena, 1)):
        return True
    return False


def healMask(tribute):
    # is health under 100 and do you have medical
    if tribute.health != 100 and tribute.getMedical() > 0:
        return True
    return False

def sleepMask(tribute):
    # is tribute tired enough to sleep
    if tribute.health <= 100 - SLEEP_VALUE:
        return True
    return False
    

def refillMask(tribute, arena):
    # is there no water near you or do you not have a canteen?
    if tribute.water_supply < tribute.max_water and checkNeighborsFor(tribute, arena, 1) and tribute.countInInventory(2) > 0:
        return True
    return False



    # return True
    # need to figure out how to track the number of turns to be asleep for when marking handle sleep
    # so then therefore how do I 



    # ROBOT PLAY FUNCTIONS

def getLocalView(tribute, arena, radius=2):
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
    for r in range(len(tribute.arenaKnowledge)):
        for c in range(len(tribute.arenaKnowledge[r])):
            if tribute.arenaKnowledge[r][c] == 1: 
                return r, c
    return 0, 0  # none yet

def setValuesBeforeTurn(tribute, arena):
    tribute.segment = arena.getSegmentFromPos(tribute.pos)
    segment = tribute.segment
    arena.updateSegmentData(tribute, segment)
    tribute.updateStatsBeforeTurn() # right now, recalcs strength - mutt logic to be added either here or there
    tribute.updateKnowledge(arena)
    handleMuttAttack(tribute, arena)




def cleanUpAfterTurn(game, arena):
    
    arena.clearDeadTributes(game)
    arena.clearDeadMutts()
    if len(arena.tributes) <= 1:
        return
    if all(t.turn_count == TURNS_PER_DAY for t in arena.tributes):
        for t in arena.tributes:
            t.turn_count = 0


def setupActionMap(tribute, arena, game):
    
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
    if attackMask(arena, tribute) and not (game.day_count == 0 and tribute.turn_count < 2):
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