import pygame as pg
from game.Game import Game
from process.Process import Process
from util.textures.Textures import AnimationInfo


class RainbowProcess(Process):
    def __init__(self, game: Game, nextProcess, step: int = 1, maxValue: int = 100):
        self.__game = game
        self.__color = [maxValue, 0, 0]
        self.__changingColor = 2
        self.__step = step
        self.__maxValue = maxValue

        self.__nextProcess = nextProcess

        self.__pressAnyKey = pg.font.SysFont("Segoe Script", 48)\
            .render("Press any key to start the game", True, (0, 0, 0))

    def setStep(self, step: int):
        self.__step = step

    def processEvents(self, events: list):
        for e in events:
            if e.type == pg.QUIT:
                self.__game.stop()
            elif e.type == pg.KEYDOWN or e.type == pg.MOUSEBUTTONDOWN:
                self.__game.replaceProcess(self.__nextProcess(self.__game))

    def update(self, delta: float):
        self.__color[abs(self.__changingColor) - 1] += self.__step if self.__changingColor > 0 else -self.__step
        if self.__changingColor > 0 and self.__color[abs(self.__changingColor) - 1] >= self.__maxValue:
            self.__changingColor = (self.__changingColor + 1) % 3 + 1
            self.__changingColor *= -1
        elif self.__changingColor < 0 and self.__color[abs(self.__changingColor) - 1] <= 0:
            self.__changingColor *= -1
            self.__changingColor = (self.__changingColor + 1) % 3 + 1

    def draw(self, dst: pg.Surface):
        dst.fill(tuple(map(lambda x: max(min(x / self.__maxValue * 255, 255), 0), self.__color)))
        dst.blit(self.__pressAnyKey, (152, 100))
