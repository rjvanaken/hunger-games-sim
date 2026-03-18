from unittest.mock import patch
import sys
import os

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from Game import Game
from Arena import Arena
from Resource import Resource
from Tribute import Tribute
import gameplay_handler as gh
import tests.test_helper as th

game2 = Game(20)

game = Game(20)
game.addTributes(game.arena.center)
game.arena.addCornucopia()
game.arena.addSources()
game.arena.addTrees(0.15)


T0 = game.arena.tributes[0]
T1 = game.arena.tributes[1]
T2 = game.arena.tributes[2]
T3 = game.arena.tributes[3]
T4 = game.arena.tributes[4]
# pickup
T7 = game.arena.tributes[7] # pickup but inventory > than just 1 bc backpack
T8 = game.arena.tributes[8] # fail pickup
T9 = game.arena.tributes[9] # can pickup
T11 = game.arena.tributes[11]
T12 = game.arena.tributes[12]
T13 = game.arena.tributes[13]
T14 = game.arena.tributes[14]

for tribute in [T7, T8, T9, T11]:
    tribute.arenaKnowledge = game.arena.arena_grid



def testHandleMove():
    pass    

def testHandleAttack():
    attack = gh.handleAttack(T1, T2)
    assert attack == True
    attack = gh.handleAttack(T0, T4)
    assert attack != True


def testHandlePickup():
    T8.hunting_skill = 90
    T11.hunting_skill = 90
    T7.singleMove('l', game.arena)
    T7.singleMove('l', game.arena) # backpack
    T8.singleMove('l', game.arena) # nothing to pick up
    T9.singleMove('l', game.arena)
    T9.singleMove('l', game.arena) # weapon
    T11.singleMove('l', game.arena)
    T11.singleMove('l', game.arena) # backpack
    T7.inventory = []
    T8.inventory = []
    T11.inventory = []
    
    # item picked up regardless bc not food, no skill check
    with patch('random.randint', side_effect=[50, 99]):
        pickup = gh.handlePickup(T7, game.arena)
        assert len(T7.inventory) == 3
        assert pickup == True



    # env setup
    arena2 = Arena(20)
    food = Resource(1, (5, 5), Resource.Type(3))
    arena2.resources.append(food)
    t = Tribute(99, (5, 5))
    arena2.tributes.append(t)
    arena2.arena_grid[5][5] = t.letter

    food2 = Resource(1, (8, 8), Resource.Type(3))
    arena2.resources.append(food2)
    t2 = Tribute(100, (8, 8))
    arena2.tributes.append(t2)
    arena2.arena_grid[8][8] = t2.letter
    t2.arenaKnowledge = arena2.arena_grid

    # check, passed, successful pickup, inventory increased
    with patch('random.randint', side_effect=[50, 10]):
        pickup = gh.handlePickup(t, arena2)
        assert len(t.inventory) == 1
        assert pickup == True

    # no check, straight to pickup, inventory increased
    with patch('random.randint', return_value=20):
        pickup = gh.handlePickup(t2, arena2)
        assert len(t2.inventory) == 1
        assert pickup == True

    t2.move(t2.pos[0], t2.pos[1] + 1)
    
    # spot is empty, returns False
    pickup = gh.handlePickup(t2, arena2)
    assert pickup == False


    food3 = Resource(1, (9, 8), Resource.Type(2))
    arena2.resources.append(food3)
    # inventory full, returns False
    pickup = gh.handlePickup(t2, arena2)
    assert pickup == False


def testHandleEatFood():
    F1 = Resource(1, (5, 5), Resource.Type(3), 1)
    F2 = Resource(1, (5, 5), Resource.Type(3), 1)
    
    T3.inventory = []
    T3.inventory.append(F2)
    T3.inventory.append(F1)

    assert T3.getFood() == 2
    T3.hunger = 10
    result = gh.handleEatFood(T3)
    assert result == True
    T3.hunger = 10
    assert T3.getFood() == 1
    result = False
    result = gh.handleEatFood(T3)
    assert result == True
    result = gh.handleEatFood(T3)
    assert result == False

    result = True
    result = gh.handleEatFood(T0)
    assert result == False


def testHandleDrinkWater():

    # NEED TO RE-WRITE THIS WHOLE TEST WITH AN ARENA TO CONFIRM DRINK WATER
    arena4 = Arena(24)
    T12.pos = (10, 10)
    T13.pos = (10, 15)
    T14.pos = (15, 10)
    arena4.tributes.extend([T12, T13, T14])


    T12.thirst = 10
    T12.water_supply = 2
    result = gh.handleDrinkWater(T12, arena4)
    assert result == True
    T13.thirst = 10
    T13.water_supply = 1
    result = False
    result = gh.handleDrinkWater(T13, arena4)
    assert result == True
    result = gh.handleDrinkWater(T13, arena4)
    assert result == False
    
    result = True
    result = gh.handleDrinkWater(T14, arena4)
    assert result == False

    T12.water_supply = 0
    T12.max_water = 0
    assert result == False
    water = Resource(1, (T12.pos[0], T12.pos[1] + 1), Resource.Type(1))
    arena4.resources.append(water)
    T12.thirst = 50
    result = gh.handleDrinkWater(T12, arena4)
    assert result == True


def testHandleUseMedical():
    M1 = Resource(1, (5, 5), Resource.Type(4))
    M2 = Resource(1, (5, 5), Resource.Type(4))
    T3.inventory = []
    T3.inventory.append(M2)
    T3.inventory.append(M1)

    assert T3.getMedical() == 2
    T3.health = 10
    result = gh.handleUseMedical(T3)
    assert result == True
    result = False
    assert T3.getMedical() == 1
    T3.health = 10
    result = gh.handleUseMedical(T3)
    assert result == True
    result = gh.handleUseMedical(T3)
    assert result == False

    result = True
    result = gh.handleUseMedical(T0)
    assert result == False



def testHandleRefillWater():
    # env setup
    arena2 = Arena(20)
    water = Resource(1, (5, 5), Resource.Type(1))
    not_water = Resource(2, (9, 9), Resource.Type(5))
    arena2.resources.append(water)
    arena2.resources.append(not_water)
    t = Tribute(99, (6, 5))
    arena2.tributes.append(t)
    arena2.arena_grid[6][5] = t.letter
    
    # TEST 1: capacity is at 0 in the beginning, cannot refill
    result = gh.handleRefillWater(t, arena2)
    assert result == False

    t.thirst = 30
    t.max_water = 15
    t.water_supply = 3
    # TEST 2: capacity is 15, water not at max
    result = gh.handleRefillWater(t, arena2)
    assert result == True
    
    result = False
    t.water_supply = 3
    t.thirst = 100
    # TEST 3: thirst does not impact refill
    result = gh.handleRefillWater(t, arena2)
    assert result == True
    
    assert t.water_supply == 15
    # TEST 4: water is already filled, no action completed
    result = gh.handleRefillWater(t, arena2)
    assert result == False

    t.thirst = 30
    t.max_water = 15
    t.water_supply = 3
    t.move(9, 8)

    # TEST 5: different resource
    assert gh.handleRefillWater(t, arena2) == False

    t.move(14, 14)
    # TEST 6: no surroundings
    assert gh.handleRefillWater(t, arena2) == False


def testHandleSingleMove():
    game = th.setupTestArena()
    A = game.players[0]
    B  = game.players[1]
    A_row = A.tribute.pos[0]
    A_col = A.tribute.pos[1]
    result = gh.handleSingleMove(A.tribute, 'left', game.arena)
    assert result == True
    assert A.tribute.pos == (A_row, A_col - 1)
    # to add from survival test when done

    


    


    



    



# def handleSleep():
#     pass

def main():
    testHandleAttack()
    testHandleDrinkWater()
    testHandleEatFood()
    testHandlePickup()
    testHandleUseMedical
    testHandleRefillWater()
    testHandleSingleMove()

if __name__ == '__main__':
    main() 