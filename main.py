from Game import Game
from GameEnv import GameEnv
import tests.test_helper as th
from stable_baselines3 import PPO
import sys




if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "--play"
    
    if mode == "--train":
        env = GameEnv(size=48)
        model = PPO("MultiInputPolicy", env, verbose=1, n_steps=8192)
        model.learn(total_timesteps=2000000)
        model.save("hunger_games_model")
        
    elif mode == "--play":
        # load model into Robot, run Game
        game = Game(size=48)
        game.run()



# def main():
        
#     game = th.setupTestArena()
#     for tribute in game.arena.tributes:
#         tribute.arenaKnowledge = game.arena.arena_grid
#     game.arena.displayArena()


#     game.run()

