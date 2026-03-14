import sys
import os

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)


from Tribute import Tribute
import test_helper as th
import gameplay_handler as gh



def testSurvival():
    game, A, B = th.setupTestArena()
    A_row = A.tribute.pos[0]
    A_col = A.tribute.pos[1]
    result = gh.handleSingleMove(A.tribute, 'left')
    assert result == True
    assert A.tribute.pos == (A_row, A_col - 1)

    '''
    
    Left side:

Trees: (2, 5), (7, 2), (12, 2)
Water cluster (lower left cell): (19, 4)
Food single: (2, 10), (5, 6), (15, 6)
Food clusters (upper left cell): (3, 10), (8, 8)
Tribute A: (3, 3)
Weapons: (3, 5), (4, 1)
Backpack large (6): (3, 1)

Right side:

Trees: (0, 11), (23, 4)
Water cluster (lower left cell): (5, 17)
Food single: (10, 18), (20, 17)
Food clusters (upper left cell): (11, 17)
Tribute B: (18, 20)
Weapons: (18, 19), (19, 20)
Backpack small (7): (18, 21)
    
    '''




def main():
    testSurvival()



if __name__ == '__main__':
    main()  