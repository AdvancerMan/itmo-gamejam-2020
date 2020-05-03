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

    def getTexture(self, health: float, maxHealth: float) -> pg.Surface:
        result = self.__lower.copy()
        transparent = pg.Surface(self.__bar.get_size(), pg.SRCALPHA)

        x = (health / maxHealth - 1) * self.__bar.get_size()[0]
        transparent.blit(self.__bar, (x, 0))

        result.blit(transparent, (0, 0))
        result.blit(self.__upper, (0, 0))
        return result

    def draw(self, src: pg.Surface, cameraRect: Rectangle, pos: tuple, health: float, maxHealth: float):
        if self.__rect.intersects(cameraRect):
            src.blit(self.getTexture(health, maxHealth), pos)
