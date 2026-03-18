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

def handleSingleMove (tribute, direction):
    if direction.lower() == 'u' or direction.lower() == 'up':
       move = tribute.singleMove('u')
    elif direction.lower() == 'd' or direction.lower() == 'down':
        move = tribute.singleMove('d')
    elif direction.lower() == 'l' or direction.lower() == 'left':
        move = tribute.singleMove('l')
    elif direction.lower() == 'r' or direction.lower() == 'right':
        move = tribute.singleMove('r')
    
    if move == True:
        return True
    else:
        return False

def handleAttack (tribute, target):
    if (-2 <= tribute.pos[0] - target.pos[0] <= 2) and (-2 <= tribute.pos[1] - target.pos[1] <= 2) :
        tribute.attack(target)
        return True
    else:
        print("cannot attack, too far away") # temp debug


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

def handlePickup (tribute, arena):
    if len(tribute.inventory) == tribute.capacity:
        print("no more room in inventory")
        return False
    resource = arena.getResourceAt(tribute.pos)
    if resource is None:
        return False

    if resource.type.value == 3:
        if not wasFoodPickedUp(tribute):
            return True # return True and consume turn, just don't pick up anything
    
    pickup = tribute.pickUpResource(resource)
    if pickup == True:
        arena.removeResource(resource)
        return True
    return False


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



def pickupMask (tribute, resourcePos):
    # REWRITE AND UTILIZE FOR ACTION MASKING
    pass

def walkMask():
    # are there obstacles in every spot near them? actually this seems impossible...
    # instead, block the directions?
    # ALSO do I need to instead make 4 separate actions instead of inputting direction?
    pass


def drinkMask():
    # is thirst at 100 or do you not have any water
    pass

def eatMask():
    # is hunger at 100 or do you not have any food
    pass

def healMask():
    # is health at 100 or do you not have any medical items?
    pass

def attackMask():
    # is there another alive tribute on your current cell?
    pass

def pickupMask():
    # is there no object in the current cell?
    pass

def refillMask():
    # is there no water near you or do you not have a canteen?
    pass





    # return True
    # need to figure out how to track the number of turns to be asleep for when marking handle sleep
    # so then therefore how do I 