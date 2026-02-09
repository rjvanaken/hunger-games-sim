from Game import Game


def main():
        # In main or wherever you create the game
    game = Game(size=10)
    print(game.arena.center)
    game.addTributes(game.arena.center)
    game.arena.addCornucopia()
    game.displayGrid()




if __name__ == '__main__':
    main()