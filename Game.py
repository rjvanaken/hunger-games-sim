from Arena import Arena
from Tribute import Tribute
from Resource import Resource
from config import TURNS_PER_DAY
from Player import Player, HumanPlayer, BotPlayer
import gymnasium as gym
from gymnasium import spaces
import numpy as np

class Game():
    
    def __init__(self, size, robot=False, train=False, test=False):    

        self.arena = Arena(size)
        self.players = []
        self.turn_count = 0
        self.day_count = 0
        self.drama = 0

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
        self.arena.addCornucopia()
        for tribute in self.arena.tributes:
            tribute.arenaKnowledge = self.arena.arena_grid
        self.arena.setupArenaLayout

        # self.arena.addSources()
        # self.arena.addTrees(0.15)
        # self.arena.displayArena()



    def setupArenaLayout(arena):
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

        # --- INTERIOR TREES ---
        interior_trees = [
            (3,8),  (4,20),  (6,35),  (7,14),
            (10,2), (12,28), (14,42), (16,10),
            (19,22),(21,38), (23,5),  (25,17),
            (28,32),(30,8),  (32,44), (34,20),
            (37,12),(39,36), (43,26), (46,6),
        ]

        for pos in border + interior_trees:
            arena.obstacles.append(pos)
            arena.arena_grid[pos[0]][pos[1]] = 8

        # --- WATER SOURCES (type 1) — 4x4 clusters in 3 corners ---
        water_positions = []

        # upper-left corner
        for r in range(2, 6):
            for c in range(2, 6):
                water_positions.append((r, c))

        # upper-right corner
        for r in range(2, 6):
            for c in range(42, 46):
                water_positions.append((r, c))

        # lower-right corner
        for r in range(42, 46):
            for c in range(42, 46):
                water_positions.append((r, c))

        for pos in water_positions:
            arena.resources.append(Resource(arena.next_resource_id, pos, Resource.Type(1)))
            arena.arena_grid[pos[0]][pos[1]] = 1
            arena.next_resource_id += 1

        # --- FOOD SOURCES (type 3) ---
        # 2x3 clusters ("bushes") spread around the mid-ring
        food_cluster_origins = [
            (5, 15), (5, 28),
            (15, 5), (15, 40),
            (32, 5), (32, 40),
            (42, 15),(42, 28),
        ]
        cluster_food = [
            (r + dr, c + dc)
            for r, c in food_cluster_origins
            for dr in range(3)
            for dc in range(2)
        ]

        # single food tiles ("animals") scattered throughout
        single_food = [
            (8,10),  (8,25),  (8,38),
            (15,20), (20,8),  (20,40),
            (24,15), (24,33), (30,18),
            (30,28), (35,10), (35,38),
            (40,20), (40,30), (44,8),
            (44,38),
        ]

        for pos in cluster_food + single_food:
            arena.resources.append(Resource(arena.next_resource_id, pos, Resource.Type(3)))
            arena.arena_grid[pos[0]][pos[1]] = 3
            arena.next_resource_id += 1



    def run(self):
            while len(self.arena.tributes) > 1:
                self.turn_count += 1
                print(f"=== DAY {self.day_count + 1} ===")
                for player in self.players:
                    if player.tribute.isAlive:
                        print(f"\n[TRIBUTE {player.tribute.letter} - Turn {self.turn_count}]")
                        player.take_turn()
                self.arena.clearDeadTributes()
                self.arena.displayArena()
                # if turn cap has been reached, reset and move to next day
                if self.turn_count == TURNS_PER_DAY:
                    self.turn_count = 0
                    self.day_count += 1
            print("THE GAMES ARE OVER! Congratulations to our victor!")

            self.printGameResults()

    def printGameResults(self):
        winner = self.arena.tributes[0]
        print("──────────────────────────────")
        print(" VICTOR")
        print("──────────────────────────────")
        print(f"  Name:        Tribute {winner.letter}")
        print(f"  District:    {winner.district}")
        print(f"  Gender:      {winner.gender.capitalize()}")
        print("──────────────────────────────")
        print(" GAME STATS")
        print("──────────────────────────────")
        print(f"  Days:        {self.day_count}")
        print(f"  Drama Score: {self.drama}")
        print("──────────────────────────────")