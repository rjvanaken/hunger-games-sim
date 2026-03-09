import sys
import os

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from Game import Game
import gameplay_handler as gh


game = Game(20)
game.addTributes(game.arena.center)
game.arena.addCornucopia()
game.arena.addSources()
game.arena.addTrees(0.15)

game.arena.tributes = game.arena.tributes[:5]

T0 = game.arena.tributes[0]
T1 = game.arena.tributes[1]
T2 = game.arena.tributes[2]
T3 = game.arena.tributes[3]
T4 = game.arena.tributes[4]



def testHandleMove():
    pass    

def testHandleAttack():
    attack = gh.handleAttack(T1, T2)
    assert attack == True
    attack = gh.handleAttack(T0, T4)
    assert attack != True


def testHandlePickup():
    T0.move(T0.pos[0] + 1, T0.pos[1])
    resourcePos = (T0.pos[0] + 1, T0.pos[1])
    # WRONG: TODO: need to figure out how to 
    r = game.arena.getResourceAt((resourcePos))
    pickup = gh.handlePickup(T4, r)
    assert pickup == False
    pickup = gh.handlePickup(T0, r)
    assert pickup == True

    

def testHandleEatFood():
    T3.food = 2
    T3.hunger = 10
    result = gh.handleEatFood(T3)
    assert result == True
    T4.food = 1
    T4.hunger = 10
    result = False
    result = gh.handleEatFood(T4)
    assert result == True
    result = gh.handleEatFood(T4)
    assert result == False

    result = True
    result = gh.handleEatFood(T0)
    assert result == False


def testHandleDrinkWater():
    T3.thirst = 10
    T3.water_supply = 2
    result = gh.handleDrinkWater(T3)
    assert result == True
    T4.thirst = 10
    T4.water_supply = 1
    result = False
    result = gh.handleDrinkWater(T4)
    assert result == True
    result = gh.handleDrinkWater(T4)
    assert result == False
    
    result = True
    result = gh.handleDrinkWater(T0)
    assert result == False


def testHandleUseMedical():
    T3.medical = 2
    T3.health = 10
    result = gh.handleUseMedical(T3)
    assert result == True
    result = False
    T4.medical = 1
    T4.health = 10
    result = gh.handleUseMedical(T4)
    assert result == True
    result = gh.handleUseMedical(T4)
    assert result == False

    result = True
    result = gh.handleUseMedical(T0)
    assert result == False



# def handleSleep():
#     pass

def main():
    testHandleAttack()
    testHandleDrinkWater()
    testHandleEatFood()
    testHandlePickup()
    testHandleUseMedical

if __name__ == '__main__':
    main() 