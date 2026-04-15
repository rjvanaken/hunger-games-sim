"""
Arena.py - defines the Arena class, which houses all elements of the game. A single arena is created
per game and is represented as a nested array.

CITATIONS:
    - Pillow (PIL): used for image processing / frame rendering
"""



from Intervention import Intervention
from Resource import Resource
import random
import gameplay_handler as gh
from config import *
from PIL import Image, ImageDraw, ImageFont

class Arena:

    """
    Represents the Arena class, which houses everything that would be used within the Arena environment.    
    """
    def __init__(self, size):
        self.size = size
        self.center = ((size // 2) - 1, (size // 2) - 1)
        self.next_resource_id = 0
        self.arena_grid = [[0 for _ in range(size)] for _ in range(size)]  # Start empty
        # x, y are bottom left corner of cornucopia
        self.num_tributes = 24
        self.resources = []
        self.obstacles = []
        self.tributes = []
        self.segments = {}
        self.mutts = []
        self.hazards = []
        self.cornucopia = []
        self.bomb = Intervention(Intervention.Type.BOMB, positions=[], damage=BOMB_HALF_DAMAGE)
        self.hazard = Intervention(Intervention.Type.HAZARD, positions=[], damage=HAZARD_DAMAGE, pos=None)



        # build out segment coordinates
        i = 1
        num_segments = size // 4
        for row in range(num_segments):
            for col in range(num_segments):
                    start_row = row * 4
                    start_col = col * 4
                    coords = []
                    for r in range(start_row, start_row + 4):
                        for c in range(start_col, start_col + 4):
                            coords.append((r, c))
                    self.segments[i] = coords
                    i += 1



    def addCornucopia(self):

        """
        Creates all Resource objects for the cornucopia area and places them inside the arena
        """

        rows = self.center[0] - 2
        cols = self.center[1] - 2
        
        
        # top
        Resource.addResource(self, (rows, cols), Resource.Type(5), self.resources, WEAK_WEAPON)
        
        Resource.addResource(self, (rows, cols + 1), Resource.Type(5), self.resources, WEAK_WEAPON)
        Resource.addResource(self, (rows, cols + 2), Resource.Type(6), self.resources)

        Resource.addResource(self, (rows, cols + 4), Resource.Type(5), self.resources, WEAK_WEAPON)



        # row 2
        Resource.addResource(self, (rows + 1, cols), Resource.Type(5), self.resources, WEAK_WEAPON)

        Resource.addResource(self, (rows + 1, cols + 2), Resource.Type(5), self.resources, STRONG_WEAPON)
        Resource.addResource(self, (rows + 1, cols + 3), Resource.Type(7), self.resources)

        Resource.addResource(self, (rows + 1, cols + 5), Resource.Type(6), self.resources)


        # row 3
        Resource.addResource(self, (rows + 2, cols), Resource.Type(6), self.resources)
        Resource.addResource(self, (rows + 2, cols + 1), Resource.Type(7), self.resources)
        
        
        Resource.addResource(self, (rows + 2, cols + 4), Resource.Type(5), self.resources, STRONG_WEAPON)
        

        
        # row 4
        Resource.addResource(self, (rows + 3, cols + 2), Resource.Type(5), self.resources, STRONG_WEAPON)

        Resource.addResource(self, (rows + 3, cols + 4), Resource.Type(7), self.resources)
        Resource.addResource(self, (rows + 3, cols + 5), Resource.Type(5), self.resources, WEAK_WEAPON)


        # row 5
        Resource.addResource(self, (rows + 4, cols), Resource.Type(6), self.resources)
        
        Resource.addResource(self, (rows + 4, cols + 2), Resource.Type(7), self.resources)
        Resource.addResource(self, (rows + 4, cols + 3), Resource.Type(5), self.resources, STRONG_WEAPON)
        
        

        # row 6
        Resource.addResource(self, (rows + 5, cols), Resource.Type(5), self.resources, WEAK_WEAPON)

        Resource.addResource(self, (rows + 5, cols + 2), Resource.Type(6), self.resources)

        Resource.addResource(self, (rows + 5, cols + 4), Resource.Type(6), self.resources)
        Resource.addResource(self, (rows + 5, cols + 5), Resource.Type(5), self.resources, WEAK_WEAPON)
        

        for resource in self.resources:
            self.arena_grid[resource.pos[0]][resource.pos[1]] = resource.type.value
            self.cornucopia.append(resource.pos)





    def addTrees(self, density=0.3):
        """
        adds 8s to the arena to represent trees
        Used in tests
        """

        center_row = self.center[0]
        center_col = self.center[1]
        
        for i in range(self.size):
            for j in range(self.size):
                # Skip cornucopia zone
                if (center_row - 9 <= i <= center_row + 9 and 
                    center_col - 9 <= j <= center_col + 9):
                    continue
                
                # Skip if already occupied (check the grid)
                if self.arena_grid[i][j] != 0:
                    continue
                
                if random.random() < density:
                    self.obstacles.append((i, j))
                    self.arena_grid[i][j] = 8  # 8 = tree



    def addSources(self):
        """
        Creates water sources and adds them to the arena
        Used in tests
        """
        Resource.addResource(self, (6, 6), Resource.Type(1), self.resources)
        Resource.addResource(self, (6, 7), Resource.Type(1), self.resources)
        Resource.addResource(self, (6, 8), Resource.Type(1), self.resources)
        Resource.addResource(self, (6, 9), Resource.Type(1), self.resources)
        Resource.addResource(self, (6, 10), Resource.Type(1), self.resources)
        Resource.addResource(self, (7, 6), Resource.Type(1), self.resources)
        Resource.addResource(self, (7, 7), Resource.Type(1), self.resources)
        Resource.addResource(self, (7, 8), Resource.Type(1), self.resources)
        Resource.addResource(self, (8, 9), Resource.Type(1), self.resources)
        Resource.addResource(self, (8, 8), Resource.Type(1), self.resources)
        Resource.addResource(self, (8, 7), Resource.Type(1), self.resources)
        Resource.addResource(self, (8, 6), Resource.Type(1), self.resources)
        Resource.addResource(self, (8, 5), Resource.Type(1), self.resources)
        Resource.addResource(self, (8, 4), Resource.Type(1), self.resources)
        Resource.addResource(self, (9, 9), Resource.Type(1), self.resources)
        Resource.addResource(self, (10, 9), Resource.Type(1), self.resources)
        Resource.addResource(self, (9, 10), Resource.Type(1), self.resources)
        Resource.addResource(self, (10, 10), Resource.Type(1), self.resources)


        for resource in self.resources:
            self.arena_grid[resource.pos[0]][resource.pos[1]] = resource.type.value



    def getResourceAt(self, pos):
        """
        Gets the resource at the provided position. If none, return None
        """
        for resource in self.resources:
            if resource.pos == pos:
                return resource
        return None
        

    def getSegmentFromPos(self, pos):
        """
        Gets the segment by the arena position
        """
        for key, value in self.segments.items():
            if pos in value:
                return key
        return list(self.segments.keys())[0] 
        

    def clearDeadTributes(self, game, gamemaker_kill=False):
        """
        Clears all the tributes flagged as dead from the arena
        """
        new_list = []
        for tribute in self.tributes:
            pos = tribute.pos 
            if tribute.isAlive:
                new_list.append(tribute)
            else:
                print(f"Tribute {tribute.letter} has died")
                self.restoreOldCellData(tribute, pos)
                tribute.pos = None
                if game.day_count == 0:
                    game.day_one_kills += 1
                if gamemaker_kill or tribute.hazard_death:
                    game.deaths_by_gamemaker += 1
                    game.deaths_per_day[game.day_count + 1]["gamemaker"] += 1
                elif tribute.recently_attacked:
                    game.deaths_by_combat += 1
                    game.deaths_per_day[game.day_count + 1]["combat"] += 1
                else:
                    game.deaths_by_decay += 1
                    game.deaths_per_day[game.day_count + 1]["decay"] += 1
                self.num_tributes -= 1
        self.tributes = new_list


    def clearDeadMutts(self):
        """
        Clears the dead mutts from the Arena 
        (not currently implemented)
        """
        new_list = []
        for mutt in self.mutts:
            pos = mutt.pos 
            if mutt.isAlive:
                new_list.append(mutt)
            else:
                self.restoreOldCellData(mutt, pos)
                mutt.pos = None
        self.mutts = new_list


    def displayArena(self, colors=False):
        """
        Displays the arena in the terminal:
            - 0: represented by dots in the arena, indicates an empty cell
            - 1: water source
            - 2: hazard wall
            - 3: food item
            - 4: bomb, represented by an orange * in the arena on detonation
            - 5: weapons
            - 6: small backpack
            - 7: large backpack
            - 8: tree or obstacle
            - A-X: the 24 tributes represented by their letter attribute
        
        """
        for i in range(self.size):
            for j in range(self.size):
                cell_value = self.arena_grid[i][j]
                
                if cell_value == 0:
                    print('.', end=' ')
                elif isinstance(cell_value, str):
                    tribute = next((t for t in self.tributes if t.letter == cell_value), None)
                    if tribute:
                        if colors:
                            c = COLORS[tribute.id % len(COLORS)]
                            print(f"{c}{cell_value}{RESET}", end=' ')
                        else:
                            print(f"{tribute.letter}", end=' ')
                            
                    else:
                        print(cell_value, end=' ')
                else:
                    print(cell_value, end=' ')
            print()
 


    def updateSegmentData(self, tribute, segment):
        """
        Update the tribute's knowledge of the arena in their current segment with data from the main arena grid
        """

        for (row, col) in self.segments[segment]:
            tribute.arenaKnowledge[row][col] = self.arena_grid[row][col]



    def moveTribute(self, tribute, row, col):
        '''
        Moves the tribute and updates their location in the grid storage
        '''
        # needs to be modified to go TOWARD said location instead
        # of immediately there. The udlr moves will update the grid

        old_row = tribute.pos[0]
        old_col = tribute.pos[1]
        self.arena_grid[old_row][old_col] = 0
        tribute.move(row, col)
        self.arena_grid[row][col] = tribute.letter


    def removeResource(self, resource):
        '''
        Run after pickup resource. 
        Removes the resource from the resources list, grid, and 
        changes id and pos to None
        '''
        self.resources.remove(resource)
        self.arena_grid[resource.pos[0]][resource.pos[1]] = 0
        resource.pos = None
        resource.id = None


    def restoreOldCellData(self, tribute, pos):
        """
        When a tribute leaves a cell, if there was something else on the cell when they walked onto the cell, 
        restore that appropriate object.
        Display Heirarchy: tributes, hazards, resources

        """

        # restore old cell - if it had a resource put it back, otherwise 0
        row, col = pos
        resource = self.getResourceAt(pos)

        
        if pos in self.hazard.positions:
            self.arena_grid[row][col] = Intervention.Type.HAZARD.value

        elif any(h.pos == pos for h in self.hazards):
            self.arena_grid[row][col] = Intervention.Type.HAZARD.value
            
        elif resource:
            self.arena_grid[row][col] = resource.type.value
        
        else:
            self.arena_grid[row][col] = 0

        # 
        if tribute:
            if tribute.isAlive:
                self.arena_grid[tribute.pos[0]][tribute.pos[1]] = tribute.letter



    def getTarget(self, tribute, attack=False):
        """
        finds a target for the given tribute in adjacent cells
        """

        target = None

        if attack:
            target = gh.checkNeighborsFor(tribute, self, find_tribute=True)
        else:     
            for t in self.tributes:
                if t.pos == tribute.pos and tribute != t:
                    target = t
                    break
            for m in self.mutts:
                if m.pos == tribute.pos:
                    target = m
                    break
        return target

    def getTributeAt(self, pos):
        """
        Retrieves the tribute at the given position.
        """
        for tribute in self.tributes:
            if tribute.pos == pos:
                return tribute
        return None



    def renderTurnFrames(self, turn_num, day_num):
        """
        captures the arena at the start of a turn and renders it into an image.
        used to create the games gif.
        """
        
        font = ImageFont.load_default()
        char_w, char_h = 6, 10

        img = Image.new("RGB", (self.size * char_w * 2, self.size * char_h + 20), (0, 0, 0))
        draw = ImageDraw.Draw(img)

        draw.text((2, 0), f"Day {day_num} | Turn {turn_num}", fill=(200, 200, 200), font=font)

        for i in range(self.size):
            for j in range(self.size):
                cell_value = self.arena_grid[i][j]

                if cell_value == 0:
                    ch = '.'
                    color = (20, 20, 20)
                elif isinstance(cell_value, str):
                    tribute = next((t for t in self.tributes if t.letter == cell_value), None)
                    ch = cell_value
                    color = (255, 220, 50) if tribute else (150, 150, 150)
                elif cell_value == 2:
                    ch = '░'
                    color = (255, 105, 180)  # pink storm
                elif cell_value == 4:
                    ch = '*'
                    color = (255, 140, 0)  # orange bomb
                else:
                    ch = str(cell_value)
                    color = (80, 80, 80)  # walls, terrain numbers, etc.

                x = j * char_w * 2  # *2 for the space
                y = i * char_h + 20
                draw.text((x, y), ch, fill=color, font=font)
        return img
    