import sys
import os
from unittest.mock import patch

import test_helper as th
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

import gameplay_handler as gh
from config import *



def testManualGame():

    # add 3rd tribute to game, set health to low, assert dead, assert not in list, etc.
    game = th.setupTestArena()
    A = game.players[0]
    B = game.players[1]
    A.tribute.hunting_skill = 90
    B.tribute.hunting_skill = 40
    for tribute in game.arena.tributes:
        tribute.arenaKnowledge = game.arena.arena_grid

    # ROUND 1
    A.tribute.updateStatsBeforeTurn()
    gh.handleSingleMove(A.tribute, 'left', game.arena)

    B.tribute.updateStatsBeforeTurn()
    assert len(B.tribute.inventory) == 0
    gh.handleSingleMove(B.tribute, 'down', game.arena)

    # ROUND 2
    A.tribute.updateStatsBeforeTurn()
    gh.handleSingleMove(A.tribute, 'left', game.arena)

    B.tribute.updateStatsBeforeTurn()
    gh.handleSingleMove(B.tribute, 'down', game.arena)

    # ROUND 3
    A.tribute.updateStatsBeforeTurn()
    assert len(A.tribute.inventory) == 0
    assert A.tribute.max_water == 0
    assert gh.handlePickup(A.tribute, game.arena) == True
    # assert large backpack items picked up
    assert A.tribute.countInInventory(3) == LARGE_BACKPACK_FOOD
    assert A.tribute.countInInventory(4) == LARGE_BACKPACK_MED
    assert A.tribute.max_water == CANTEEN_VALUE

    B.tribute.updateStatsBeforeTurn()
    gh.handleSingleMove(B.tribute, 'right', game.arena)


    # ROUND 4:
    A.tribute.updateStatsBeforeTurn()
    gh.handleSingleMove(A.tribute, 'down', game.arena)

    B.tribute.updateStatsBeforeTurn()
    assert len(B.tribute.inventory) == 0
    assert B.tribute.max_water == 0
    gh.handlePickup(B.tribute, game.arena)
    # assert small backpack items picked up
    assert B.tribute.countInInventory(3) == SMALL_BACKPACK_FOOD
    assert B.tribute.countInInventory(4) == SMALL_BACKPACK_MED
    assert B.tribute.max_water == CANTEEN_VALUE


    # ROUND 5: 
    A.tribute.updateStatsBeforeTurn()
    weapon = game.arena.getResourceAt(A.tribute.pos)
    gh.handlePickup(A.tribute, game.arena)
    # assert weapon picked up
    assert A.tribute.weapon_value == weapon.value
    assert A.tribute.strength == A.tribute.base_strength + weapon.value
    assert A.tribute.countInInventory(5) == 1
    assert weapon not in game.arena.resources
    assert game.arena.arena_grid[A.tribute.pos[0]][A.tribute.pos[1]] == 0

    B.tribute.updateStatsBeforeTurn()
    gh.handleSingleMove(B.tribute, 'left', game.arena)

    
    
    # ROUND 6:
    A.tribute.updateStatsBeforeTurn()
    gh.handleSingleMove(A.tribute, 'right', game.arena)

    B.tribute.updateStatsBeforeTurn()
    gh.handleSingleMove(B.tribute, 'left', game.arena)
    
    # ROUND 7:
    A.tribute.updateStatsBeforeTurn()
    gh.handleSingleMove(A.tribute, 'right', game.arena)

    B.tribute.updateStatsBeforeTurn()
    weapon = game.arena.getResourceAt(B.tribute.pos)
    gh.handlePickup(B.tribute, game.arena)
    # assert weapon picked up
    assert B.tribute.weapon_value == weapon.value
    assert B.tribute.strength == B.tribute.base_strength + weapon.value
    assert B.tribute.countInInventory(5) == 1
    assert weapon not in game.arena.resources
    assert game.arena.arena_grid[B.tribute.pos[0]][B.tribute.pos[1]] == 0

    # ROUND 8:
    A.tribute.updateStatsBeforeTurn()
    assert gh.handleSleep(A.tribute) == False # negative sleep case, full health
    gh.handleSingleMove(A.tribute, 'right', game.arena)
    
    B.tribute.updateStatsBeforeTurn()
    assert gh.handleSleep(B.tribute) == False
    gh.handleSingleMove(B.tribute, 'down', game.arena)



    # ROUND 9:
    A.tribute.updateStatsBeforeTurn()
    gh.handleSingleMove(A.tribute, 'right', game.arena)

    B.tribute.updateStatsBeforeTurn()
    gh.handleSingleMove(B.tribute, 'right', game.arena)

    # ROUND 10:
    A.tribute.updateStatsBeforeTurn()
    gh.handleSingleMove(A.tribute, 'up', game.arena)

    B.tribute.updateStatsBeforeTurn()
    assert gh.handlePickup(B.tribute, game.arena) == False
    gh.handleSingleMove(B.tribute, 'up', game.arena)
    assert game.arena.arena_grid[B.tribute.pos[0] + 1][B.tribute.pos[1]] == 5

    # ROUND 11
    A.tribute.updateStatsBeforeTurn()
    assert gh.handlePickup(A.tribute, game.arena) == False
    gh.handleSingleMove(A.tribute, 'right', game.arena)
    assert game.arena.arena_grid[A.tribute.pos[0]][A.tribute.pos[1] - 1] == 5
    gh.handleSingleMove(A.tribute, 'left', game.arena)

    B.tribute.updateStatsBeforeTurn()
    gh.handleSingleMove(B.tribute, 'down', game.arena)
    gh.handleSingleMove(B.tribute, 'down', game.arena)

    # ROUND 12
    A.tribute.updateStatsBeforeTurn()
    assert A.tribute.hunger == 100 - (HUNGER_DECAY * 12)
    assert A.tribute.thirst == 100 - (THIRST_DECAY * 12)
    gh.handleSingleMove(A.tribute, 'down', game.arena)

    B.tribute.updateStatsBeforeTurn()
    assert B.tribute.hunger == 100 - (HUNGER_DECAY * 12)
    assert B.tribute.thirst == 100 - (THIRST_DECAY * 12)
    gh.handleSingleMove(B.tribute, 'l', game.arena)

    # ROUND 13
    A.tribute.updateStatsBeforeTurn()
    gh.handleSingleMove(A.tribute, 'd', game.arena)
    
    B.tribute.updateStatsBeforeTurn()
    gh.handleSingleMove(B.tribute, 'l', game.arena)

    # ROUND 14
    A.tribute.updateStatsBeforeTurn()
    gh.handleSingleMove(A.tribute, 'RIGHT', game.arena)
    
    B.tribute.updateStatsBeforeTurn()
    gh.handleSingleMove(B.tribute, 'l', game.arena)


    # ROUND 15        
    A.tribute.updateStatsBeforeTurn()
    current_food = A.tribute.getFood()
    with patch('random.randint', side_effect=[50, 1, 10]):  # success
        gh.handlePickup(A.tribute, game.arena)
    assert A.tribute.getFood() == current_food + 1
    
    B.tribute.updateStatsBeforeTurn()
    current_food = B.tribute.getFood()
    with patch('random.randint', side_effect=[50, 99]):  # fail
        gh.handlePickup(B.tribute, game.arena)
    assert B.tribute.getFood() == current_food

    

    # ROUNDS 16-25 (10):
    for i in range(10):
        A.tribute.updateStatsBeforeTurn()
        gh.handleSingleMove(A.tribute, 'RIGHT', game.arena)

        B.tribute.updateStatsBeforeTurn()
        gh.handleSingleMove(B.tribute, 'l', game.arena)

    # MODIFICATIONS
    # remove canteen for testing
    for item in B.tribute.inventory:
        if item.type.value == 2:
            B.tribute.inventory.remove(item)
    B.tribute.max_water = 0


    # ROUND 26:
    A.tribute.updateStatsBeforeTurn()
    assert A.tribute.water_supply == 0
    gh.handleRefillWater(A.tribute, game.arena)
    assert A.tribute.water_supply == A.tribute.max_water
    
    B.tribute.updateStatsBeforeTurn()
    assert gh.handleRefillWater(A.tribute, game.arena) == False
    assert gh.handleDrinkWater(B.tribute, game.arena) == True
    assert B.tribute.thirst == 100


    # ROUND 27:
    A.tribute.updateStatsBeforeTurn()
    gh.handleSingleMove(A.tribute, 'left', game.arena)

    B.tribute.updateStatsBeforeTurn()
    gh.handleSingleMove(B.tribute, 'down', game.arena)


    # ROUND 28
    A.tribute.updateStatsBeforeTurn()
    gh.handleDrinkWater(A.tribute, game.arena)
    expected_thirst = max(0, 100 - (THIRST_DECAY * 28)) + WATER_VALUE
    assert A.tribute.thirst == expected_thirst
    assert A.tribute.water_supply == A.tribute.max_water - 1
    
    B.tribute.updateStatsBeforeTurn()
    assert gh.handleDrinkWater(B.tribute, game.arena) == False
    assert B.tribute.thirst == 100 - (THIRST_DECAY * 2)
    

    # ROUND 29
    A.tribute.updateStatsBeforeTurn()
    gh.handleSingleMove(A.tribute, 'right', game.arena)

    B.tribute.updateStatsBeforeTurn()
    gh.handleSingleMove(B.tribute, 'up', game.arena)


    # ROUND 30
    A.tribute.updateStatsBeforeTurn()
    gh.handleDrinkWater(A.tribute, game.arena)
    assert A.tribute.water_supply == A.tribute.max_water - 1

    B.tribute.updateStatsBeforeTurn()
    assert gh.handleSingleMove(B.tribute, 'up', game.arena) == False # cannot walk onto water source
    
    
        # ROUNDS 31-34 (4):
    for i in range(4):
        A.tribute.updateStatsBeforeTurn()
        gh.handleSingleMove(A.tribute, 'left', game.arena)

        B.tribute.updateStatsBeforeTurn()
        gh.handleSingleMove(B.tribute, 'right', game.arena)

    
    # ROUND 35
    A.tribute.updateStatsBeforeTurn()
    gh.handleSingleMove(A.tribute, 'down', game.arena)

    B.tribute.updateStatsBeforeTurn()
    gh.handleSingleMove(B.tribute, 'right', game.arena)

    
    # ROUNDS 36-42
    for i in range(7):
        A.tribute.updateStatsBeforeTurn()
        gh.handleSingleMove(A.tribute, 'down', game.arena)

        B.tribute.updateStatsBeforeTurn()
        gh.handleSingleMove(B.tribute, 'up', game.arena)
    


    # ROUNDS 
    A.tribute.health = 100
    B.tribute.health = 70
    B.tribute.strength = 10
    A.tribute.strength = 20
    A.tribute.isAlive = True
    B.tribute.isAlive = True

    A.tribute.updateStatsBeforeTurn()
    with patch('Tribute.random.random', return_value=0.99):
        gh.handleAttack(A.tribute, game.arena)

    B.tribute.updateStatsBeforeTurn()
    with patch('Tribute.random.random', return_value=0.01):
        gh.handleAttack(B.tribute, game.arena)

    A.tribute.updateStatsBeforeTurn()
    with patch('Tribute.random.random', return_value=0.99):
        gh.handleAttack(A.tribute, game.arena)

    B.tribute.updateStatsBeforeTurn()
    with patch('Tribute.random.random', return_value=0.01):
        gh.handleAttack(B.tribute, game.arena)
    

    game.arena.clearDeadTributes(game)
    assert A.tribute in game.arena.tributes
    assert A.tribute.isAlive == True
    assert B.tribute.isAlive == False

    assert len(game.arena.tributes) == 1

    game.printGameResults()
    assert A.tribute.isAlive == True





    '''
    
    Left side:

Trees: (2, 5), (7, 2), (12, 2)
Water cluster (lower left cell): (19, 4)
Food single: (2, 10), (5, 6), (15, 6)
Food clusters (upper left cell): (3, 10), (8, 8)
Tribute A: (3, 3)
Weapons: (3, 5) 10 value, (4, 1), 20 value
Backpack large (6): (3, 1)

Right side:

Trees: (0, 11), (23, 4)
Water cluster (lower left cell): (5, 17)
Food single: (10, 18), (20, 17)
Food clusters (upper left cell): (11, 17)
Tribute B: (18, 20)
Weapons: (18, 19) 10 value, (19, 20) 20 value
Backpack small (7): (18, 21)
    
    '''




def main():
    testManualGame()



if __name__ == '__main__':
    main()