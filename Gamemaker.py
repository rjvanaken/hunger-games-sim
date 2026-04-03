from Intervention import Intervention
from config import BOMB_HALF_DAMAGE, BOMB_CENTER_IND, HAZARD_DAMAGE, HAZARD_DAMAGE_PARTIAL, HAZARD_TRIGGER_DISTANCE
from collections import Counter

class Gamemaker:

    def __init__(self, arena):
        self.arena = arena




    def assessInterference(self, game):

        if game.day_count > 0:    
            if self.arena.bomb.isDeployed:
                if game.turn_count - self.arena.bomb.turn_deployed == 2:
                    print("detonate bomb")
                    self.detonate()
                    self.arena.clearDeadTributes(game, gamemaker_kill=True)
                    return
        
            # apply damage - function blocks applying unless isDeployed
            self.applyHazardDamage()
                
            if self.arena.bomb.wasDeployedToday or self.arena.hazard.wasDeployedToday:
                return
            
            if len(self.arena.tributes) > 2:
                if self.arena.bomb.day_deployed is None or game.day_count - self.arena.bomb.day_deployed > 1:
                    if game.deaths_per_day.get(game.day_count, {}).get("combat", 0) == 0:
                        self.arena.bomb.turn_deployed = game.turn_count
                        self.deployBomb(game)
                        return

            if game.day_count >= 2:
                result = self.evaluateAndShrinkArena()
                self.arena.hazard.wasDeployedToday = result

                



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

    def deployBomb(self, game):
        self.arena.bomb.day_deployed = game.day_count
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
                self.arena.arena_grid[row][col] = Intervention.Type.BOMB.value
        
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
        self.arena.bomb.day_deployed
        for pos in self.arena.bomb.positions:
            self.arena.restoreOldCellData(None, pos)
        self.arena.bomb.positions = []
        

    def findDenseSegment(self):
        all_segments = [tribute.segment for tribute in self.arena.tributes]
        tribute_segments = [s for s in all_segments if s is not None]
        if len(tribute_segments) <= 1:
            return None
        return Counter(tribute_segments).most_common(1)[0][0]

    '''
    ========================
    THE STORM IS COMING
    ========================
    '''


    def applyHazardDamage(self):
        if self.arena.hazard.isDeployed:
            for tribute in self.arena.tributes:
                partial_damage = False
                full_damage = False
                row, col = tribute.pos
                full = [(row + 1, col), (row - 1, col), (row, col + 1), (row, col - 1)]
                partial = [(row + 2, col), (row - 2, col), (row, col + 2), (row, col - 2)]
                
                full_damage = any(pos in self.arena.hazard.positions for pos in full)
                partial_damage = not full_damage and any(pos in self.arena.hazard.positions for pos in partial)
                
                if full_damage:
                    tribute.health -= HAZARD_DAMAGE
                    tribute.hazard_damage += HAZARD_DAMAGE
                    print(f"full damage applied to {tribute.letter}")

                elif partial_damage:
                    tribute.health -= HAZARD_DAMAGE_PARTIAL
                    tribute.hazard_damage += HAZARD_DAMAGE_PARTIAL
                    print(f"Partial damage applied to {tribute.letter}")
 
                    #may figure out how to use the hazard count later, leaving for now
                        
        self.arena.clearDeadTributes(self, gamemaker_kill=True)


        
    def evaluateAndShrinkArena(self):
        min_row, max_row = self.getShrinkRow()
        min_col, max_col = self.getShrinkColumns()

        spread = (max_col - min_col + max_row - min_row) / len(self.arena.tributes)
        if spread > HAZARD_TRIGGER_DISTANCE:
            self.shrinkArena(min_row, max_row, min_col, max_col)
            print("placed wall") # temp DEBUG
            return True


    def shrinkArena(self, min_row, max_row, min_col, max_col):

        for i in range(self.arena.size):
            for j in range(self.arena.size):
                if i < min_row or i > max_row:
                    self.arena.hazard.positions.append((i, j))
                    self.arena.arena_grid[i][j] = Intervention.Type.HAZARD.value
                if j < min_col or j > max_col:
                    self.arena.hazard.positions.append((i, j))
                    self.arena.arena_grid[i][j] = Intervention.Type.HAZARD.value

        self.arena.hazard.positions = list(set(self.arena.hazard.positions))


    def getShrinkColumns(self):
        min_col = min(tribute.pos[1] for tribute in self.arena.tributes)
        max_col = max(tribute.pos[1] for tribute in self.arena.tributes)

        return min_col, max_col
             

    def getShrinkRow(self):
        min_row = min(tribute.pos[0] for tribute in self.arena.tributes)
        max_row = max(tribute.pos[0] for tribute in self.arena.tributes)
        
        return min_row, max_row

    
