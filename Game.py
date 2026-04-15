"""
Game.py - Defines the Game class, which is the engine behind the simulator itself.

"""


from Arena import Arena
from Gamemaker import Gamemaker
from Intervention import Intervention
from Tribute import Tribute
from Resource import Resource
from config import *
from Player import Player, HumanPlayer, BotPlayer
import gymnasium as gym
from gymnasium import spaces
from tqdm import tqdm
import numpy as np
import gameplay_handler as gh

class Game():
    """
    Represents the Game class
    """
    
    def __init__(self, size, robot=False, train=False, test=False):    

        self.arena = Arena(size)
        self.gamemaker = None
        self.players = []
        self.turn_count = 0
        self.day_count = 0
        self.drama = 0
        self.retaliation_count = 0
        self.game_rewards = 0
        self.winner = None
        self.deaths_by_combat = 0
        self.deaths_by_decay = 0
        self.deaths_by_gamemaker = 0
        self.death_log = []
        self.deaths_per_day = {1: {"decay": 0, "combat": 0, "gamemaker": 0}}
        self.action_counts = {i: 0 for i in range(7)}
        self.cornucopia_pickups = 0
        self.end_condition = None # "cap", "winner", "mutual_decay"
        self.exceeded_training_cap = False
        self.victory_by_combat = False
        self.day_one_kills = 0
        self.desperate_resource_uses = 0





        if train:
            self.setupArena(robot, train)

        elif not train and not test:
            self.setupArena(robot)


    def addTributes(self, pos, robot=False):
        """
        Creates all 24 BotPlayers and their Tributes and adds the tributes to the arena around the cornucopia
        """

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
        
    def setupArena(self, robot=False, train=False):
        """
        Sets up the arena, creates the gamemaker, provides the tributes with a canteen, adds in the cornucopia
        and puts all required elements into the arena
        
        """

        self.arena = Arena(self.arena.size)
        self.gamemaker = Gamemaker(self.arena)
        self.arena.tributes = []
        self.addTributes(self.arena.center, robot)
        for tribute in self.arena.tributes:
            canteen = Resource(None, None, Resource.Type(2))
            tribute.inventory.append(canteen)
            tribute.max_water = CANTEEN_VALUE
        self.arena.addCornucopia()
        for tribute in self.arena.tributes:
            tribute.arenaKnowledge = self.arena.arena_grid
        if train:
            self.setupArenaLayout(self.arena, train=True)
        else:
            self.setupArenaLayout(self.arena, train=False)


    def print_results(self):
        """
        Prints the results of the executed games for training mode
        """
        print("____________________")
        print("GAME OVER")
        print("____________________\n")
        print(f"Days: {self.day_count + 1}\n")

        self.print_action_table()
        self.action_counts = {i: 0 for i in range(7)}
        print("\nDEATHS")
        print(f"Combat: {self.deaths_by_combat}")
        print(f"Decay: {self.deaths_by_decay}")
        print(f"Gamemaker: {self.deaths_by_gamemaker}")
        print("\n\n")


    def print_action_table(self):
        """
        prints the action distribution table for the executed games
        """
        action_names = {0: 'move', 1: 'attack', 2: 'pickup', 3: 'eat', 4: 'drink', 5: 'medical', 6: 'refill'}
        print(f"{'ACTION':<10} {'COUNT':<10}")
        print("-" * 30)
        for k, v in self.action_counts.items():
            print(f"{action_names[k]:<10} {v:<10}")



    def run(self, show_arena=True, show_colors=False, print_moves=False, save_frames=False, progress=None):
        """
        The main engine object around the game. Executes the full games loop
        before printing the results
        """
        frames = []


        while len(self.arena.tributes) > 1:
            self.turn_count += 1
            if show_arena:
                self.arena.displayArena(show_colors)
            # if print_moves:
            print(f"\n========== DAY {self.day_count + 1} ===============")
            self.deaths_per_day[self.day_count + 1] = {"decay": 0, "combat": 0, "gamemaker" : 0}
            while self.turn_count <= TURNS_PER_DAY:
                
                if save_frames:
                    frames.append(self.arena.renderTurnFrames(self.turn_count, self.day_count + 1))
                for player in self.players:
                    if not player.tribute.isAlive:
                        continue
                    player.tribute.segment = self.arena.getSegmentFromPos(player.tribute.pos)
                    gh.setValuesBeforeTurn(player.tribute, self.arena)

                    # NOTE: NEED TO MAKE SURE WE ARE APPROPRIATELY CHECKING IF THE GAME IS OVER AFTER SET VALUES BEFORE TURN

                    if print_moves:
                        print(f"\n[TRIBUTE {player.tribute.letter} - Turn {self.turn_count}]")
                    if player.tribute.isAlive:
                        player.valid_actions = gh.setupActionMap(player.tribute, self.arena, self)
                        player.take_turn(self, print_moves)
                    self.arena.clearDeadTributes(self)
                    self.players = [p for p in self.players if p.tribute.isAlive]
                    if len(self.arena.tributes) <= 1:
                        if len(self.arena.tributes) == 1:
                            self.winner = self.arena.tributes[0]
                            if self.winner == player.tribute:
                                self.victory_by_combat = True
                        break
                if len(self.arena.tributes) <= 1:
                    break
                self.turn_count += 1
                # at the end of a round, assess interference
                self.gamemaker.assessInterference(self)

            self.arena.bomb.wasDeployedToday = False
            self.arena.hazard.wasDeployedToday = False

            self.turn_count = 0
            self.day_count += 1
            if self.day_count >= 10: # ON day 11 because index 0 start
                self.exceeded_training_cap = True
            if self.day_count >= 15:
                self.end_condition = "cap"
                break
            if progress is not None:
                progress.update(1)
            if len(self.arena.tributes) <= 1:
                break

        if self.death_log:
            print(f"\n--- Day {self.day_count} Deaths ---")
            for msg in self.death_log:
                print(msg)
            self.death_log = []

        for pos in self.arena.cornucopia:
            if not any(resource.pos == pos for resource in self.arena.resources):
                self.cornucopia_pickups += 1

        if save_frames and frames:
            frames[0].save("games.gif", save_all=True, append_images=frames[1:], duration=GIF_DURATION, loop=0)

        end_statement = ""
        if len(self.arena.tributes) == 1:
            self.end_condition = "winner"
            end_statement = " Congratulations to our victor!"
        elif len(self.arena.tributes) > 1:
            self.end_condition = "cap"
        elif len(self.arena.tributes) < 1:
            self.end_condition = "mutual_decay"
        else:
            self.end_condition = "none" # for preacaution

        
        print(f"\n\nTHE GAMES ARE OVER!{end_statement}")
        self.printGameResults()

    def printGameResults(self):
        """
        Prints the game results for the executed games
        """
        print("-" * 30)
        print("VICTOR")
        print("-" * 30)
        if self.end_condition == "winner":
            print(f"Name:        Tribute {self.winner.letter}")
            print(f"District:    {self.winner.district}")
            print(f"Gender:      {self.winner.gender.capitalize()}")
        else:
            print("No victor")
        print("-" * 30)
        print("GAME STATS")
        print("-" * 30)
        print(f"Days:               {self.day_count + 1}")
        print(f"Gamemaker Kills:    {self.deaths_by_gamemaker}")
        print(f"Decay Kills:        {self.deaths_by_decay}")
        print(f"Combat Kills:       {self.deaths_by_combat}")
        print("-" * 30)
        self.print_action_table()
        print("-" * 30)
            # print(f"  Drama Score: {self.drama}")



    def setupArenaLayout(self, arena, train=False):
        """
        Adds all non-tribute and cornucopia objects to the arena:
        - trees and obstacles
        - scattered food
        - scattered water sources
        - hazards (disabled)
        """

        # --- BORDER WALL ---
        border = (
            [(0, c) for c in range(arena.size)] +
            [(arena.size - 1, c) for c in range(arena.size)] +
            [(r, 0) for r in range(1, arena.size - 1)] +
            [(r, arena.size - 1) for r in range(1, arena.size - 1)]
        )

        # --- INTERIOR TREES ---
        interior_trees = [
            (2,5),(2,11),(2,18),(2,24),(2,31),(2,37),(2,43),
            (3,8),(3,15),(3,21),(3,28),(3,34),(3,40),(3,46),
            (4,3),(4,13),(4,19),(4,26),(4,33),(4,38),(4,45),
            (5,7),(5,16),(5,22),(5,29),(5,36),(5,42),
            (6,10),(6,20),(6,32),(6,39),(6,44),
            (7,4),(7,13),(7,25),(7,35),(7,43),
            (8,8),(8,17),(8,22),(8,30),(8,38),(8,45),
            (9,3),(9,12),(9,19),(9,27),(9,33),(9,41),
            (10,6),(10,15),(10,24),(10,36),(10,44),
            (11,10),(11,20),(11,29),(11,39),(11,46),
            (12,4),(12,14),(12,23),(12,32),(12,42),
            (13,8),(13,18),(13,26),(13,35),(13,43),
            (14,3),(14,12),(14,22),(14,30),(14,40),(14,46),
            (15,7),(15,16),(15,24),(15,33),(15,44),
            (16,11),(16,20),(16,29),(16,38),(16,45),
            (17,5),(17,14),(17,31),(17,41),
            (18,3),(18,9),(18,40),(18,46),
            (19,6),(19,13),(19,38),(19,44),
            (20,4),(20,10),(20,37),(20,43),
            (21,7),(21,12),(21,39),(21,46),
            (22,3),(22,9),(22,41),(22,45),
            (23,5),(23,13),(23,38),(23,44),
            (24,8),(24,11),(24,40),(24,46),
            (25,4),(25,14),(25,37),(25,43),
            (26,6),(26,10),(26,39),(26,45),
            (27,3),(27,12),(27,34),(27,40),(27,46),
            (28,7),(28,16),(28,30),(28,38),(28,44),
            (29,4),(29,11),(29,22),(29,35),(29,42),
            (30,8),(30,18),(30,26),(30,37),(30,45),
            (31,3),(31,13),(31,21),(31,32),(31,41),(31,46),
            (32,6),(32,17),(32,28),(32,36),(32,43),
            (33,10),(33,20),(33,25),(33,33),(33,40),(33,45),
            (34,4),(34,14),(34,22),(34,30),(34,38),(34,46),
            (35,7),(35,16),(35,24),(35,33),(35,42),
            (36,3),(36,11),(36,20),(36,29),(36,38),(36,45),
            (37,6),(37,15),(37,23),(37,31),(37,40),(37,46),
            (38,9),(38,18),(38,26),(38,35),(38,43),
            (39,4),(39,13),(39,22),(39,30),(39,41),(39,46),
            (40,7),(40,16),(40,25),(40,34),(40,44),
            (41,3),(41,11),(41,20),(41,28),(41,37),(41,45),
            (42,6),(42,15),(42,23),(42,32),(42,40),(42,46),
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

        # bottom-center — 5x6
        for r in range(38, 43):
            for c in range(21, 27):
                water_positions.append((r, c))

        # center-right — shifted out 2 from cols 28-30 to cols 32-34
        for r in range(23, 26):
            for c in range(32, 35):
                water_positions.append((r, c))

        # center-left — shifted out 2 from rows 15-18 to rows 13-16, cols 21-24
        for r in range(13, 17):
            for c in range(21, 25):
                water_positions.append((r, c))

        # center-right upper — shifted out 2 from rows 15-18 to rows 13-16, cols 28-32
        for r in range(13, 17):
            for c in range(28, 32):
                water_positions.append((r, c))

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
        food_cluster_origins = [
            (6, 16), (6, 27),
            (16, 5), (16, 40),
            (31, 5), (31, 40),
            (41, 16), (41, 27),
            (22, 31), (24, 35), (26, 32),
            (10, 16), (10, 30),
            (15, 3), (15, 42),
            (20, 3), (20, 42),
            (30, 3), (30, 42),
            (36, 16), (36, 27),
        ]

        cluster_food = [
            (r + dr, c + dc)
            for r, c in food_cluster_origins
            for dr in range(3)
            for dc in range(2)
        ]

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

        # --- TREES ---
        for pos in border + interior_trees:
            r, c = pos
            if arena.arena_grid[r][c] != 0:
                continue
            arena.obstacles.append(pos)
            arena.arena_grid[r][c] = 8

        # --- TRAINING HAZARD TILES ---
        if train:

            hazard_positions = [
            (5, 15), (5, 28), (17, 4), (17, 41),
            (32, 4), (32, 41), (42, 15), (42, 28),
            (10, 17), (15, 17), (26, 16), (33, 17),
            (37, 15), (37, 32), (43, 15), (43, 32),
            ]

            for r, c in hazard_positions:
                if arena.arena_grid[r][c] != 0:
                    continue
                arena.hazards.append(Intervention(Intervention.Type.HAZARD, positions=[], damage=HAZARD_DAMAGE, pos=(r, c)))
                arena.arena_grid[r][c] = Intervention.Type.HAZARD.value

        print("-" * 30)
