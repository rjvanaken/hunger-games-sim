import sys
import os

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from Game import Game
from Arena import Arena

game = Game(30)

def testClearDeadTributes(game):
    game.addTributes(game.arena.center, False)
    
    T1 = game.arena.tributes[12]
    T2 = game.arena.tributes[19]
    T3 = game.arena.tributes[2]
    
    assert T1.health == 100
    assert T2.health == 100
    assert T3.health == 100
    
    T1.health -= 100
    T2.health -= 101
    T3.health -= 99

    T1.isAlive = False
    T2.isAlive = False

    T1_pos = T1.pos
    T2_pos = T2.pos
    game.arena.clearDeadTributes(game)

    assert T1 not in game.arena.tributes
    assert T2 not in game.arena.tributes
    assert T3 in game.arena.tributes
    assert game.arena.arena_grid[T1_pos[0]][T1_pos[1]] == 0
    assert game.arena.arena_grid[T2_pos[0]][T2_pos[1]] == 0


def main():
    testClearDeadTributes(game)



if __name__ == '__main__':
    main()  