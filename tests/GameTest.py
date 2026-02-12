import sys
import os

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from Arena import Arena
from Tribute import Tribute
from Resource import Resource
from Game import Game

# setup

game = Game(20)

def testSetup():
    assert game.arena.size == 20
    assert game.tributes == []


def testAddTributes():
    
    num_males = 0
    num_females = 0

    game.addTributes(game.arena.center)
    assert len(game.tributes) == 24

    for tribute in game.tributes:
        if tribute.gender == 'male':
            num_males += 1
        else:
            num_females += 1

    # confirm districts
    assert game.tributes[0].district == 1 and game.tributes[1].district == 1
    assert game.tributes[2].district == 2 and game.tributes[3].district == 2
    assert game.tributes[4].district == 3 and game.tributes[5].district == 3
    assert game.tributes[6].district == 4 and game.tributes[7].district == 4
    assert game.tributes[8].district == 5 and game.tributes[9].district == 5
    assert game.tributes[10].district == 6 and game.tributes[11].district == 6
    assert game.tributes[12].district == 7 and game.tributes[13].district == 7
    assert game.tributes[14].district == 8 and game.tributes[15].district == 8
    assert game.tributes[16].district == 9 and game.tributes[17].district == 9
    assert game.tributes[18].district == 10 and game.tributes[19].district == 10
    assert game.tributes[20].district == 11 and game.tributes[21].district == 11
    assert game.tributes[22].district == 12 and game.tributes[23].district == 12

    # confirm 12 males, 12 females
    assert num_males == 12
    assert num_females == 12


def testUpdateTributesList():
    # set variables
    T1 = game.tributes[12]
    T2 = game.tributes[19]
    T3 = game.tributes[2]
    # CHECK INITIAL VALUES
    assert T1.health == 100
    assert T2.health == 100
    assert T3.health == 100
    # subtract health
    T1.health -= 100
    T2.health -= 101
    T3.health -= 99
    # call update list
    game.updateTributesList()

    # test list successfully updated
    assert T1 not in game.tributes
    assert T2 not in game.tributes
    assert T3 in game.tributes


def main():
    testAddTributes()
    testUpdateTributesList()



if __name__ == '__main__':
    main()  
    