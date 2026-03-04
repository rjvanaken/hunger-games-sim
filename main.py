from Game import Game

def main():
        # In main or wherever you create the game
    game = Game(size=50)
    game.addTributes(game.arena.center)
    game.arena.addCornucopia()
    game.arena.addSources()
    game.arena.addTrees(0.15)
    game.arena.displayArena()

    game.run()







if __name__ == '__main__':
    main()