

class Arena:
    def __init__(self, size):
        self.size = size
        self.center = ((size // 2), (size // 2))
        # x, y are bottom left corner of cornucopia
        x = self.center[0] - 2
        y = self.center[1] - 2

        self.backpacks = [
            (x + 1, y + 1, 10), (x + 3, y + 1, 10), (x + 4, y + 4, 10),
            (x + 3, y, 4), (x + 5, y + 3, 4), (x + 1, y + 5, 4),
        ]

        self.weapons = [
            (x + 4, y + 1, 20), (x + 3, y + 2, 20), (x + 2, y + 2, 20),
            (x + 2, y + 3, 20), (x + 4, y + 3, 20),
            (x, y, 10), (x + 5, y, 10), (x, y + 5, 10), (x + 5, y + 5, 10),
        ]

        self.medical = [
            (x + 2, y + 1, 50), (x + 4, y + 2, 50), 
            (x + 1, y + 3, 50), (x + 3, y + 4, 50),
        ]

        self.water_containers = [
            (x + 2, y, 15), (x + 2, y + 3, 15), (x, y + 3, 15), 
            (x + 5, y + 2, 15), (x + 2, y + 5, 15),
        ]

        self.food = [
            (x + 1, y, 0), (x + 4, y, 0), (x, y + 1, 0), (x + 5, y + 1, 0),
            (x, y + 2, 0), (x + 1, y + 2, 0), (x + 3, y + 3, 0),
            (x, y + 4, 0), (x + 1, y + 4, 0), (x + 2, y + 4, 0), (x + 5, y + 4, 0),
            (x + 3, y + 5, 0), (x + 4, y + 5, 0),
        ]

