from GameController import GameController


def main():
    con = GameController(21)
    con.addTributes(con.arena.c_pos)
    con.displayGrid()

if __name__ == '__main__':
    main()