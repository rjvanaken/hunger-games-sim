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
        self.ACTION_MAP = {0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7}
        self.valid_actions = set()

        self.action_counts = {i: 0 for i in range(8)}
        # cut tribute count in half for training
        # for tribute in self.arena.tributes:
        #     if tribute.gender == 'female':
        #         tribute.isAlive = False

        
        for i in range(18):
            self.arena.tributes[i].isAlive = False
 
        # cleanup "dead" tributes 
        self.arena.clearDeadTributes()
        self.arena.displayArena()


        VIEW_RADIUS = 2  # 5x5 window

        self.action_space = spaces.Discrete(8)

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
        # for tribute in self.arena.tributes:
        #     if tribute.gender == 'female':
        #         tribute.isAlive = False

        for i in range(18):
            self.arena.tributes[i].isAlive = False

        self.arena.clearDeadTributes()
        # self.arena.displayArena()
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
            reward -= 5
            gh.cleanUpAfterTurn(self.game, self.arena)
            if len(self.arena.tributes) == 1:
                reward += 20
                print(f"Tribute {self.arena.tributes[0].letter} wins!!")
                print("GAME OVER\n\n")
                return obs, reward, True, False, {}

            self.current_tribute_index = 0
            self.tribute = self.arena.tributes[self.current_tribute_index]
            return obs, reward, False, False, {}

        if action not in self.valid_actions:
            return obs, -1, False, False, {}
        
        gh.setValuesBeforeTurn(self.tribute, self.arena)

        # HANDLE ACTION
        if action == 0:
            direction = gh.getRandomValidMove(self.tribute, self.arena)
            gh.handleSingleMove(self.tribute, direction, self.arena)
            reward += 0.01
            # print(f"Tribute {self.tribute.letter} moved {direction}")

        elif action == 1:
            health_before = self.tribute.health
            kills_before = self.tribute.num_kills
            gh.handleAttack(self.tribute, self.arena)
            # print(f"Tribute {self.tribute.letter} attacked tribute")
            if self.tribute.num_kills > kills_before:
                reward += 15.0  # got a kill
            if self.tribute.health >= health_before:
                reward += 2.0  # won an attack
            

        elif action == 2:
            capacity_before = self.tribute.capacity
            weapon_before = self.tribute.weapon_value
            result = gh.handlePickup(self.tribute, self.arena)
            # print(f"Tribute {self.tribute.letter} picked up an item")
            if result == 1:
                reward += 0.5
                if self.tribute.capacity > capacity_before:
                    reward += 0.2  # picked up backpack
                if self.tribute.weapon_value > weapon_before:
                    reward += 0.2  # picked up weapon
                    if self.tribute.weapon_value > WEAK_WEAPON:
                        reward += 0.1  # weapon is strong

        elif action == 3:
            gh.handleEatFood(self.tribute)
            # print(f"Tribute {self.tribute.letter} ate food")
            reward += 1.0

        elif action == 4:
            gh.handleDrinkWater(self.tribute, self.arena)
            # print(f"Tribute {self.tribute.letter} drank water")
            reward += 1.0

        elif action == 5:
            gh.handleUseMedical(self.tribute)
            # print(f"Tribute {self.tribute.letter} used medical")
            reward += 1.0

        elif action == 6:
            health_before = self.tribute.health
            gh.handleSleep(self.tribute)
            # print(f"Tribute {self.tribute.letter} slept")
            if health_before <= 40:
                reward += 0.1

        elif action == 7:
            gh.handleRefillWater(self.tribute, self.arena)
            # print(f"Tribute {self.tribute.letter} refilled their canteen")
            reward += 1.0

        self.action_counts[action] += 1

        # stat penalties
        if self.tribute.hunger <= HUNGER_WARNING_THRESHOLD:
            reward -= 0.1
        if self.tribute.thirst <= THIRST_WARNING_THRESHOLD:
            reward -= 0.1
        if self.tribute.health <= 40:
            reward -= 0.1

        if not self.tribute.isAlive:
            print(f"Tribute {self.tribute.letter} died")

        
        if len(self.arena.tributes) == 1:
            terminated = True
            print(f"Tribute {self.tribute.letter} wins!!")

        gh.cleanUpAfterTurn(self.game, self.arena)

        if self.game.day_count >= 10:
            terminated = True

        if len(self.arena.tributes) == 0:
            terminated = True
            

        if terminated:
            print("____________________")
            print("GAME OVER")
            print("____________________\n\n")


            action_names = {0: 'move', 1: 'attack', 2: 'pickup', 3: 'eat', 4: 'drink', 5: 'medical', 6: 'sleep', 7: 'refill'}
            print(f"{'Action':<10} {'Count':<10}")
            print("-" * 20)
            for k, v in self.action_counts.items():
                print(f"{action_names[k]:<10} {v:<10}")
            self.action_counts = {i: 0 for i in range(8)}
            print("\n\n")
            return obs, reward, terminated, False, {}

        # move to next tribute
        self.tribute.turn_count += 1
        self.current_tribute_index += 1
        if self.current_tribute_index >= len(self.arena.tributes):
            self.game.turn_count += 1
            self.current_tribute_index = 0
            if self.game.turn_count % TURNS_PER_DAY == 0:
                self.game.day_count += 1
                print(f"=== DAY {self.game.day_count + 1} ===")
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