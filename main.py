from Game import Game

def main():
        # In main or wherever you create the game
    game = Game(size=48)
    game.addTributes(game.arena.center)
    game.arena.addCornucopia()
    for tribute in game.arena.tributes:
        tribute.arenaKnowledge = game.arena.arena_grid
    game.arena.addSources()
    game.arena.addTrees(0.15)
    game.arena.displayArena()

    game.run()







if __name__ == '__main__':
    main()





# every frame runs "hit spacebar or not"
'''
starts off hitting it every time 
figures out its own function for bar location, distance, and figure it out
model reinforces how to update itself based on the event and its result and the variables together

dont hard code words
at every location, you can do actions, blah blah
and then allow it to do those things and calcualte the success


hazards that can kill then
hazards might have class and damage level
ways to heal
actions taking to avoid those hazards
optimizing for not dying

bomb spces results in death
ok bomb spaces do not go to
avoid the bombs



2 things to work on
wait till learn RL in class - way you do it will be consistent to what you were taught in class
in mean time
gamemaker is not RL and instead will be SOMETHING ELSE maybe?

Go slow, keep the arena and total number of things small for now
some things put together to ease in gamemaker 
- if you can quantify drama that's cool
- well we want people to run into one another
- higher likelihood of fighting
- almost die but not fully

start with rules based or random algorithm just to try out getting code built and working
then optimize for leveraging RL later

- maybe do flappy bird with RL to learn
the output, with the research is, with all these constraints, what would be a dramatic game
which games are dramatic 
gamemaker updats the state of the board or whatever
- next tick and turn, here's a new set of information
- build training loop around with current information had, with matrix, did you die or did you not die
---- or did it lead to decreased health or not

gamemaker - did it increase or decrease drama? - as it learns
models canlearn how to look ahead, take an action to decrease drama right now

---


wii bowling, bowl from here, left, right, turn, did you get a good score

define what the game is and the rules of the game
define it as if it is a board game

keep it simple and add more later

beginning
- food
- water
- 2 types of hazards

-- h: bomb and sets you on fire, takes damage every turn uhtil you get to water
-- h: mutt
define lookahead: they cannot see the whole map they don't know what's coming
they can only see this much, go walk this direction, search for water


'''