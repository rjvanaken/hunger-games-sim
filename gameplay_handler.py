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
    if tribute.pos[1] == target.pos[1] - 2 or tribute.pos[1] == target.pos[1] + 2:
        tribute.attack(target)
        return True  
    elif tribute.pos[0] == target.pos[0] - 2 or tribute.pos[0] == target.pos[0] + 2:
        tribute.attack(target)
        return True
    else:
        print("cannot attack, too far away") # temp debug


def handleEatFood (tribute):
    if tribute.food >= 1:
        tribute.eatFood()
        return True
    else:
        print("no food units left to use") # temp debug


def handleDrinkWater (tribute):
    if tribute.water >= 1:
        tribute.drinkWater()
        return True
    else:
        print("no water units left to use") # temp debug

def handleUseMedical (tribute):
    if tribute.medical >= 1:
        tribute.useMedical()
        return True
    else:
        print("no medical units left to use") # temp debug

def handlePickup (tribute, resource):
    if resource.pos == tribute.pos:
        tribute.pickUpResource(resource)
        return True
    else:
        print("No resource to pick up") # temp debug

def handleSleep(tribute):
    pass
    # return True
    # need to figure out how to track the number of turns to be asleep for when marking handle sleep
    # so then therefore how do I 