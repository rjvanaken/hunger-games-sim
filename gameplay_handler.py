import random
from Resource import Resource

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


def handleAttack (tribute, target):
    if (-2 <= tribute.pos[0] - target.pos[0] <= 2) and (-2 <= tribute.pos[1] - target.pos[1] <= 2) :
        tribute.attack(target)
        return True
    else:
        print("cannot attack, too far away") # temp debug


def handleEatFood (tribute):
    if tribute.hunger != 100:
        if tribute.food >= 1:
            tribute.eatFood()
            return True
        else:
            print("no food units left to use") # temp debug
            return False
    return False


def handleDrinkWater (tribute):
    if tribute.thirst != 100:
        if tribute.water_supply >= 1:
            tribute.drinkWater()
            return True
        else:
            print("no water units left to use") # temp debug
            return False
    return False

def handleUseMedical (tribute):
    if tribute.health != 100:
        if tribute.medical >= 1:
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

def handlePickup (tribute, resource):
    if resource is None:
        return True # doesn't mean successful pickup, but tracked as a successful turn
    requires_skill_check = random.randint(0, 100)
    if requires_skill_check > 30:
        # if chance is greater than skill, simply return True, don't pick up
        if random.randint(1, 100) >= tribute.hunting_skill:
            return True # doesn't mean successful pickup, but tracked as a successful turn
    
    rp = resource.pos
    if canPickup(tribute, rp):
        tribute.pickUpResource(resource)
        return True
    else:
        if tribute.inventory == tribute.capacity:
            print("no more room in inventory")
        else:
            print("Cannot pick up") # temp debug
        return False



def canPickup (tribute, resourcePos):
    if tribute.inventory < tribute.capacity:
        success = False
        tRow = tribute.pos[0]
        tCol = tribute.pos[1]
        rRow = resourcePos[0]
        rCol = resourcePos[1]
        if tRow == rRow + 1 and tCol == rCol:
            success = True
        elif tRow == rRow - 1 and tCol == rCol:
            success = True
        elif tRow == rRow and tCol == rCol + 1:
            success = True
        elif tRow == rRow and tCol == rCol - 1:
            success = True
        
        return success
    else:
        return False

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
        
    
        

def isCellEmpty(arena, row, col):
    if arena.arena_grid[row, col] != 0:
        return False
    return True

# def handleSleep(tribute):
#     if tribute.isAsleep == False:
#         tribute.sleep
#     pass


    # return True
    # need to figure out how to track the number of turns to be asleep for when marking handle sleep
    # so then therefore how do I 