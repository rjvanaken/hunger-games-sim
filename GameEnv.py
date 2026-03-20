from Arena import Arena
from Game import Game
from Tribute import Tribute
from Resource import Resource
from config import *
from Player import Player, HumanPlayer, BotPlayer
import gymnasium as gym
from gymnasium import spaces
import numpy as np
import gameplay_handler as gh
import train_helper as th

class GameEnv(gym.Env):
    
    def __init__(self, size):    
        super().__init__()
            
        self.game = Game(size=48, robot=True)
        self.arena = self.game.arena
        self.tribute = None
        self.ACTION_MAP = {0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9, 10: 10}
        self.valid_actions = set()

        # cut tribute count in half for training
        for tribute in self.arena.tributes:
            if tribute.gender == 'female':
                tribute.isAlive = False
                
        # cleanup "dead" tributes 
        self.arena.clearDeadTributes()
        self.arena.displayArena()


        VIEW_RADIUS = 2  # 5x5 window

        self.action_space = spaces.Discrete(11)

        self.observation_space = spaces.Dict({
            "local_view": spaces.Box(low=0, high=10, shape=(5, 5), dtype=np.int32),
            "known_water_row": spaces.Discrete(49),
            "known_water_col": spaces.Discrete(49),
            "health": spaces.Discrete(101),
            "hunger": spaces.Discrete(101),
            "thirst": spaces.Discrete(101),
            "row": spaces.Discrete(49),
            "col": spaces.Discrete(49),
})
            



    def reset(self, **kwargs):
        self.game = Game(size=48, robot=True)
        self.arena = self.game.arena
        for tribute in self.arena.tributes:
            if tribute.gender == 'female':
                tribute.isAlive = False
        self.arena.clearDeadTributes()
        self.arena.displayArena()
        self.current_tribute_index = 0
        self.tribute = self.arena.tributes[self.current_tribute_index]

        obs = {
            "local_view": gh.getLocalView(self.tribute, self.arena),
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
        self.valid_actions = gh.setupActionMap(self.tribute, self.arena)
        
        gh.setValuesBeforeTurn(self.tribute, self.arena)


        obs = {
            "local_view": gh.getLocalView(self.tribute, self.arena),
            "health": self.tribute.health,
            "hunger": self.tribute.hunger,
            "thirst": self.tribute.thirst,
            "row": self.tribute.pos[0],
            "col": self.tribute.pos[1],
            "known_water_row": gh.getKnownWater(self.tribute)[0],
            "known_water_col": gh.getKnownWater(self.tribute)[1],
        }

        if not self.tribute.isAlive:
            reward -= 500
            gh.cleanUpAfterTurn(self.game, self.arena)
            if len(self.arena.tributes) == 1:
                reward += 2000
                print(f"Tribute {self.arena.tributes[0].letter} wins!!")
                print("GAME OVER\n\n")
                return obs, reward, True, False, {}

            self.current_tribute_index = 0
            self.tribute = self.arena.tributes[self.current_tribute_index]
            return obs, reward, False, False, {}

        if action not in self.valid_actions:
            return obs, -100, False, False, {}
        
        # not done at all, placeholders
        if action == 0:
            gh.handleSingleMove(self.tribute, 'up', self.arena)
            print(f"Tribute {self.tribute.letter} moved up")

        elif action == 1:
            gh.handleSingleMove(self.tribute, 'down', self.arena)
            print(f"Tribute {self.tribute.letter} moved down")
            
        elif action == 2:
            gh.handleSingleMove(self.tribute, 'left', self.arena)
            print(f"Tribute {self.tribute.letter} moved left")

        elif action == 3:
            gh.handleSingleMove(self.tribute, 'right', self.arena)
            print(f"Tribute {self.tribute.letter} moved right")

        elif action == 4:
            health_before = self.tribute.health
            kills_before = self.tribute.num_kills
            gh.handleAttack(self.tribute, self.arena)
            print(f"Tribute {self.tribute.letter} attacked tribute")
            if self.tribute.num_kills > kills_before:
                reward += 500 # got a kill
            if self.tribute.health < health_before:
                reward -= 50 # got damage
            else:
                reward += 50 # won an attakc

        elif action == 5:
            capacity_before = self.tribute.capacity
            weapon_before = self.tribute.weapon_value
            result = gh.handlePickup(self.tribute, self.arena)
            print(f"Tribute {self.tribute.letter} picked up an item")
            if result == 1:
                reward += 50
                if self.tribute.capacity > capacity_before:
                    reward += 20 # additional 10 for picking up backpack
                if self.tribute.weapon_value > weapon_before:
                    reward += 20 # additional 10 for picking up weapon
                    if self.tribute.weapon_value > WEAK_WEAPON:
                        reward += 10 # additional 5 for weapon being strong

        elif action == 6:
            gh.handleEatFood(self.tribute)
            print(f"Tribute {self.tribute.letter} ate food")
            reward += 30

        elif action == 7:
            gh.handleDrinkWater(self.tribute, self.arena)
            print(f"Tribute {self.tribute.letter} drank water")
            reward += 30
        elif action == 8:
            gh.handleUseMedical(self.tribute)
            print(f"Tribute {self.tribute.letter} used medical")
            reward += 30

        elif action == 9:
            gh.handleSleep(self.tribute)
            print(f"Tribute {self.tribute.letter} slept")
            reward += 10

        elif action == 10:
            gh.handleRefillWater(self.tribute, self.arena)
            print(f"Tribute {self.tribute.letter} refilled their canteen")
            reward += 50

        if self.tribute.hunger <= HUNGER_WARNING_THRESHOLD:
            reward -= 10
        if self.tribute.thirst <= THIRST_WARNING_THRESHOLD:
            reward -= 10
        if self.tribute.health <= 40:
            reward -= 10

        if not self.tribute.isAlive:
            print(f"Tribute {self.tribute.letter} died")
            reward -= 500

        if len(self.arena.tributes) == 1:
            reward += 2000
            terminated = True
            print(f"Tribute {self.tribute.letter} wins!!")

        gh.cleanUpAfterTurn(self.game, self.arena)

        if terminated:
            # self.arena.displayArena()
            print("____________________")
            print("GAME OVER")
            print("____________________\n\n")

            return obs, reward, terminated, False, {}

        # move to next tribute
        self.current_tribute_index += 1
        if self.current_tribute_index >= len(self.arena.tributes):
            self.current_tribute_index = 0
        self.tribute = self.arena.tributes[self.current_tribute_index]

        obs = {
            "local_view": gh.getLocalView(self.tribute, self.arena),
            "health": self.tribute.health,
            "hunger": self.tribute.hunger,
            "thirst": self.tribute.thirst,
            "row": self.tribute.pos[0],
            "col": self.tribute.pos[1],
            "known_water_row": gh.getKnownWater(self.tribute)[0],
            "known_water_col": gh.getKnownWater(self.tribute)[1],
        }


        
        return obs, reward, terminated, False, {}
    

