from Resource import Resource
import random

class Arena:
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



    def addCornucopia(self):

        rows = self.center[0] - 2
        cols = self.center[1] - 2
        
        
        # top
        Resource.addResource(self, (rows, cols), Resource.Type(5), self.resources, 10)
        
        Resource.addResource(self, (rows, cols + 1), Resource.Type(5), self.resources, 10)
        Resource.addResource(self, (rows, cols + 2), Resource.Type(6), self.resources)

        Resource.addResource(self, (rows, cols + 4), Resource.Type(5), self.resources, 10)



        # row 2
        Resource.addResource(self, (rows + 1, cols), Resource.Type(5), self.resources, 10)

        Resource.addResource(self, (rows + 1, cols + 2), Resource.Type(5), self.resources, 20)
        Resource.addResource(self, (rows + 1, cols + 3), Resource.Type(7), self.resources)

        Resource.addResource(self, (rows + 1, cols + 5), Resource.Type(6), self.resources)


        # row 3
        Resource.addResource(self, (rows + 2, cols), Resource.Type(6), self.resources)
        Resource.addResource(self, (rows + 2, cols + 1), Resource.Type(7), self.resources)
        
        
        Resource.addResource(self, (rows + 2, cols + 4), Resource.Type(5), self.resources, 20)
        

        
        # row 4
        Resource.addResource(self, (rows + 3, cols + 2), Resource.Type(5), self.resources, 20)

        Resource.addResource(self, (rows + 3, cols + 4), Resource.Type(7), self.resources)
        Resource.addResource(self, (rows + 3, cols + 5), Resource.Type(5), self.resources, 10)


        # row 5
        Resource.addResource(self, (rows + 4, cols), Resource.Type(6), self.resources)
        
        Resource.addResource(self, (rows + 4, cols + 2), Resource.Type(7), self.resources)
        Resource.addResource(self, (rows + 4, cols + 3), Resource.Type(5), self.resources, 20)
        
        

        # row 6
        Resource.addResource(self, (rows + 5, cols), Resource.Type(5), self.resources, 10)

        Resource.addResource(self, (rows + 5, cols + 2), Resource.Type(6), self.resources)

        Resource.addResource(self, (rows + 5, cols + 4), Resource.Type(6), self.resources)
        Resource.addResource(self, (rows + 5, cols + 5), Resource.Type(5), self.resources, 10)
        

        for resource in self.resources:
            self.arena_grid[resource.pos[0]][resource.pos[1]] = resource.type.value

        #todo: add more later, need 4 more spots

    def updateCornucopiaItems(self):
        new_list = []
        for resource in self.resourses:
            if resource.isTaken:
                new_list.append(resource)
            else:
                row, col = resource.pos
                self.arena.arena_grid[row][col] = 0
        self.resources = new_list

    def addTrees(self, density=0.3):
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
        # body of water
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
        for resource in self.resources:
            if resource.pos == pos:
                return resource
        return None
        

    def clearDeadTributes(self):
        new_list = []
        for tribute in self.tributes:
            if tribute.isAlive:
                new_list.append(tribute)
            else:
                row, col = tribute.pos
                self.arena_grid[row][col] = 0
                self.num_tributes -= 1
        self.tributes = new_list

    def displayArena(self):
        for i in range(self.size):
            for j in range(self.size):
                cell_value = self.arena_grid[i][j]
                
                if cell_value == 0:
                    print('.', end=' ')
                else:
                    print(cell_value, end=' ')
            print()  # New line after each row


    def moveTribute(self, tribute, row, col):
        old_row = tribute.pos[0]
        old_col = tribute.pos[1]
        self.arena_grid[old_row][old_col] = 0
        tribute.move(row, col)
        self.arena_grid[row][col] = tribute.letter