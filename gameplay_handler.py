import random
from Resource import Resource
from config import SLEEP_VALUE

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
    target = arena.getTarget(tribute)
    if not target:
        return False
    if (-2 <= tribute.pos[0] - target.pos[0] <= 2) and (-2 <= tribute.pos[1] - target.pos[1] <= 2) :
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
    requires_skill_check = random.randint(0, 100)
    # 70% chance of getting a skill check
    if requires_skill_check > 30:
        # if chance is greater than skill, return food check as a fail
        if random.randint(1, 100) >= tribute.hunting_skill:
            return False 
    
    # either no check or successful pickup check, return true
    return True


def checkNeighborsFor(tribute, arena, type_num):
    tRow = tribute.pos[0]
    tCol = tribute.pos[1]
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
    # is there a tribute on the same cell as you?
    canAttack = False
    for target in arena.tributes:
        if target.pos == tribute.pos and tribute != target:
            canAttack = True
            break
    if canAttack:
        return True
    return False

def pickupMask(tribute, arena):
    canPickup = False
    for resource in arena.resources:
        if resource.pos == tribute.pos:
            canPickup = True
            break
        elif resource.type.value == 6 or resource.type.value == 7:
            canPickup = True
    if canPickup:
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