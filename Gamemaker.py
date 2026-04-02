from config import BOMB_DAMAGE_FAR, BOMB_DAMAGE_NEAR
from collections import Counter

class Gamemaker:

    def __init__(self, arena):
        self.arena = arena




    '''
    ========================
    TRIGGER MUTT
    ========================
    '''


    def activateMutt(mutt):
        mutt.isDormant = False

  
            
    '''
    ========================
    BLOW UP TIME 
    ========================
    '''

    def deployBomb(self):
        # CREATE bomb object
        bomb = None
        # get target segment
        target = self.findDenseSegment()
        bomb_center = [5, 6, 9, 10]
        for i in range(len(bomb_center)):
            index = bomb_center[i]
            pos = self.arena.segments[target][index]
            bomb.positions.append(pos)
            row, col = pos
            if not self.arena.getTributeAt(pos):
                self.arena.arena_grid[row][col] = 4
        
        return bomb
            


    
    def detonate(self, bomb):

        row, col = pos
            if distance == 0:
                tribute.health = 0 
            elif distance == 1:
                tribute.health -= BOMB_DAMAGE_NEAR
            elif distance == 2:
                tribute.health -= BOMB_DAMAGE_FAR


    def findDenseSegment(self):

        tribute_segments = []
        for tribute in self.arena.tributes:
            tribute_segments.append(tribute.segment)
        
        segment_counts = Counter(tribute_segments).most_common(1)[0][0]

        return segment_counts[0]
    

    '''
    ========================
    SHRINK ARENA - wall
    ========================
    '''

    def shrinkArena(self):
        min_row = self.getShrinkRow()
        min_col, max_col = self.getShrinkColumns()

        for i in range(self.size):
            for j in range(self.size):
                if i < min_row:
                    self.arena.arena_grid[i][j] = 8
                if j < min_col or j > max_col:
                    self.arena.arena_grid[i][j] = 8


    def getShrinkColumns(self):
        min = min(tribute.pos[1] for tribute in self.arena.tributes)
        max = max(tribute.pos[1] for tribute in self.arena.tributes)

        return min, max
             

    def getShrinkRow(self):
        return min(tribute.pos[0] for tribute in self.arena.tributes)

    
