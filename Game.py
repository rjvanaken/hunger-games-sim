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
        self.arena.addSources()
        self.arena.addTrees(0.15)
        self.arena.displayArena()


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