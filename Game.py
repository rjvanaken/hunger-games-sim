from Arena import Arena
from Tribute import Tribute
from Resource import Resource

class Game:
    
    def __init__(self, size):

        self.arena = Arena(size)
        self.tributes = []



    def addTributes(self, pos):
        center_row = pos[0]
        center_col = pos[1]
        id = 0
        
        # top row - 6 tributes (skip corners at -4 and +3)
        row = center_row - 4
        for col in range(center_col - 2, center_col + 4):
            tribute = Tribute(id, (row, col))
            self.tributes.append(tribute)
            self.arena.arena_grid[row][col] = tribute.letter
            id += 1
        
        # right column - 6 tributes (skip corners at -4 and +3)
        col = center_col + 5
        for row in range(center_row - 2, center_row + 4):
            tribute = Tribute(id, (row, col))
            self.tributes.append(tribute)
            self.arena.arena_grid[row][col] = tribute.letter
            id += 1
        
        # bottom row - 6 tributes (skip corners at +3 and -4)
        row = center_row + 5
        for col in range(center_col + 3, center_col - 3, -1):
            tribute = Tribute(id, (row, col))
            self.tributes.append(tribute)
            self.arena.arena_grid[row][col] = tribute.letter
            id += 1
        
        # left column - 6 tributes (skip corners at +3 and -4)
        col = center_col - 4
        for row in range(center_row + 3, center_row - 3, -1):
            tribute = Tribute(id, (row, col))
            self.tributes.append(tribute)
            self.arena.arena_grid[row][col] = tribute.letter
            id += 1

    

    def displayGrid(self):
        for i in range(self.arena.size):
            for j in range(self.arena.size):
                cell_value = self.arena.arena_grid[i][j]
                
                if cell_value == 0:
                    print('.', end=' ')
                else:
                    print(cell_value, end=' ')
            print()  # New line after each row




    # # TODO do json import and then simplify display function
    # def displayGrid(self):
    #     for i in range(self.arena.size):
    #         for j in range(self.arena.size):
    #             # Check resources
    #             resource_found = False
    #             for resource in self.arena.resources:
    #                 if resource.pos == (i, j):
    #                     print(resource.type.value, end=' ')
    #                     resource_found = True
    #                     break
    #             if resource_found:
    #                 continue
    #             # Check obstacles
    #             obstacle_found = False
    #             for pos in self.arena.obstacles:
    #                 if pos == (i, j):
    #                     print('8', end=' ')
    #                     obstacle_found = True
    #                     break
    #             if obstacle_found:
    #                 continue
    #             # Check tributes
    #             tribute_found = False
    #             for tribute in self.tributes:
    #                 if tribute.pos == (i, j):
    #                     print(tribute.letter, end=' ')
    #                     tribute_found = True
    #                     break
    #             if tribute_found:
    #                 continue
                    
    #             # Nothing found
    #             print('.', end=' ')
    #         print()  # New line after each row


        

        