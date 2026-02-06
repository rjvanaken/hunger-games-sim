from Game import Game


def main():
        # In main or wherever you create the game
    game = Game(size=21)
    game.addTributes(game.arena.center)
    game.displayGrid()




if __name__ == '__main__':
    main()