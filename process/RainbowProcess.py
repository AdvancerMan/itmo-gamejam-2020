import pygame as pg
from game.Game import Game
from process.Process import Process
from util.Textures import AnimationInfo


class RainbowProcess(Process):
    def __init__(self, game: Game, step: int = 1, maxValue: int = 100):
        self.__game = game
        self.__color = [maxValue, 0, 0]
        self.__changingColor = 2
        self.__step = step
        self.__maxValue = maxValue

        self.__playerAnimation = game.getTextureManager().getAnimation(AnimationInfo.FRIEND_ANIMATION)
        self.__playerAnimation.play()
        self.__coords = [50, 50]
        self.__coordsChange = [0, 0]

    def setStep(self, step: int):
        self.__step = step

    def processEvents(self, events: list):
        for e in events:
            if e.type == pg.QUIT:
                self.__game.stop()
            elif e.type == pg.KEYUP or e.type == pg.KEYDOWN:
                d = 1 if e.type == pg.KEYDOWN else -1
                if e.key == pg.K_LEFT:
                    self.__coordsChange[0] -= d
                elif e.key == pg.K_RIGHT:
                    self.__coordsChange[0] += d
                elif e.key == pg.K_UP:
                    self.__coordsChange[1] -= d
                elif e.key == pg.K_DOWN:
                    self.__coordsChange[1] += d

    def update(self):
        self.__color[abs(self.__changingColor) - 1] += self.__step if self.__changingColor > 0 else -self.__step
        if self.__changingColor > 0 and self.__color[abs(self.__changingColor) - 1] >= self.__maxValue:
            self.__changingColor = (self.__changingColor + 1) % 3 + 1
            self.__changingColor *= -1
        elif self.__changingColor < 0 and self.__color[abs(self.__changingColor) - 1] <= 0:
            self.__changingColor *= -1
            self.__changingColor = (self.__changingColor + 1) % 3 + 1

        self.__coords = list(map(sum, zip(self.__coords, self.__coordsChange)))

    def draw(self, screen: pg.Surface):
        screen.fill(tuple(map(lambda x: max(min(x / self.__maxValue * 255, 255), 0), self.__color)))
        self.__playerAnimation.blit(screen, tuple(self.__coords))
