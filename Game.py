from Arena import Arena
from Tribute import Tribute
from Resource import Resource
from Player import Player, HumanPlayer #, BotPlayer

class Game:
    
    def __init__(self, size):

        self.arena = Arena(size)
        self.tributes = []
        self.players = []



    def addTributes(self, pos):
        center_row = pos[0]
        center_col = pos[1]
        id = 0
        
        # top row - 6 tributes (skip corners at -4 and +3)
        row = center_row - 4
        for col in range(center_col - 2, center_col + 4):
            tribute = Tribute(id, (row, col))
            player = HumanPlayer(self.arena, tribute)
            self.players.append(player)
            self.tributes.append(tribute)
            self.arena.arena_grid[row][col] = tribute.letter
            id += 1
        
        # right column - 6 tributes (skip corners at -4 and +3)
        col = center_col + 5
        for row in range(center_row - 2, center_row + 4):
            tribute = Tribute(id, (row, col))
            player = HumanPlayer(self.arena, tribute)
            self.players.append(player)
            self.tributes.append(tribute)
            self.arena.arena_grid[row][col] = tribute.letter
            id += 1
        
        # bottom row - 6 tributes (skip corners at +3 and -4)
        row = center_row + 5
        for col in range(center_col + 3, center_col - 3, -1):
            tribute = Tribute(id, (row, col))
            player = HumanPlayer(self.arena, tribute)
            self.players.append(player)
            self.tributes.append(tribute)
            self.arena.arena_grid[row][col] = tribute.letter
            id += 1
        
        # left column - 6 tributes (skip corners at +3 and -4)
        col = center_col - 4
        for row in range(center_row + 3, center_row - 3, -1):
            tribute = Tribute(id, (row, col))
            player = HumanPlayer(self.arena, tribute)
            self.players.append(player)
            self.tributes.append(tribute)
            self.arena.arena_grid[row][col] = tribute.letter
            id += 1
        
        
    def clearDeadTributes(self):
        new_list = []
        for tribute in self.tributes:
            if tribute.isAlive:
                new_list.append(tribute)
            else:
                row, col = tribute.pos
                self.arena.arena_grid[row][col] = 0
                self.arena.num_tributes -= 1
        self.tributes = new_list


    def displayGrid(self):
        for i in range(self.arena.size):
            for j in range(self.arena.size):
                cell_value = self.arena.arena_grid[i][j]
                
                if cell_value == 0:
                    print('.', end=' ')
                else:
                    print(cell_value, end=' ')
            print()  # New line after each row

