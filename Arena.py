from Resource import Resource

class Arena:
    def __init__(self, size):
        self.size = size
        self.center = ((size // 2) - 1, (size // 2) - 1)
        self.next_resource_id = 0
        # x, y are bottom left corner of cornucopia
        
        self.resources = []



    def addCornucopia(self):

        rows = self.center[0] - 2
        cols = self.center[1] - 2
        
        
        # bottom row
        Resource.addResource(self, (rows, cols + 1), Resource.Type(5), self.resources, 10)
        Resource.addResource(self, (rows, cols + 2), Resource.Type(6), self.resources)

        Resource.addResource(self, (rows, cols + 4), Resource.Type(5), self.resources, 10)



        # row 2
        Resource.addResource(self, (rows - 1, cols), Resource.Type(5), self.resources, 10)

        Resource.addResource(self, (rows - 1, cols + 2), Resource.Type(5), self.resources, 20)
        Resource.addResource(self, (rows - 1, cols + 3), Resource.Type(7), self.resources)

        Resource.addResource(self, (rows - 1, cols + 5), Resource.Type(6), self.resources)


        # row 3
        Resource.addResource(self, (rows - 2, cols), Resource.Type(6), self.resources)
        Resource.addResource(self, (rows - 2, cols + 1), Resource.Type(7), self.resources)
        
        
        Resource.addResource(self, (rows - 2, cols + 4), Resource.Type(5), self.resources, 20)
        

        
        # row 4
        Resource.addResource(self, (rows - 3, cols + 2), Resource.Type(5), self.resources, 20)

        Resource.addResource(self, (rows - 3, cols + 4), Resource.Type(7), self.resources)
        Resource.addResource(self, (rows - 3, cols + 5), Resource.Type(5), self.resources, 10)


        # row 5
        Resource.addResource(self, (rows - 4, cols), Resource.Type(6), self.resources)
        
        Resource.addResource(self, (rows - 4, cols + 2), Resource.Type(7), self.resources)
        Resource.addResource(self, (rows - 4, cols + 3), Resource.Type(5), self.resources, 20)
        
        

        # row 6
        Resource.addResource(self, (rows - 5, cols), Resource.Type(5), self.resources, 10)

        Resource.addResource(self, (rows - 5, cols + 2), Resource.Type(6), self.resources)

        Resource.addResource(self, (rows - 5, cols + 4), Resource.Type(6), self.resources)
        Resource.addResource(self, (rows - 5, cols + 5), Resource.Type(5), self.resources, 10)
        
        #todo: add more later, need 4 more spots



