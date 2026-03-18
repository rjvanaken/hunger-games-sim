import gameplay_handler

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
0: quickmove
1: singleMove ('u', 'd', 'l', 'r')
2: attack
3: pick up item
4: eat
5: drink
6: heal
7: sleep
8: refill
9: skip tribute (debug)
10: print stats (debug)
''')

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
                    success = gameplay_handler.handleMove(self.tribute, self.arena)

                elif action == "1":
                    direction = input("Please enter direction ('up', 'down', 'left', 'right'): ")
                    success = gameplay_handler.handleSingleMove(direction)

                elif action == "2":
                    target_id = self.get_tribute_letter(target=True)
                    target = self.arena.tributes[target_id]
                    success = gameplay_handler.handleAttack(self.tribute, target)

                elif action == "3":
                    resource = self.arena.getResourceAt(self.tribute.pos)
                    if resource is None:
                        print("No resource at your position.")
                    else:
                        success = gameplay_handler.handlePickup(self.tribute, self.arena)

                elif action == "4":
                    success = gameplay_handler.handleEatFood(self.tribute)

                elif action == "5":
                    success = gameplay_handler.handleDrinkWater(self.tribute, self.arena)

                elif action == "6":
                    success = gameplay_handler.handleUseMedical(self.tribute)

                elif action == "7":
                    success = gameplay_handler.handleSleep(self.tribute)

                elif action == "8":
                    success = gameplay_handler.handleRefillWater(self.tribute, self.arena)

                elif action == "9":
                    success = "skip"
                else:
                    print("Invalid choice, try again.")

            except Exception as e:
                print(f"Action failed: {e}")

            if success:
                self.arena.displayArena() # temporary - ultimately, will only print at start of each day
                break
                


#⭐⭐⭐⭐⭐⭐⭐ REMEMBER: need to add a property trigger for when a segment the tribute is currently in changes in any way, their knowledge of that segment is updated too




    # class BotPlayer(Player):



    # player needs to have the arena instance

    # game creates tributes and stores it, creates and arena, and the player takes a given tribute
    # and the arena 

    # this calls the functions from the handler which runs the verification on the functions. This is just
    # the menu validation. Only 2 functions. Display menu and the ones to handle it. And the loop? Or is the loop in 
    # main with run_manual? ugh



    # PLAYER OBJECT ASSIGNED TRIBUTE
    ## if human
    ## take turns - either human takes turn or 
    ## also a gamemaker type 
    ### human tribute
    ### robot tribute
    ### human gamemaker
    ### robot gamemaker


    ## player is parent class
    ## it has enum for the 4 types
    # or no? PLAYER has 

    # contain a tribute and combine human or bot interaction with game logic

    # parent class PLAYER has do turn action
    # game loop runs through the game and does the loop

    # game loop doesnt know its a bot list vs human list jisgt that its player
    # override is needed to target its subclass not its player class













    # this calls the functions from the handler which runs the verification on the functions. This is just
    # the menu validation. Only 2 functions. Display menu and the ones to handle it. And the loop? Or is the loop in 
    # main wi