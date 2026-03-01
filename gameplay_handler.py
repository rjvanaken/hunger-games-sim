def handleMove (game, tribute, row, col):
    # only used by manual - AI mode will use pathfinding
    if game.arena.arena_grid[row, col] == 0:
        tribute.move(row, col)
    else:
        print ("spot is not free") # temp debug


def handleAttack (tribute, target):
    if tribute.pos[1] == target.pos[1] - 2 or tribute.pos[1] == target.pos[1] + 2:
        tribute.attack(target)
    elif tribute.pos[0] == target.pos[0] - 2 or tribute.pos[0] == target.pos[0] + 2:
        tribute.attack(target)
    else:
        print("cannot attack, too far away") # temp debug


def handleEatFood (tribute):
    if tribute.food >= 1:
        tribute.eatFood()
    else:
        print("no food units left to use") # temp debug


def handleDrinkWater (tribute):
    if tribute.water >= 1:
        tribute.drinkWater()
    else:
        print("no water units left to use") # temp debug

def handleUseMedical (tribute):
    if tribute.medical >= 1:
        tribute.useMedical()
    else:
        print("no medical units left to use") # temp debug

def handlePickup (tribute, resource):
    if resource.pos == tribute.pos:
        tribute.pickUpResource(resource)
    else:
        print("No resource to pick up") # temp debug