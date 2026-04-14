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

class GameEnv(gym.Env):
    
    def __init__(self, size):    
        super().__init__()
            
        self.game = Game(size=48, robot=True, train=True)
        self.arena = self.game.arena
        self.gamemaker = self.game.gamemaker
        self.tribute = None
        self.ACTION_MAP = {0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7}
        self.valid_actions = set()
 
        self.arena.clearDeadTributes(self.game)
        self.arena.displayArena()

        VIEW_RADIUS = 2

        self.action_space = spaces.Discrete(7)

        self.observation_space = spaces.Dict({
            "local_view": spaces.Box(low=0, high=10, shape=(5, 5), dtype=np.int32),
            "known_water_row": spaces.Discrete(49),
            "known_water_col": spaces.Discrete(49),
            "health": spaces.Discrete(101),
            "hunger": spaces.Discrete(101),
            "thirst": spaces.Discrete(101),
            "row": spaces.Discrete(49),
            "col": spaces.Discrete(49),
            "recently_attacked": spaces.Discrete(2),
        })



    def check_game_over(self, obs, reward):
        if len(self.arena.tributes) <= 1:
            if len(self.arena.tributes) == 1:
                print(f"Tribute {self.arena.tributes[0].letter} wins!!")
            self.game.print_results()
            return obs, reward, True, False, {}
        return None

    def reset(self, **kwargs):
        self.game = Game(size=48, robot=True, train=True)
        self.arena = self.game.arena
        self.gamemaker = self.game.gamemaker
        self.arena.clearDeadTributes(self.game)
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
            "recently_attacked": self.tribute.recently_attacked
        }

        return obs, {}

    def step(self, action):
        reward = 0
        terminated = False
        self.valid_actions = gh.setupActionMap(self.tribute, self.arena, self.game)

        obs = {
            "local_view": gh.getLocalView(self.tribute, self.arena),
            "health": self.tribute.health,
            "hunger": self.tribute.hunger,
            "thirst": self.tribute.thirst,
            "row": self.tribute.pos[0],
            "col": self.tribute.pos[1],
            "known_water_row": gh.getKnownWater(self.tribute)[0],
            "known_water_col": gh.getKnownWater(self.tribute)[1],
            "recently_attacked": self.tribute.recently_attacked
        }
        
        was_near_hazard = self.tribute.near_hazard
        was_in_warning = self.tribute.hazard_warning_zone
        
        gh.setValuesBeforeTurn(self.tribute, self.arena)

        
        result = self.check_game_over(obs, reward)
        if result is not None:
            return result
        

        if action not in self.valid_actions:
            return obs, -1, False, False, {}
        
        # if len(self.arena.tributes) <= TRIBUTE_PROXIMITY_TRIGGER:
        #     if gh.isNearAnyTribute(self.tribute, self.arena): 
        #         reward += NEAR_TRIBUTE_REWARD

        if action == 0:
            direction = gh.getRandomValidMove(self.tribute, self.arena)
            gh.handleSingleMove(self.tribute, direction, self.arena)
            reward += MOVE_REWARD

        elif action == 1:
            health_before = self.tribute.health
            kills_before = self.tribute.num_kills
            gh.handleAttack(self.tribute, self.arena, print_moves=False)
            reward += ATTACK_REWARD
            if self.tribute.recently_attacked:
                self.game.retaliation_count += 1
                reward += CONTINUE_FIGHT_REWARD
                self.tribute.recently_attacked = 0

            if self.tribute.num_kills > kills_before:
                reward += KILL_REWARD
            if self.tribute.health >= health_before:
                reward += WIN_ATTACK_REWARD

        elif action == 2:
            very_hungry = False
            capacity_before = self.tribute.capacity
            weapon_before = self.tribute.weapon_value
            if self.tribute.hunger < HUNGER_WARNING_THRESHOLD:
                very_hungry = True
            food_before = self.tribute.getFood()
            result = gh.handlePickup(self.tribute, self.arena)
            reward += PICKUP_REWARD
            if self.tribute.getFood() > food_before:
                if very_hungry:
                    reward += FOOD_PICKUP_REWARD
            if self.tribute.capacity > capacity_before:
                if self.tribute.capacity - capacity_before == LARGE_CAPACITY:
                    reward += LARGE_BACKPACK_REWARD
                elif self.tribute.capacity - capacity_before == SMALL_CAPACITY:
                    reward += SMALL_BACKPACK_REWARD
            elif self.tribute.weapon_value > weapon_before:
                if self.tribute.weapon_value - weapon_before == STRONG_WEAPON:
                    reward += STRONG_WEAPON_REWARD
                elif self.tribute.weapon_value - weapon_before == WEAK_WEAPON:
                    reward += WEAK_WEAPON_REWARD
                


        elif action == 3:
            very_hungry = False
            if self.tribute.hunger <= HUNGER_WARNING_THRESHOLD:
                very_hungry = True
            gh.handleEatFood(self.tribute)
            reward += EAT_REWARD
            if very_hungry:
                reward += VERY_HUNGRY_BONUS

        elif action == 4:
            very_thirsty = False
            if self.tribute.thirst <= THIRST_WARNING_THRESHOLD:
                very_thirsty = True
            gh.handleDrinkWater(self.tribute, self.arena)
            reward += DRINK_REWARD
            if very_thirsty:
                reward += VERY_THIRSTY_BONUS

        elif action == 5:
            very_low_health = False
            if self.tribute.health <= HEALTH_THRESHOLD:
                very_low_health = True
            gh.handleUseMedical(self.tribute)
            reward += MEDICAL_REWARD
            if very_low_health:
                reward += VERY_LOW_HEALTH_BONUS

        elif action == 6:
            gh.handleRefillWater(self.tribute, self.arena)
            reward += REFILL_REWARD

        self.game.action_counts[action] += 1

        # after action, before next turn:
        if self.tribute.hunger <= HUNGER_WARNING_THRESHOLD:
            reward -= LOW_HUNGER_PENALTY
        if self.tribute.thirst <= THIRST_WARNING_THRESHOLD:
            reward -= LOW_THIRST_PENALTY
        if self.tribute.health <= HEALTH_THRESHOLD:
            reward -= LOW_HEALTH_PENALTY

        
        # if self.tribute.hazard_warning_zone and not was_in_warning:
        #     reward -= ENTERED_WARNING_ZONE_PENALTY
        # if self.tribute.near_hazard and was_in_warning:
        #     reward -= ENTERED_HAZARD_PENALTY
        # if self.tribute.hazard_warning_zone and was_near_hazard:
        #     reward += MOVED_AWAY_FROM_HAZARD_REWARD
        # if self.tribute.near_hazard and was_near_hazard:
        #     reward -= STAYED_NEAR_HAZARD_PENALTY

        if self.tribute.near_hazard:
            reward -= ENTERED_HAZARD_PENALTY
        if not self.tribute.near_hazard and was_near_hazard:
            reward += MOVED_AWAY_FROM_HAZARD_REWARD


        if not self.tribute.isAlive:
            # print(f"Tribute {self.tribute.letter} died")
            reward -= DEATH_PENALTY

        self.game.game_rewards += reward

        gh.cleanUpAfterTurn(self.game, self.arena)

        result = self.check_game_over(obs, reward)
        if result is not None:
            return result

        if self.game.day_count >= 10:
            terminated = True

        if terminated:
            self.game.print_results()
            return obs, reward, terminated, False, {}

        self.tribute.turn_count += 1
        self.current_tribute_index += 1
        if self.current_tribute_index >= len(self.arena.tributes): #all tributes have gone, new round
            self.game.turn_count += 1
            self.gamemaker.assessInterference(self.game)
            self.current_tribute_index = 0
            if self.game.turn_count > 0 and self.game.turn_count % TURNS_PER_DAY == 0:
                self.game.day_count += 1
                for tribute in self.arena.tributes:
                    tribute.health = min(100, tribute.health + int(SLEEP_VALUE * (tribute.hunger / 100)))
                    # print(f"{tribute.letter}, health: {tribute.health}, hunger: {tribute.hunger}, thirst: {tribute.thirst}") 
                gh.cleanUpAfterTurn(self.game, self.arena)

                result = self.check_game_over(obs, reward)
                if result is not None:
                    return result
                
                self.game.deaths_per_day[self.game.day_count + 1] = {"decay": 0, "combat": 0, "gamemaker": 0}
                self.game.arena.hazard.wasDeployedToday = False
                self.game.arena.bomb.wasDeployedToday = False
                
                print(f"=== DAY {self.game.day_count + 1} ===")

        if self.current_tribute_index >= len(self.arena.tributes):
            result = self.check_game_over(obs, reward)
            if result is not None:
                return result
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
            "recently_attacked": self.tribute.recently_attacked
        }

        return obs, reward, terminated, False, {}