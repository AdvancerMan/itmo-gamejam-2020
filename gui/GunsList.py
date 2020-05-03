import pygame as pg
import pyganim as pga
from game.Game import Game
from util.Rectangle import iterSum
from util.textures.Textures import TextureInfo


class GunsList:
    def __init__(self, game: Game, pos: tuple):
        self.__background = pg.transform.scale2x(game.getTextureManager().getTexture(TextureInfo.GUNS_BACKGROUND))
        self.__pos = pos
        self.__guns = [game.getTextureManager().getTexture(info)
                       for info in (TextureInfo.GUN1,
                                    TextureInfo.GUN2,
                                    TextureInfo.GUN3)]
        self.__detGuns = [game.getTextureManager().getTexture(info)
                          for info in (TextureInfo.DETALIZED_GUN1,
                                       TextureInfo.DETALIZED_GUN2,
                                       TextureInfo.DETALIZED_GUN3)]
        self.__numbers = list(map(pg.transform.scale2x, game.getTextureManager().getNumbers()))
        self.__i = 0

        self.__guns = list(map(pg.transform.scale2x, self.__guns))
        self.__detGuns = list(map(pg.transform.scale2x, self.__detGuns))

    def __getI(self, di: int) -> int:
        return (self.__i + di + len(self.__guns)) % len(self.__guns)

    def switchRight(self):
        self.__i = self.__getI(1)

    def switchLeft(self):
        self.__i = self.__getI(-1)

    def draw(self, dst: pg.Surface, ammoRemaining: int):
        dst.blit(self.__background, self.__pos)
        dst.blit(self.__guns[self.__getI(-1)], iterSum(self.__pos, (0, 14)))
        dst.blit(self.__detGuns[self.__i], iterSum(self.__pos, (38, 4)))
        dst.blit(self.__guns[self.__getI(1)], iterSum(self.__pos, (104, 14)))
        if ammoRemaining < 10:
            dst.blit(self.__numbers[ammoRemaining], iterSum(self.__pos, (64, 56)))
        else:
            dst.blit(self.__numbers[ammoRemaining // 10], iterSum(self.__pos, (56, 56)))
            dst.blit(self.__numbers[ammoRemaining % 10], iterSum(self.__pos, (70, 56)))
