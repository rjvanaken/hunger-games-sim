"""
main.py - Entry point for the Hunger Games RL simulation.

Supports four runtime modes (passed as command-line arguments):
  --train   : Train a new PPO model from scratch, or fine-tune an existing one by adding on --tune
  --eval    : Batch-run the trained model over many episodes and print aggregate stats
  --robot   : Run a single episode with the trained model (default mode)
  --play    : (Experimental) Human-playable mode

CITATIONS:
    - stable-baselines3: used for PPO training and inference
"""

from math import floor
import os
from tqdm import tqdm
from Game import Game
from GameEnv import GameEnv
import tests.test_helper as th
from stable_baselines3 import PPO
import sys
from config import TURNS_PER_DAY, BASE_MODEL, TUNED_MODEL, PLAY_MODEL
from contextlib import redirect_stdout
from log_helper import TrimmedFile





timesteps = 50000000
fine_tune_timesteps = 25000000
episodes = 3000

# model params
verbose = 1
n_steps = 8192
ent_coef = 0.1
device = "cpu"
learning_rate = 0.00003




def collect_game_stats():
    """Append per-episode action counts, rewards, game length, and loop end conditions to their respective tracking lists."""

    all_rewards.append(game.game_rewards)
    all_end_conditions.append(game.end_condition)
    all_day_counts.append(game.day_count + 1)
    all_moves.append(game.action_counts[0])
    all_attacks.append(game.action_counts[1])
    all_pickups.append(game.action_counts[2])
    all_eats.append(game.action_counts[3])
    all_drinks.append(game.action_counts[4])
    all_meds.append(game.action_counts[5])
    all_refills.append(game.action_counts[6])
    all_day1_deaths.append(game.day_one_kills)
    all_combat_victories.append(game.victory_by_combat)
    all_exceeded_training_caps.append(game.exceeded_training_cap)




def calulate_game_stats():

    """
    Compute derived per-episode statistics (retaliation rate, cornucopia pickup rate,
    cause-of-death breakdown) and append them to their tracking lists.
    
    - Retaliation rate: fraction of attacks that were responses to being attacked first.
    - Cornucopia rate: fraction of cornucopia items picked up out of total available.
    - End conditions: what caused the loop to end
    """

    retaliation_rate = game.retaliation_count / max(game.action_counts[1], 1)
    cornucopia_rate = game.cornucopia_pickups / len(game.arena.cornucopia)
    desperate_use_rate = game.desperate_resource_uses / max(game.action_counts[3] + game.action_counts[4] + game.action_counts[5] + game.action_counts[2], 1)
    all_desperate_use_rates.append(desperate_use_rate)
    all_retaliation_rates.append(retaliation_rate)
    all_cornucopia_rates.append(cornucopia_rate)

    combat_death_rate = game.deaths_by_combat / 23
    gamemaker_death_rate = game.deaths_by_gamemaker / 23
    
    all_kill_rates.append(combat_death_rate)
    all_gm_kill_rates.append(gamemaker_death_rate)


def get_averages():
    """
    Calculates the averages for the stats to be reported for eval mode
    """
    avg_rewards = sum(all_rewards) / episodes
    avg_rewards_per_tribute = (sum(all_rewards) / episodes) / 24
    avg_moves = sum(all_moves) / episodes
    avg_attacks = sum(all_attacks) / episodes
    avg_pickups = sum(all_pickups) / episodes
    avg_eats = sum(all_eats) / episodes
    avg_drinks = sum(all_drinks) / episodes
    avg_meds = sum(all_meds) / episodes
    avg_refills = sum(all_refills) / episodes
    avg_day1_deaths = round(sum(all_day1_deaths) / episodes)
    avg_retal_rate = round((sum(all_retaliation_rates) / episodes) * 100, 2)
    avg_kill_rate = round((sum(all_kill_rates) / episodes) * 100, 2)
    avg_gm_kill_rate = round((sum(all_gm_kill_rates) / episodes) * 100, 2)
    avg_days = sum(all_day_counts) / episodes
    avg_cornucopia_rate = round((sum(all_cornucopia_rates) / episodes) * 100, 2)
    avg_winner_ends = round((all_end_conditions.count('winner') / episodes) * 100, 2)
    avg_mutual_decay_ends = round((all_end_conditions.count('mutual_decay') / episodes) * 100, 2)
    avg_combat_victory_rate = round((sum(all_combat_victories) / max(all_end_conditions.count('winner'), 1)) * 100, 2)
    exceeded_training_cap_rate = round((sum(all_exceeded_training_caps) / episodes) * 100, 2)
    avg_desperate_use_rates = round((sum(all_desperate_use_rates) / episodes) * 100, 2)
    


    return avg_rewards, avg_rewards_per_tribute, avg_moves, avg_attacks, avg_pickups, avg_eats, avg_drinks, avg_meds, avg_refills, avg_retal_rate, avg_kill_rate, avg_gm_kill_rate, avg_days, avg_cornucopia_rate, avg_winner_ends, avg_mutual_decay_ends, avg_day1_deaths, avg_combat_victory_rate, exceeded_training_cap_rate, avg_desperate_use_rates

def print_eval_results():
            
            """Print the results of running in --eval mode."""
            length = 37
            print(f"\nMODEL: {PLAY_MODEL}.zip")

            avg_rewards, avg_rewards_per_tribute, avg_moves, avg_attacks, avg_pickups, avg_eats, avg_drinks, avg_meds, avg_refills, avg_retal_rate, avg_kill_rate, avg_gm_kill_rate, avg_days, avg_cornucopia_rate, avg_winner_ends, avg_mutual_decay_ends, avg_day1_deaths, avg_combat_victory_rate, exceeded_training_cap_rate, avg_desperate_use_rates = get_averages()
            print("=" * length)
            print("ACTION DISTRIBUTION")
            print("=" * length)
            print(f'''move        {int(avg_moves)}
attack      {int(avg_attacks)}
pickup      {int(avg_pickups)}
eat         {int(avg_eats)}
drink       {int(avg_drinks)}
medical     {int(avg_meds)}
refill      {int(avg_refills)}
                  ''')
    

            
            
            
            

            # print results
            print("=" * length)
            print("GAME STATS")
            print("=" * length)
            print(f"Average Rewards: {round(avg_rewards, 2)}" ) 
            print(f"Average Rewards Per Tribute: {round(avg_rewards_per_tribute, 2)}" ) 
            print(f"Average Length: {round(avg_days)} days")
            print(f"Average Day 1 Deaths: {avg_day1_deaths}" ) #TODO 
            
            print(f"-" * length)
            print(f"Retaliation Rate: {avg_retal_rate}%")
            print(f"Cornucopia Pickup Rate: {avg_cornucopia_rate}%")
            print(f"Death by Combat Rate: {avg_kill_rate}%")
            print(f"Death by Gamemaker Rate: {avg_gm_kill_rate}%")
            print(f"-" * length)
            print(f"Combat Victory Rate: {avg_combat_victory_rate}%" ) #TODO 
            print(f"Desperate Resource Use Rate: {avg_desperate_use_rates}%\n" ) #TODO
            
            print("=" * length)
            print("END CONDITIONS")
            print("=" * length)
            print(f"✨ Winner Rate: {avg_winner_ends}%")
            print(f"👍 Mutual Decay Rate: {avg_mutual_decay_ends}%")
            print(f"-" * length)
            print(f"❌ Passed Training Cap Rate: {exceeded_training_cap_rate}%") # make it training cap, use new flag #TODO
            print("=" * length)
            print("\n")




if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "--robot" # train, eval, robot, or play
    display = "--display" in sys.argv
    colors = "--color" in sys.argv
    print_moves = "--print" in sys.argv
    fine_tune = "--tune" in sys.argv

    
    if mode == "--train":

        # load the existing model and fine-tune it
        if fine_tune:
            with TrimmedFile("results_tune.txt") as f:
                sys.stdout = f
                env = GameEnv(size=48)
                model = PPO.load(
                    BASE_MODEL, 
                    env=env, 
                    verbose=verbose, 
                    n_steps=n_steps, 
                    ent_coef=ent_coef, 
                    device=device, 
                    learning_rate=learning_rate
                    )
                model.learn(total_timesteps=fine_tune_timesteps)
                model.save(TUNED_MODEL)
                
        else: 
            # run training from scratch
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
                model.save(BASE_MODEL)

        sys.stdout = sys.__stdout__



        
    elif mode in ("--robot", "--eval"):
        # rewards
        all_rewards = []
        # actions
        all_moves = []
        all_attacks = []
        all_pickups = []
        all_eats = []
        all_drinks = []
        all_meds = []
        all_refills = []
        all_cornucopia_rates = []
        all_desperate_use_rates = []
        # retaliation
        all_retaliation_rates = []
        # kills
        all_kill_rates = []
        all_gm_kill_rates = []
        # game details
        all_day_counts = []
        all_end_conditions = []
        all_day1_deaths = []
        all_combat_victories = []
        all_exceeded_training_caps = []

        
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
            print_eval_results()



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





