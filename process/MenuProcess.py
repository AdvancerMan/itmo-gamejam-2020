import pygame as pg
from game.Game import Game
from process.Process import Process


class MenuProcess(Process):
    def __init__(self, game: Game):
        self.__game = game

    def processEvents(self, events: list):
        for e in events:
            if e.type == pg.QUIT:
                self.__game.stop()


if __name__ == "__main__":
    pg.init()
    game = Game()
    game.run(MenuProcess(game))
