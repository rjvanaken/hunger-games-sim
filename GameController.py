from Arena import Arena
from Tribute import Tribute

class GameController:
    
    def __init__(self, size, c_pos=None):
        if c_pos == None:
            c_pos = ((size // 2) - 1, (size // 2) - 1)

        self.arena = Arena(size, c_pos)
        self.tributes = []

    def addTributes(self, pos):
        x = pos[0] - 2
        y = pos[1] - 1
        id = 0
        for i in range(6):
            tribute = Tribute(id, (x, y))
            self.tributes.append(tribute)
            y += 1
            id += 1

        x += 1
        for i in range(6):
            tribute = Tribute(id, (x, y))
            self.tributes.append(tribute)
            x += 1
            id += 1

        y -= 1
        for i in range(6):
            tribute = Tribute(id, (x, y))
            self.tributes.append(tribute)
            y -= 1
            id += 1

        x -= 1
        for i in range(6):
            tribute = Tribute(id, (x, y))
            self.tributes.append(tribute)
            x -= 1
            id += 1

        # check success
        if x == pos[0] - 1 and y == pos[1] - 2:
            print("success")
            print((x, y))
        

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


        

        