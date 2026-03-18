import sys
import os

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from Arena import Arena
from Tribute import Tribute
from Resource import Resource
from Game import Game

# setup

game = Game(30)

def testGameSetup():
    assert game.arena.size == 30
    assert game.arena.tributes == []


def testAddTributes():
    
    num_males = 0
    num_females = 0

    game.addTributes(game.arena.center)
    assert len(game.arena.tributes) == 24

    for tribute in game.arena.tributes:
        if tribute.gender == 'male':
            num_males += 1
        else:
            num_females += 1

    # confirm districts
    assert game.arena.tributes[0].district == 1 and game.arena.tributes[1].district == 1
    assert game.arena.tributes[2].district == 2 and game.arena.tributes[3].district == 2
    assert game.arena.tributes[4].district == 3 and game.arena.tributes[5].district == 3
    assert game.arena.tributes[6].district == 4 and game.arena.tributes[7].district == 4
    assert game.arena.tributes[8].district == 5 and game.arena.tributes[9].district == 5
    assert game.arena.tributes[10].district == 6 and game.arena.tributes[11].district == 6
    assert game.arena.tributes[12].district == 7 and game.arena.tributes[13].district == 7
    assert game.arena.tributes[14].district == 8 and game.arena.tributes[15].district == 8
    assert game.arena.tributes[16].district == 9 and game.arena.tributes[17].district == 9
    assert game.arena.tributes[18].district == 10 and game.arena.tributes[19].district == 10
    assert game.arena.tributes[20].district == 11 and game.arena.tributes[21].district == 11
    assert game.arena.tributes[22].district == 12 and game.arena.tributes[23].district == 12

    # confirm 12 males, 12 females
    assert num_males == 12
    assert num_females == 12




def main():
    testGameSetup()
    testAddTributes()



if __name__ == '__main__':
    main()  
    