try:
    import pygame as pg
    from game.Game import Game
    from process.MenuProcess import MenuProcess

    pg.init()
    pg.mixer.init()
    game = Game()
    game.run(MenuProcess(game))
    pg.mixer.quit()
    pg.quit()
except:
    try:
        from traceback import format_exc
        from util.Logger import log

        log(format_exc())
    except:
        pass
