import gameplay_handler

class Player:

    def __init__(self, tribute, arena):
        self.tribute = tribute
        self.arena = arena


class HumanPlayer(Player):
    def __init__(self, tribute, arena):
        super().__init__(tribute, arena)

    def displayMenu():
            
        print("ACTION MENU\n")
        print('''
        1: move
        2: attack
        3: pick up item
        4: eat
        5: drink
        6: heal
        7: sleep
        -----------------------------
        0: SELECT NEW TRIBUTE
    ''')

    def get_tribute_letter(game, target=False):
        if target == False:
            letter = input(f"Enter a tribute letter (or exit to quit game): ").upper()
        else:
            letter = input(f"Enter a target tribute letter (or cancel to go back): ").upper()
        id = ord(letter) - ord(letter)
        return id


    def take_turn(self):
        if self.isAsleep:
            if self.num_sleep_turns == 0 and self.isAsleep == True:
                self.isAsleep == False
            # letter = input("Enter a tribute letter (or exit to quit): ").upper()
            # id = ord(letter) - ord(letter)
            # # wait noooooo we don't need to entrer a tribute number anymore
            # # because we are rotating turns instead.
            # # that needs to be completed.
            # # then this is just a "heres the menu, pick one, end turn"
            # if letter == 'EXIT':
            #     exit
            # if letter == "Y" or letter == "Z":
            #     print("Invalid letter, try again\n")
            # elif self.arena.tributes[id].isAlive != False:
            #     print("Tribute is dead. Pick another\n")
            # else:
                # maybe need to do an else here and put another error before it goes into the inner loop for the menu? idk
        else:
            self.displayMenu()
            action = input("ENTER CHOICE: ")
            if action == "1":
                try:
                    gameplay_handler.handleMove()
                except Exception as e:
                    print(e)
            
            if action == "2":
                id = self.get_tribute_letter(False)
                try:
                    # well wait a minute once again how do I get the current and target tribute?
                    # I know I have that value from the other thing but its rejecting it right now
                    gameplay_handler.handleAttack(self.tribute, self.arena.tributes[id])
                except Exception as e:
                    print(e)
            
            if action == "3":
                if self.arena.arena_grid[self.tribute.pos[0]][self.tribue.pos[1]] != 0:
                    resource = self.arena.getResourceAt(self.tribute.pos)
                    try:
                        gameplay_handler.handlePickup(self.tribute, resource)
                    except Exception as e:
                        print(e)

            if action == "4":
                try:
                    gameplay_handler.handleEatFood(self.tribute)
                except Exception as e:
                    print(e)
            if action == "5":
                try:
                    gameplay_handler.handleDrinkWater(self.tribute)
                except Exception as e:
                    print(e)
            if action == "6":
                try:
                    gameplay_handler.handleUseMedial(self.tribute)
                except Exception as e:
                    print(e)

            if action == "7":
                if self.tribute.isAsleep == False:
                    try:
                        gameplay_handler.handleSleep(self.tribute)
                    except Exception as e:
                        print(e)  
            # manual loop?



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