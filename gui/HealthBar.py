import pygame as pg
from game.Game import Game
from util.Rectangle import Rectangle, rectFromSize
from util.textures.Textures import TextureInfo


class HealthBar:
    def __init__(self, game: Game):
        self.__upper = game.getTextureManager().getTexture(TextureInfo.HEALTH_BAR_UPPER)
        self.__lower = game.getTextureManager().getTexture(TextureInfo.HEALTH_BAR_LOWER)
        self.__bar = game.getTextureManager().getTexture(TextureInfo.HEALTH_BAR)
        self.__rect = rectFromSize(0, 0, *self.__lower.get_size())

    def __getTexture(self, health: float, maxHealth: float) -> pg.Surface:
        result = self.__lower.copy()
        transparent = pg.Surface(self.__bar.get_size(), pg.SRCALPHA)

        x = (health / maxHealth - 1) * self.__bar.get_size()[0]
        transparent.blit(self.__bar, (x, 0))

        result.blit(transparent, (3, 0))
        result.blit(self.__upper, (0, 0))
        return result

    def getWidth(self) -> float:
        return self.__lower.get_size()[0]

    def getHeight(self) -> float:
        return self.__lower.get_size()[1]

    def draw(self, dst: pg.Surface, pos: tuple, health: float, maxHealth: float):
        dst.blit(self.__getTexture(health, maxHealth), pos)
