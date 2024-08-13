from classes import *


if __name__ == "__main__":
    game = Mainscreen()
    game.loop()

    lvl_1 = Level_1()
    lvl_1.game_loop()

    lvl_2 = Level_2()
    lvl_2.game_loop()

    lvl_3 = Level_3()
    lvl_3.game_loop()

    victory = Victory()
    victory.loop()