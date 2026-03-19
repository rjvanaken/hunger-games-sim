from Arena import Arena
from Game import Game
from Tribute import Tribute
from Resource import Resource
from config import *
from Player import Player, HumanPlayer, BotPlayer
import gymnasium as gym
from gymnasium import spaces
import numpy as np
import gameplay_handler

class GameEnv(gym.Env):
    
    def __init__(self, size):    
        super().__init__()
            
        self.arena = Arena(size)
        self.game = Game(48, False)
        self.tribute = None
        self.ACTION_MAP = {0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9, 10: 10}
        self.valid_actions = set()


        VIEW_RADIUS = 2  # 5x5 window

        self.observation_space = spaces.Dict({
            "local_view": spaces.Box(low=0, high=10, shape=(5, 5), dtype=np.int32),
            "known_water_row": spaces.Discrete(30),
            "known_water_col": spaces.Discrete(30),
            "health": spaces.Discrete(101),
            "hunger": spaces.Discrete(101),
            "thirst": spaces.Discrete(101),
            "row": spaces.Discrete(30),
            "col": spaces.Discrete(30),
})

    def setupActionMap(self, tribute, arena):
        self.valid_actions = set()
        if gameplay_handler.moveMask(tribute, 'up'):
            self.valid_actions.add(0)
        if gameplay_handler.moveMask(tribute, 'down'):
            self.valid_actions.add(1)
        if gameplay_handler.moveMask(tribute, 'left'):
            self.valid_actions.add(2)
        if gameplay_handler.moveMask(tribute, 'right'):
            self.valid_actions.add(3)
        if gameplay_handler.attackMask(arena, tribute):
            self.valid_actions.add(4)
        if gameplay_handler.pickupMask(tribute, arena):
            self.valid_actions.add(5)
        if gameplay_handler.eatMask(tribute):
            self.valid_actions.add(6)
        if gameplay_handler.drinkMask(tribute, arena):
            self.valid_actions.add(7)
        if gameplay_handler.healMask(tribute):
            self.valid_actions.add(8)
        if gameplay_handler.sleepMask(tribute):
            self.valid_actions.add(9)
        if gameplay_handler.refillMask(tribute, arena):
            self.valid_actions.add(10)
            

    def getLocalView(self, tribute, radius=2):
        size = radius * 2 + 1
        view = np.zeros((size, size), dtype=np.int32)
        
        for dr in range(-radius, radius + 1):
            for dc in range(-radius, radius + 1):
                r = tribute.pos[0] + dr
                c = tribute.pos[1] + dc
                row_i = dr + radius
                col_i = dc + radius
                
                if 0 <= r < self.arena.size and 0 <= c < self.arena.size:
                    cell = self.arena.arena_grid[r][c]
                    if isinstance(cell, str):  # tribute letter
                        view[row_i][col_i] = 10  # TRIBUTE
                    else:
                        view[row_i][col_i] = cell # number already there
                else:
                    view[row_i][col_i] = 8  # out of bounds is an obstacle
        
        return view
    
    def getKnownWater(self, tribute):
        for r in range(len(tribute.arenaKnowledge)):
            for c in range(len(tribute.arenaKnowledge[r])):
                if tribute.arenaKnowledge[r][c] == 1: 
                    return r, c
        return -1, -1  # none yet
    

    def setValuesBeforeTurn(self):
        self.tribute.segment = self.arena.getSegmentFromPos(self.tribute.pos)
        segment = self.tribute.segment
        self.arena.updateSegmentData(self.tribute, segment)
        self.tribute.updateStatsBeforeTurn()
        self.tribute.updateKnowledge(self.arena)

    def cleanUpAfterTurn(self):
        # reset values
        self.arena.clearDeadTributes()
        self.game.turn_count += 1
        if self.game.turn_count == TURNS_PER_DAY:
            self.game.turn_count = 0
            self.game.day_count += 1


    def reset(self):
        self.game.setupArena()
        self.current_tribute_index = 0
        self.tribute = self.game.tributes[self.current_tribute_index]

        obs = {
            "local_view": self.getLocalView(self.tribute),
            "health": self.tribute.health,
            "hunger": self.tribute.hunger,
            "thirst": self.tribute.thirst,
            "row": self.tribute.pos[0],
            "col": self.tribute.pos[1],
            "known_water_row": 0,
            "known_water_col": 0,
        }

        return obs, {}

    def step(self, action):
        reward = 0
        terminated = False
        self.setupActionMap(self.tribute, self.arena)
        
        self.setValuesBeforeTurn()

        obs = {
            "local_view": self.getLocalView(self.tribute),
            "health": self.tribute.health,
            "hunger": self.tribute.hunger,
            "thirst": self.tribute.thirst,
            "row": self.tribute.pos[0],
            "col": self.tribute.pos[1],
            "known_water_row": self.getKnownWater(self.tribute)[0],
            "known_water_col": self.getKnownWater(self.tribute)[1],
        }

        if action not in self.valid_actions:
            return obs, -100, False, False, {}
        
        # not done at all, placeholders
        if action == 0:
            gameplay_handler.handleSingleMove(self.tribute, 'up')

        elif action == 1:
            gameplay_handler.handleSingleMove(self.tribute, 'down')
            
        elif action == 2:
            gameplay_handler.handleSingleMove(self.tribute, 'left')

        elif action == 3:
            gameplay_handler.handleSingleMove(self.tribute, 'right')

        elif action == 4:
            health_before = self.tribute.health
            kills_before = self.tribute.num_kills
            gameplay_handler.handleAttack(self.tribute, self.arena)
            if self.tribute.num_kills > kills_before:
                reward += 500 # got a kill
            if self.tribute.health < health_before:
                reward -= 50 # got damage
            else:
                reward += 50 # won an attakc

        elif action == 5:
            capacity_before = self.tribute.capacity
            weapon_before = self.tribute.weapon_value
            result = gameplay_handler.handlePickup(self.tribute, self.arena)
            if result == 1:
                reward += 20
                if self.tribute.capacity > capacity_before:
                    reward += 10 # additional 10 for picking up backpack
                if self.tribute.weapon_value > weapon_before:
                    reward += 10 # additional 10 for picking up weapon
                    if self.tribute.weapon_value > WEAK_WEAPON:
                        reward += 5 # additional 5 for weapon being strong
            elif result == 2:
                reward -= 5

        elif action == 6:
            gameplay_handler.handleEatFood(self.tribute)
            reward += 5

        elif action == 7:
            gameplay_handler.handleDrinkWater(self.tribute, self.arena)
            reward += 5
        elif action == 8:
            gameplay_handler.handleUseMedical(self.tribute)
            reward += 20

        elif action == 9:
            gameplay_handler.handleSleep(self.tribute)
            reward += 10

        elif action == 10:
            gameplay_handler.handleRefillWater(self.tribute, self.arena)
            reward += 20

        if self.tribute.hunger <= HUNGER_WARNING_THRESHOLD:
            reward -= 10
        if self.tribute.thirst <= THIRST_WARNING_THRESHOLD:
            reward -= 10
        if self.tribute.health <= 40:
            reward -= 10

        if not self.tribute.isAlive():
            reward -= 500
            terminated = True

        if len(self.arena.tributes) == 1:
            reward += 2000

        self.cleanUpAfterTurn()

        # move to next tribute
        self.current_tribute_index += 1
        if self.current_tribute_index >= len(self.game.tributes):
            self.current_tribute_index = 0
        self.tribute = self.game.tributes[self.current_tribute_index]

        obs = {
            "local_view": self.getLocalView(self.tribute),
            "health": self.tribute.health,
            "hunger": self.tribute.hunger,
            "thirst": self.tribute.thirst,
            "row": self.tribute.pos[0],
            "col": self.tribute.pos[1],
            "known_water_row": self.getKnownWater(self.tribute)[0],
            "known_water_col": self.getKnownWater(self.tribute)[1],
        }

        
        return obs, reward, terminated, False, {}