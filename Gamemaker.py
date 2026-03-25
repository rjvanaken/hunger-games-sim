from config import BOMB_DAMAGE_FAR, BOMB_DAMAGE_NEAR

class Gamemaker:

    def __init__(self, arena):
        self.arena = arena


    def shrinkArena(self):
        min_row = self.getShrinkRow()
        min_col, max_col = self.getShrinkColumns()

        for i in range(self.size):
            for j in range(self.size):
                if i < min_row:
                    self.arena.arena_grid[i][j] = 8
                if j < min_col or j > max_col:
                    self.arena.arena_grid[i][j] = 8
                

    def activateMutt(mutt):
        mutt.isDormant = False


    def deployBomb(self, pos):
        row, col = pos
        for tribute in self.arena.tributes:
            dr = abs(tribute.pos[0] - row)
            dc = abs(tribute.pos[1] - col)
            distance = max(dr, dc) 
            
            if distance == 0:
                tribute.health = 0 
            elif distance == 1:
                tribute.health -= BOMB_DAMAGE_NEAR
            elif distance == 2:
                tribute.health -= BOMB_DAMAGE_FAR
    



    def getShrinkColumns(self):
        min = min(tribute.pos[1] for tribute in self.arena.tributes)
        max = max(tribute.pos[1] for tribute in self.arena.tributes)

        return min, max
             

    def getShrinkRow(self):
        return min(tribute.pos[0] for tribute in self.arena.tributes)

    
