from math import floor
import os
from tqdm import tqdm
from Game import Game
from GameEnv import GameEnv
import tests.test_helper as th
from stable_baselines3 import PPO
import sys
from config import TURNS_PER_DAY
from contextlib import redirect_stdout
from log_helper import TrimmedFile



timesteps = 50000000
fine_tune_timesteps = 40000000
episodes = 100

# model params
verbose = 1
n_steps = 8192
ent_coef = 0.1
device = "cpu"
learning_rate = 0.00003




def collect_game_stats():

    all_rewards.append(game.game_rewards)
    all_moves.append(game.action_counts[0])
    all_attacks.append(game.action_counts[1])
    all_pickups.append(game.action_counts[2])
    all_eats.append(game.action_counts[3])
    all_drinks.append(game.action_counts[4])
    all_meds.append(game.action_counts[5])
    all_refills.append(game.action_counts[6])

def calulate_game_stats():
    retaliation_rate = game.retaliation_count / max(game.action_counts[1], 1)
    all_retaliation_rates.append(retaliation_rate)

    combat_death_rate = game.deaths_by_combat / 23
    gamemaker_death_rate = game.deaths_by_gamemaker / 23
    all_kill_rates.append(combat_death_rate)
    all_gm_kill_rates.append(gamemaker_death_rate)

    all_day_counts.append(game.day_count)

def get_averages():
    # get averages
    avg_rewards = sum(all_rewards) / episodes
    avg_rewards_per_tribute = (sum(all_rewards) / episodes) / 24
    avg_moves = sum(all_moves) / episodes
    avg_attacks = sum(all_attacks) / episodes
    avg_pickups = sum(all_pickups) / episodes
    avg_eats = sum(all_eats) / episodes
    avg_drinks = sum(all_drinks) / episodes
    avg_meds = sum(all_meds) / episodes
    avg_refills = sum(all_refills) / episodes
    avg_retal_rate = round((sum(all_retaliation_rates) / episodes) * 100, 2)
    avg_kill_rate = round((sum(all_kill_rates) / episodes) * 100, 2)
    avg_gm_kill_rate = round((sum(all_gm_kill_rates) / episodes) * 100, 2)
    avg_days = sum(all_day_counts) / episodes

    return avg_rewards, avg_rewards_per_tribute, avg_moves, avg_attacks, avg_pickups, avg_eats, avg_drinks, avg_meds, avg_refills, avg_retal_rate, avg_kill_rate, avg_gm_kill_rate, avg_days


def print_eval_results():
            avg_rewards, avg_rewards_per_tribute, avg_moves, avg_attacks, avg_pickups, avg_eats, avg_drinks, avg_meds, avg_refills, avg_retal_rate, avg_kill_rate, avg_gm_kill_rate, avg_days = get_averages()
            print("=" * 30)
            print("ACTION DISTRIBUTION")
            print("=" * 30)
            print(f'''move        {int(avg_moves)}
attack      {int(avg_attacks)}
pickup      {int(avg_pickups)}
eat         {int(avg_eats)}
drink       {int(avg_drinks)}
medical     {int(avg_meds)}
refill      {int(avg_refills)}
                  ''')
    

            # print results
            print("=" * 30)
            print("GAME STATS")
            print("=" * 30)
            print(f"Average Rewards: {round(avg_rewards, 2)}" ) 
            print(f"Average Rewards Per Tribute: {round(avg_rewards_per_tribute, 2)}" ) 
            print(f"Average Length: {round(avg_days)} days")
            print(f"-" * 30)
            print(f"Retaliation Rate: {avg_retal_rate}%")
            print(f"Death by Combat Rate: {avg_kill_rate}%")
            print(f"Death by Gamemaker Rate: {avg_gm_kill_rate}%")
            print("\n")




if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "--robot" # train, eval, robot, or play
    display = "--display" in sys.argv
    colors = "--color" in sys.argv
    print_moves = "--print" in sys.argv
    fine_tune = "--tune" in sys.argv

    
    if mode == "--train":

        # load the existing model and train with the hazard environment
        if fine_tune:
            with TrimmedFile("results_hazard.txt") as f:
                sys.stdout = f
                env = GameEnv(size=48)
                model = PPO.load(
                    "hunger_games_model", 
                    env=env, 
                    verbose=verbose, 
                    n_steps=n_steps, 
                    ent_coef=ent_coef, 
                    device=device, 
                    learning_rate=learning_rate
                    )
                model.learn(total_timesteps=fine_tune_timesteps)
                model.save("hunger_games_model_hazard")
                
        else: 
            with TrimmedFile("results.txt") as f:
                sys.stdout = f
                env = GameEnv(size=48)
                model = PPO("MultiInputPolicy",
                    env=env, 
                    verbose=verbose, 
                    n_steps=n_steps, 
                    ent_coef=ent_coef, 
                    device=device, 
                    learning_rate=learning_rate
                    )
                model.learn(total_timesteps=timesteps)
                model.save("hunger_games_model")

        sys.stdout = sys.__stdout__



        
    elif mode in ("--robot", "--eval"):
        # rewards
        all_rewards = []
        # action distribution
        all_moves = []
        all_attacks = []
        all_pickups = []
        all_eats = []
        all_drinks = []
        all_meds = []
        all_refills = []
        # retaliation
        all_retaliation_rates = []
        # kills
        all_kill_rates = []
        all_gm_kill_rates = []
        # game length
        all_day_counts = []
        
        # IF EVAL MODE - BATCH RUN
        if mode == "--eval":
            display

            print("The Hunger Games are underway...")

            with redirect_stdout(open(os.devnull, 'w')):
                for i in tqdm(range(episodes)):
                    game = Game(size=48, robot=True, train=False, test=False)
                    game.run(display, colors, save_frames=False)
                    collect_game_stats()
            
            calulate_game_stats()
            get_averages()
            print_eval_results()



        # IF NOT EVAL MODE - robot and single run, run with --robot

        else:
            game = Game(size=48, robot=True, train=False, test=False)
            if print_moves:
                game.run(display, colors, print_moves, save_frames=True)
            else:
                with tqdm() as pbar:
                    game.run(display, colors, print_moves, save_frames=True, progress=pbar)
                    
        

    elif mode == "--play": # THIS MODE IS PROBABLY BROKEN AT THIS POINT
        # load model into Robot, run Game
        game = Game(size=48)
        game.run()





