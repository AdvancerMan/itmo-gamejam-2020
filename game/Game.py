import pygame as pg
from process.Process import Process
from config.Config import *


class Game:
    def __init__(self):
        self.__processesStack = []
        self.__popped = False
        self.__screen = None
        self.__running = False

    def addProcess(self, process: Process):
        self.__processesStack.append(process)

    def popProcess(self):
        self.__popped = True

    def __popProcess(self):
        if self.__popped:
            self.__processesStack.pop()

    def __init(self):
        self.__screen = pg.display.set_mode(WINDOW_RESOLUTION)
        pg.display.set_caption("Hello world!")
        self.__running = True

    def stop(self):
        self.__running = False

    def run(self, process: Process):
        self.__init()
        self.__processesStack.append(process)
        while len(self.__processesStack) > 0 and self.__running:
            process = self.__processesStack[-1]
            process.processEvents(pg.event.get())
            process.update()
            self.__screen.fill(BACKGROUND_COLOR)
            process.draw(self.__screen)
            pg.display.update()
            self.__popProcess()


class GameProcess(Process):
    def __init__(self, game: Game):
        self.__game = game

    def processEvents(self, events: list):
        for e in events:
            if e.type == pg.QUIT:
                self.__game.stop()


if __name__ == "__main__":
    pg.init()
    game = Game()
    game.run(GameProcess(game))
