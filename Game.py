from Arena import Arena
from Tribute import Tribute
from Resource import Resource
from config import *
from Player import Player, HumanPlayer, BotPlayer
import gymnasium as gym
from gymnasium import spaces
import numpy as np
import gameplay_handler as gh

class Game():
    
    def __init__(self, size, robot=False, train=False, test=False):    

        self.arena = Arena(size)
        self.players = []
        self.turn_count = 0
        self.day_count = 0
        self.drama = 0
        self.winner = None
        self.action_counts = {i: 0 for i in range(7)}
        self.deaths_by_combat = 0
        self.deaths_by_decay = 0


        if test:
            pass

        elif not train and not test:
            self.setupArena(robot)


    def addTributes(self, pos, robot=False):
        center_row = pos[0]
        center_col = pos[1]
        id = 0
        
        # top row - 6 tributes (skip corners at -4 and +3)
        row = center_row - 4
        for col in range(center_col - 2, center_col + 4):
            tribute = Tribute(id, (row, col))
            if robot:
                player = BotPlayer(tribute, self.arena)
            else:
                player = HumanPlayer(tribute, self.arena)

            self.players.append(player)
            self.arena.tributes.append(tribute)
            self.arena.arena_grid[row][col] = tribute.letter
            id += 1
        
        # right column - 6 tributes (skip corners at -4 and +3)
        col = center_col + 5
        for row in range(center_row - 2, center_row + 4):
            tribute = Tribute(id, (row, col))
            if robot:
                player = BotPlayer(tribute, self.arena)
            else:
                player = HumanPlayer(tribute, self.arena)
            self.players.append(player)
            self.arena.tributes.append(tribute)
            self.arena.arena_grid[row][col] = tribute.letter
            id += 1
        
        # bottom row - 6 tributes (skip corners at +3 and -4)
        row = center_row + 5
        for col in range(center_col + 3, center_col - 3, -1):
            tribute = Tribute(id, (row, col))
            if robot:
                player = BotPlayer(tribute, self.arena)
            else:
                player = HumanPlayer(tribute, self.arena)
            self.players.append(player)
            self.arena.tributes.append(tribute)
            self.arena.arena_grid[row][col] = tribute.letter
            id += 1
        
        # left column - 6 tributes (skip corners at +3 and -4)
        col = center_col - 4
        for row in range(center_row + 3, center_row - 3, -1):
            tribute = Tribute(id, (row, col))
            if robot:
                player = BotPlayer(tribute, self.arena)
            else:
                player = HumanPlayer(tribute, self.arena)
            self.players.append(player)
            self.arena.tributes.append(tribute)
            self.arena.arena_grid[row][col] = tribute.letter
            id += 1
        
    def setupArena(self, robot=False):
        self.arena = Arena(self.arena.size)
        self.arena.tributes = []
        self.addTributes(self.arena.center, robot)
        for tribute in self.arena.tributes:
            canteen = Resource(None, None, Resource.Type(2))
            tribute.inventory.append(canteen)
            tribute.max_water = CANTEEN_VALUE
        self.arena.addCornucopia()
        for tribute in self.arena.tributes:
            tribute.arenaKnowledge = self.arena.arena_grid
        self.setupArenaLayout(self.arena)

    def print_results(self):
        print("____________________")
        print("GAME OVER")
        print("____________________\n\n")
        action_names = {0: 'move', 1: 'attack', 2: 'pickup', 3: 'eat', 4: 'drink', 5: 'medical', 6: 'refill'}
        print(f"{'Action':<10} {'Count':<10}")
        print("-" * 20)
        for k, v in self.action_counts.items():
            print(f"{action_names[k]:<10} {v:<10}")
        self.action_counts = {i: 0 for i in range(7)}
        print("\nDEATHS")
        print(f"Combat: {self.deaths_by_combat}")
        print(f"Decay: {self.deaths_by_decay}")
        print("\n\n")



    def setupArenaLayout(self, arena):
        '''
        Sets up the fixed arena layout — trees, water sources, and food.
        Call this after tributes and cornucopia are already placed.
        Does not add tributes, backpacks, or weapons (those come from cornucopia/other setup).
        '''

        # --- BORDER WALL ---
        border = (
            [(0, c) for c in range(arena.size)] +
            [(arena.size - 1, c) for c in range(arena.size)] +
            [(r, 0) for r in range(1, arena.size - 1)] +
            [(r, arena.size - 1) for r in range(1, arena.size - 1)]
        )

        # --- INTERIOR TREES (~120 total, dense coverage) ---
        interior_trees = [
            # row 2-3
            (2,5),(2,11),(2,18),(2,24),(2,31),(2,37),(2,43),
            (3,8),(3,15),(3,21),(3,28),(3,34),(3,40),(3,46),
            # row 4-6
            (4,3),(4,13),(4,19),(4,26),(4,33),(4,38),(4,45),
            (5,7),(5,16),(5,22),(5,29),(5,36),(5,42),
            (6,10),(6,20),(6,32),(6,39),(6,44),
            # row 7-9
            (7,4),(7,13),(7,25),(7,35),(7,43),
            (8,8),(8,17),(8,22),(8,30),(8,38),(8,45),
            (9,3),(9,12),(9,19),(9,27),(9,33),(9,41),
            # row 10-13
            (10,6),(10,15),(10,24),(10,36),(10,44),
            (11,10),(11,20),(11,29),(11,39),(11,46),
            (12,4),(12,14),(12,23),(12,32),(12,42),
            (13,8),(13,18),(13,26),(13,35),(13,43),
            # row 14-17
            (14,3),(14,12),(14,22),(14,30),(14,40),(14,46),
            (15,7),(15,16),(15,24),(15,33),(15,44),
            (16,11),(16,20),(16,29),(16,38),(16,45),
            (17,5),(17,14),(17,23),(17,31),(17,41),
            # row 18-21 (avoid cornucopia center ~19-28, 19-29)
            (18,3),(18,9),(18,40),(18,46),
            (19,6),(19,13),(19,38),(19,44),
            (20,4),(20,10),(20,37),(20,43),
            (21,7),(21,12),(21,39),(21,46),
            # row 22-26
            (22,3),(22,9),(22,41),(22,45),
            (23,5),(23,13),(23,38),(23,44),
            (24,8),(24,11),(24,40),(24,46),
            (25,4),(25,14),(25,37),(25,43),
            (26,6),(26,10),(26,39),(26,45),
            # row 27-30
            (27,3),(27,12),(27,34),(27,40),(27,46),
            (28,7),(28,16),(28,30),(28,38),(28,44),
            (29,4),(29,11),(29,22),(29,35),(29,42),
            (30,8),(30,18),(30,26),(30,37),(30,45),
            # row 31-34
            (31,3),(31,13),(31,21),(31,32),(31,41),(31,46),
            (32,6),(32,17),(32,28),(32,36),(32,43),
            (33,10),(33,20),(33,25),(33,33),(33,40),(33,45),
            (34,4),(34,14),(34,22),(34,30),(34,38),(34,46),
            # row 35-38
            (35,7),(35,16),(35,24),(35,33),(35,42),
            (36,3),(36,11),(36,20),(36,29),(36,38),(36,45),
            (37,6),(37,15),(37,23),(37,31),(37,40),(37,46),
            (38,9),(38,18),(38,26),(38,35),(38,43),
            # row 39-42
            (39,4),(39,13),(39,22),(39,30),(39,41),(39,46),
            (40,7),(40,16),(40,25),(40,34),(40,44),
            (41,3),(41,11),(41,20),(41,28),(41,37),(41,45),
            (42,6),(42,15),(42,23),(42,32),(42,40),(42,46),
            # row 43-46
            (43,9),(43,18),(43,26),(43,35),(43,43),
            (44,4),(44,13),(44,22),(44,30),(44,41),(44,46),
            (45,7),(45,16),(45,24),(45,33),(45,40),
            (46,3),(46,11),(46,20),(46,28),(46,37),(46,45),
        ]

        # --- WATER SOURCES (type 1) ---
        water_positions = []

        

        # upper-left — 4x4
        for r in range(4, 8):
            for c in range(6, 10):
                water_positions.append((r, c))

        # upper-right — 4x4
        for r in range(3, 7):
            for c in range(38, 42):
                water_positions.append((r, c))

        # bottom-center — larger 5x6
        for r in range(38, 43):
            for c in range(21, 27):
                water_positions.append((r, c))

        # center-right — 3x3 near cornucopia
        for r in range(23, 26):
            for c in range(28, 31):
                water_positions.append((r, c)) # TEST

        # center-left — near cornucopia, rows 15-18
        for r in range(15, 19):
            for c in range(21, 25):
                water_positions.append((r, c)) # TEST

        # center-right — near cornucopia, rows 15-18
        for r in range(15, 19):
            for c in range(28, 32):
                water_positions.append((r, c)) # TEST


    # mid-left — rows 22-25
        for r in range(22, 25):
            for c in range(8, 11):
                water_positions.append((r, c))

        # mid-right — rows 22-25
        for r in range(22, 25):
            for c in range(39, 42):
                water_positions.append((r, c))

        # center-bottom-left — rows 30-33
        for r in range(30, 33):
            for c in range(10, 13):
                water_positions.append((r, c))

        # center-bottom-right — rows 30-33
        for r in range(30, 33):
            for c in range(37, 40):
                water_positions.append((r, c))




        for pos in water_positions:
            r, c = pos
            if arena.arena_grid[r][c] != 0:
                continue
            arena.resources.append(Resource(arena.next_resource_id, pos, Resource.Type(1)))
            arena.arena_grid[r][c] = 1
            arena.next_resource_id += 1

        # --- FOOD SOURCES (type 3) ---
        # 2x3 clusters ("bushes")
        # food_cluster_origins = [
        #     (6, 16), (6, 27),
        #     (16, 5), (16, 40),
        #     (31, 5), (31, 40),
        #     (41, 16), (41, 27),
        #     (22, 31), (24, 35), (26, 32), # TEST

        #                 # additional clusters
        #     (10, 30), (10, 16),   # upper mid left/right
        #     (20, 42), (20, 3),    # mid outer left/right
        #     (30, 42), (30, 3),    # lower outer left/right
        #     (36, 16), (36, 27),   # lower mid left/right
        #     (18, 16), (18, 31),   # near cornucopia
        
        # ]

        food_cluster_origins = [
            (6, 16), (6, 27),
            (16, 5), (16, 40),
            (31, 5), (31, 40),
            (41, 16), (41, 27),
            # (22, 31), (24, 35), (26, 32),
            # additional clusters (all outside rows 18-29, cols 18-29 clear zone)
            (10, 16), (10, 30),   # upper mid left/right
            (15, 3), (15, 42),    # upper outer left/right
            (20, 3), (20, 42),    # mid outer left/right
            (30, 3), (30, 42),    # lower outer left/right
            (36, 16), (36, 27),   # lower mid left/right
        ]

        cluster_food = [
            (r + dr, c + dc)
            for r, c in food_cluster_origins
            for dr in range(3)
            for dc in range(2)
        ]

        # single food tiles ("animals")
        single_food = [
            (8,12),(8,26),(8,39),
            (14,22),(18,10),(18,38),
            (24,16),(24,32),(29,19),
            (29,28),(34,11),(34,37),
            (39,22),(39,31),(44,9),
            (44,37),(11,35),(11,8),
            (21,42),(21,5),
        ]

        for pos in cluster_food + single_food:
            r, c = pos
            if arena.arena_grid[r][c] != 0:
                continue
            arena.resources.append(Resource(arena.next_resource_id, pos, Resource.Type(3)))
            arena.arena_grid[r][c] = 3
            arena.next_resource_id += 1

        # --- TREES (placed last so they never overwrite anything) ---
        for pos in border + interior_trees:
            r, c = pos
            if arena.arena_grid[r][c] != 0:
                continue
            arena.obstacles.append(pos)
            arena.arena_grid[r][c] = 8

    def run(self, show_arena=True):
            while len(self.arena.tributes) > 1:
                self.turn_count += 1
                if show_arena:
                    self.arena.displayArena()
                print(f"\n========== DAY {self.day_count + 1} ===============")
                while self.turn_count <= TURNS_PER_DAY:
                    for player in self.players:
                        if not player.tribute.isAlive:
                            continue
                        player.tribute.segment = self.arena.getSegmentFromPos(player.tribute.pos)
                        gh.setValuesBeforeTurn(player.tribute, self.arena)
                        player.valid_actions = gh.setupActionMap(player.tribute, self.arena, self)
                        print(f"\n[TRIBUTE {player.tribute.letter} - Turn {self.turn_count}]")
                        player.take_turn()
                        self.arena.clearDeadTributes(self)
                        self.players = [p for p in self.players if p.tribute.isAlive]
                        if len(self.arena.tributes) <= 1:
                            if len(self.arena.tributes) == 1:
                                self.winner = self.arena.tributes[0]
                            break
                    if len(self.arena.tributes) <= 1:
                        break
                    self.turn_count += 1
                    
                self.turn_count = 0
                self.day_count += 1
                if len(self.arena.tributes) <= 1:
                    break

            print("THE GAMES ARE OVER! Congratulations to our victor!")
            self.printGameResults()

    def printGameResults(self):
        print("_" * 30)
        print(" VICTOR")
        print("_" * 30)
        print(f"  Name:        Tribute {self.winner.letter}")
        print(f"  District:    {self.winner.district}")
        print(f"  Gender:      {self.winner.gender.capitalize()}")
        print("_" * 30)
        print(" GAME STATS")
        print("_" * 30)
        print(f"  Days:        {self.day_count}")
        print(f"  Drama Score: {self.drama}")
        print("_" * 30)