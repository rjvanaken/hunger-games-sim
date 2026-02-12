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
        if tribute.gender == 'female':
            num_females += 1

    assert num_males == 12
    assert num_females == 12



def main():
    testAddTributes()



if __name__ == '__main__':
    main()  
    