import gymnasium as gym
from gymnasium import spaces
from Game import Game
import numpy as np

class HungerGamesEnv(gym.Env):
    def __init__(self, game):
        self.action_space = spaces.Discrete(4)
        self.observation_space = spaces.Box(
            low=0,
            high=100,
            shape=(48 * 48,),
            dtype=float
        )
        self.game = game
        


    def reset(self):  
        self.game.addTributes(self.game.arena.center)
        self.game.arena.addCornucopia()
        for tribute in self.game.arena.tributes:
            tribute.arenaKnowledge = self.game.arena.arena_grid
        self.game.arena.addSources()
        self.game.arena.addTrees(0.15)
        self.game.arena.displayArena()



    def step(self, action):
        if action == 0:
            self.arena.player.tribute.singleMove('u')

        elif action == 1:
            self.arena.player.tribute.singleMove('d')

        elif action == 2:
            self.arena.tribute.singleMove('l')
            
        elif action == 3:
            self.arena.player.tribute.singleMove('r')

        reward = 0
        new_state = self.get_state()
        truncated = False
        info = {}
        if self.arena.player.
        terminated = False
        
        return new_state, reward, terminated, truncated, info



    def get_state(self):
        flat = []
        for row in self.arena.player.tribute.arenaKnowledge:
            for cell in row:
                if cell is None:
                    flat.append(0)
                else:
                    flat.append(ord(cell))
        return np.array(flat, dtype=float)