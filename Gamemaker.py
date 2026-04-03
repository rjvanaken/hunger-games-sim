from config import BOMB_HALF_DAMAGE, BOMB_CENTER_IND, WALL_TRIGGER_DISTANCE
from collections import Counter

class Gamemaker:

    def __init__(self, arena):
        self.arena = arena




    def assessInterference(self, game):
        if len(self.arena.tributes) > 2:
            if not self.arena.bomb.wasDeployedToday:
            # if bomb deployed and the deploy delay has passed, detonate bomb
                if self.arena.bomb.isDeployed:
                    if game.turn_count - self.arena.bomb.turn_deployed == 2:
                        print("detonate bomb")
                        self.detonate()
                        self.arena.clearDeadTributes(game, gamemaker_kill=True)

                elif game.day_count > 0 and game.deaths_per_day.get(game.day_count, 0) == 0:
                    self.arena.bomb.turn_deployed = game.turn_count
                    self.deployBomb()

        # perhaps if not greater than 2, we do a wall instead?

        if game.day_count >= 2:
            result = self.evaluateAndShrinkArena()
            game.placed_wall_today = result
            

            




        # add other checks - something about kill type? if not a lot of combat kills, shrink arena?


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
        self.arena.bomb.wasDeployedToday = True
        # get target segment
        target = self.findDenseSegment()
        if not target:
            return
            # if should not drop bomb then do not deploy
        self.arena.bomb.segment = target
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
        all_segments = [tribute.segment for tribute in self.arena.tributes]
        tribute_segments = [s for s in all_segments if s is not None]
        if len(tribute_segments) <= 1:
            return None
        return Counter(tribute_segments).most_common(1)[0][0]

    '''
    ========================
    SHRINK ARENA - wall
    ========================
    '''

    def evaluateAndShrinkArena(self):
        min_row, max_row = self.getShrinkRow()
        min_col, max_col = self.getShrinkColumns()

        spread = (max_col - min_col + max_row - min_row) / len(self.arena.tributes)
        if spread > WALL_TRIGGER_DISTANCE:
            self.shrinkArena(min_row, max_row, min_col, max_col)
            print("placed wall") # temp DEBUG
            return True


    def shrinkArena(self, min_row, max_row, min_col, max_col):

        for i in range(self.arena.size):
            for j in range(self.arena.size):
                if i < min_row or i > max_row:
                    self.arena.arena_grid[i][j] = 8
                if j < min_col or j > max_col:
                    self.arena.arena_grid[i][j] = 8


    def getShrinkColumns(self):
        min_col = min(tribute.pos[1] for tribute in self.arena.tributes)
        max_col = max(tribute.pos[1] for tribute in self.arena.tributes)

        return min_col, max_col
             

    def getShrinkRow(self):
        min_row = min(tribute.pos[0] for tribute in self.arena.tributes)
        max_row = max(tribute.pos[0] for tribute in self.arena.tributes)
        
        return min_row, max_row

    
