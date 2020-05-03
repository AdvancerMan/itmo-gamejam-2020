import pygame as pg
import pyganim as pga
from game.Game import Game
from objects.friendly.Player import Player
from objects.platforms.HalfCollidedPlatform import HalfCollidedPlatform
from util.Rectangle import Rectangle, rectFromSize, iterSum
from util.textures.AnimationPack import AnimationPack, AnimationName
from util.textures.Textures import AnimationInfo, TextureInfo


class BasePlatform(HalfCollidedPlatform):
    def __init__(self, game: Game, process, x: float, y: float):
        HalfCollidedPlatform.__init__(self, game, process, x, y, 106, 9,
                                      AnimationPack({AnimationName.STAY:
                                                         pga.PygAnimation([(pg.Surface((20, 20), pg.SRCALPHA), 100)])
                                                     }))

    def hide(self):
        self._notColliding.clear()
        self.getBody().active = False

    def show(self):
        self.getBody().active = True


class Base:
    def __init__(self, game: Game, process, x, y, player: Player):
        self.__animation = game.getTextureManager().getAnimation(AnimationInfo.BASE_ANIMATION)
        self.__animation.play()
        self.__light = game.getTextureManager().getTexture(TextureInfo.LIGHT_BASE)
        self.__turnedOn = False
        self.__player = player
        self.__rect = rectFromSize(x, y, *self.__light.get_size())

        self.__lowerPlatform = BasePlatform(game, process, x, y)
        self.__upperPlatform = BasePlatform(game, process, x,
                                            y + self.__light.get_size()[1] - self.__lowerPlatform.getAABB().h)

    def isTurnedOn(self):
        return self.__turnedOn

    def preUpdate(self, delta: float):
        if self.__player.getAABB().intersects(self.__rect):
            self.__turnedOn = True
        else:
            self.__turnedOn = False
        self.__lowerPlatform.setPosition(*self.__rect.pos())
        self.__upperPlatform.setPosition(self.__rect.x,
                                         self.__rect.y + self.__light.get_size()[1] - self.__lowerPlatform.getAABB().h)
        self.__lowerPlatform.preUpdate(delta)
        self.__upperPlatform.preUpdate(delta)

    def postUpdate(self):
        self.__lowerPlatform.postUpdate()
        self.__upperPlatform.postUpdate()

    def getDrawPos(self, cameraRect: Rectangle, x: int, y: int) -> tuple:
        x, y = iterSum(map(lambda x: -x, cameraRect.pos()), (x, y))
        return x, cameraRect.h - y

    def draw(self, dst: pg.Surface, cameraRect: Rectangle):
        if cameraRect.intersects(self.__rect):
            pos = self.getDrawPos(cameraRect, *self.__rect.pos())
            pos = (pos[0], pos[1] - self.__light.get_size()[1])
            self.__animation.blit(dst, pos)
            if self.__turnedOn:
                dst.blit(self.__light, pos)
            self.__lowerPlatform.draw(dst, cameraRect)
            self.__upperPlatform.draw(dst, cameraRect)
