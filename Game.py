from Arena import Arena
from Tribute import Tribute

class Game:
    
    def __init__(self, size):

        self.arena = Arena(size)
        self.tributes = []



    def addTributes(self, pos):
        center_row = pos[0]
        center_col = pos[1]
        id = 0
        
        # top row - 6 tributes (skip corners at -4 and +3)
        row = center_row - 3
        for col in range(center_col - 2, center_col + 4):
            tribute = Tribute(id, (row, col))
            self.tributes.append(tribute)
            id += 1
        
        # right column - 6 tributes (skip corners at -4 and +3)
        col = center_col + 4
        for row in range(center_row - 2, center_row + 4):
            tribute = Tribute(id, (row, col))
            self.tributes.append(tribute)
            id += 1
        
        # bottom row - 6 tributes (skip corners at +3 and -4)
        row = center_row + 4
        for col in range(center_col + 3, center_col - 3, -1):
            tribute = Tribute(id, (row, col))
            self.tributes.append(tribute)
            id += 1
        
        # left column - 6 tributes (skip corners at +3 and -4)
        col = center_col - 3
        for row in range(center_row + 3, center_row - 3, -1):
            tribute = Tribute(id, (row, col))
            self.tributes.append(tribute)
            id += 1
    

    def displayGrid(self):
        for i in range(self.arena.size):
            for j in range(self.arena.size):
                tribute_here = None
                for tribute in self.tributes:
                    if tribute.pos == (i, j):
                        tribute_here = tribute
                        break
                if tribute_here:
                    print(tribute_here.letter, end=' ')
                else:
                    print(".", end=' ')
            print()


        

        