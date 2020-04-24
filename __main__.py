try:
    import pygame as pg
    from game.Game import Game
    from process.MenuProcess import MenuProcess

    pg.init()
    game = Game()
    game.run(MenuProcess(game))
    pg.quit()
except:
    try:
        from traceback import format_exc
        from util.Logger import log

        log(format_exc())
    except:
        print("ERROR IN LOGGING")
