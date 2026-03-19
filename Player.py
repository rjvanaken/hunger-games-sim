import gameplay_handler
from stable_baselines3 import PPO
import numpy as np

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
        # if asleep, skip turn but decrement sleep counter
        if self.tribute.isAsleep:
            self.tribute.num_sleep_turns -= 1
            if self.tribute.num_sleep_turns == 0:
                self.tribute.isAsleep = False
            return
            
        # keep looping until a valid action succeeds
        while True:

            self.displayMenu()

            action = input("ENTER CHOICE: ")
            success = False

            try:

                if action == "0":
                    success = gameplay_handler.handleSingleMove(self.tribute, 'up')

                elif action == "1":
                    success = gameplay_handler.handleSingleMove(self.tribute, 'down')
                    
                elif action == "2":
                    success = gameplay_handler.handleSingleMove(self.tribute, 'left')

                elif action == "3":
                    success = gameplay_handler.handleSingleMove(self.tribute, 'right')

                elif action == "4":
                    success = gameplay_handler.handleAttack(self.tribute, self.arena)

                elif action == "5":
                    resource = self.arena.getResourceAt(self.tribute.pos)
                    if resource is None:
                        print("No resource at your position.")
                    else:
                        success = gameplay_handler.handlePickup(self.tribute, self.arena)

                elif action == "6":
                    success = gameplay_handler.handleEatFood(self.tribute)

                elif action == "7":
                    success = gameplay_handler.handleDrinkWater(self.tribute, self.arena)

                elif action == "8":
                    success = gameplay_handler.handleUseMedical(self.tribute)

                elif action == "9":
                    success = gameplay_handler.handleSleep(self.tribute)

                elif action == "10":
                    success = gameplay_handler.handleRefillWater(self.tribute, self.arena)

                elif action == "11":
                    success = "skip" # debug

                elif action == "12":
                    success = gameplay_handler.handleMove(self.tribute, self.arena) #debug
                else:
                    print("Invalid choice, try again.")

            except Exception as e:
                print(f"Action failed: {e}")

            if success:
                self.arena.displayArena() # temporary - ultimately, will only print at start of each day
                break
                





class BotPlayer(Player):
    def __init__(self, tribute, arena, model_path):
        super().__init__(tribute, arena)
        self.model = PPO.load(model_path)

        self.ACTION_MAP = {0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9, 10: 10}






    # this calls the functions from the handler which runs the verification on the functions. This is just
    # the menu validation. Only 2 functions. Display menu and the ones to handle it. And the loop? Or is the loop in 
    # main wi