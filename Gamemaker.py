from config import BOMB_HALF_DAMAGE, BOMB_CENTER_IND
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
        # get target segment
        target = self.findDenseSegment()
        for i in range(len(BOMB_CENTER_IND)):
            index = BOMB_CENTER_IND[i]
            pos = self.arena.segments[target][index]
            self.arena.bomb.positions.append(pos)
            row, col = pos
            if not self.arena.getTributeAt(pos):
                self.arena.arena_grid[row][col] = 4
        
        self.arena.bomb.isDeployed = True
            
    
    def detonate(self):
        if self.arena.bomb.isDeployed:
            segment = self.arena.bomb.segment
            for i, pos in enumerate(self.arena.segments[segment]):
                tribute = self.arena.getTributeAt(pos)
                if tribute:
                    tribute.health -= BOMB_HALF_DAMAGE
                    if i in BOMB_CENTER_IND:
                        tribute.health -= BOMB_HALF_DAMAGE

        self.arena.bomb.isDeployed = False
        self.arena.bomb.segment = None
        self.arena.bomb.positions = []
        

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

    
