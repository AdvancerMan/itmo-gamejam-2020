import pygame as pg
from game.Game import Game
from process.Process import Process


class RainbowProcess(Process):
    def __init__(self, game: Game, step: int = 1, maxValue: int = 100):
        self.__game = game
        self.__color = [maxValue, 0, 0]
        self.__changingColor = 2
        self.__step = step
        self.__maxValue = maxValue

    def setStep(self, step: int):
        self.__step = step

    def processEvents(self, events: list):
        for e in events:
            if e.type == pg.QUIT:
                self.__game.stop()

    def update(self):
        self.__color[abs(self.__changingColor) - 1] += self.__step if self.__changingColor > 0 else -self.__step
        if self.__changingColor > 0 and self.__color[abs(self.__changingColor) - 1] == self.__maxValue:
            self.__changingColor = (self.__changingColor + 1) % 3 + 1
            self.__changingColor *= -1
        elif self.__changingColor < 0 and self.__color[abs(self.__changingColor) - 1] == 0:
            self.__changingColor *= -1
            self.__changingColor = (self.__changingColor + 1) % 3 + 1

    def draw(self, screen: pg.Surface):
        screen.fill(tuple(map(lambda x: x / self.__maxValue * 255, self.__color)))


if __name__ == "__main__":
    pg.init()
    game = Game()
    game.run(RainbowProcess(game))
