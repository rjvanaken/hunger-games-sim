import gameplay_handler as gh
from stable_baselines3 import PPO
import numpy as np
import os

class Player:

    def __init__(self, tribute, arena):
        self.tribute = tribute
        self.arena = arena
        tribute.arenaKnowledge = [[0 for _ in range(arena.size)] for _ in range(arena.size)]  # Start empty

class HumanPlayer(Player):
    def __init__(self, tribute, arena):
        super().__init__(tribute, arena)


    def displayMenu(self):
            print(f"\n\nACTION MENU: Tribute '{self.tribute.letter.upper()}'")
            print(
'''
0: move up
1: move down
2: move left
3: move right
4: attack
5: pick up item
6: eat
7: drink
8: heal
9: sleep
10: refill
11: skip tribute (debug)
12: quickmove (debug)
'''
)

    def get_tribute_letter(game, target=False):
        if target == False:
            letter = input(f"Enter a tribute letter (or exit to quit game): ").upper()
        else:
            letter = input(f"Enter a target tribute letter (or cancel to go back): ").upper()
        id = ord(letter) - ord(letter)
        return id


    def take_turn(self):
        
        self.tribute.segment = self.arena.getSegmentFromPos(self.tribute.pos)
        segment = self.tribute.segment
        self.arena.updateSegmentData(self.tribute, segment)

        self.tribute.updateStatsBeforeTurn()
            
        # keep looping until a valid action succeeds
        while True:

            self.displayMenu()

            action = input("ENTER CHOICE: ")
            success = False

            try:

                if action == "0":
                    success = gh.handleSingleMove(self.tribute, 'up', self.arena)

                elif action == "1":
                    success = gh.handleSingleMove(self.tribute, 'down', self.arena)
                    
                elif action == "2":
                    success = gh.handleSingleMove(self.tribute, 'left', self.arena)

                elif action == "3":
                    success = gh.handleSingleMove(self.tribute, 'right', self.arena)

                elif action == "4":
                    success = gh.handleAttack(self.tribute, self.arena)

                elif action == "5":
                    resource = self.arena.getResourceAt(self.tribute.pos)
                    if resource is None:
                        print("No resource at your position.")
                    else:
                        success = gh.handlePickup(self.tribute, self.arena)

                elif action == "6":
                    success = gh.handleEatFood(self.tribute)

                elif action == "7":
                    success = gh.handleDrinkWater(self.tribute, self.arena)

                elif action == "8":
                    success = gh.handleUseMedical(self.tribute)

                elif action == "9":
                    success = gh.handleSleep(self.tribute)

                elif action == "10":
                    success = gh.handleRefillWater(self.tribute, self.arena)

                elif action == "11":
                    success = "skip" # debug

                elif action == "12":
                    success = gh.handleMove(self.tribute, self.arena) #debug
                else:
                    print("Invalid choice, try again.")

            except Exception as e:
                print(f"Action failed: {e}")

            if success:
                # self.arena.displayArena() # temporary - ultimately, will only print at start of each day
                break
                





class BotPlayer(Player):
    def __init__(self, tribute, arena, model_path="hunger_games_model"):
        super().__init__(tribute, arena)
        self.model = PPO.load(model_path) if os.path.exists(model_path + ".zip") else None
        self.valid_actions = set()
        self.turn_count = 0
        

    def take_turn(self):
        while True:
            
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
            action, _ = self.model.predict(obs)
            action = int(action)
            success = False

            if action not in self.valid_actions:
                continue

            else:

                if action == 0:          
                    direction = gh.getRandomValidMove(self.tribute, self.arena)
                    success = gh.handleSingleMove(self.tribute, direction, self.arena)
                    print(f"Tribute {self.tribute.letter} moved {direction}")

                elif action == 1:
                    success = gh.handleAttack(self.tribute, self.arena)
                    print(f"Tribute {self.tribute.letter} attacked tribute")

                elif action == 2:
                    success = gh.handlePickup(self.tribute, self.arena)
                    print(f"Tribute {self.tribute.letter} picked up an item")

                elif action == 3:
                    success = gh.handleEatFood(self.tribute)
                    print(f"Tribute {self.tribute.letter} ate food")

                elif action == 4:
                    success = gh.handleDrinkWater(self.tribute, self.arena)
                    print(f"Tribute {self.tribute.letter} drank water")

                elif action == 5:
                    success = gh.handleUseMedical(self.tribute)
                    print(f"Tribute {self.tribute.letter} used medical")

                elif action == 6:
                    success = gh.handleRefillWater(self.tribute, self.arena)
                    print(f"Tribute {self.tribute.letter} refilled their canteen")

            if success:
                self.turn_count += 1
                # self.arena.displayArena() # temporary - ultimately, will only print at start of each day
                break

