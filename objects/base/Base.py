import pygame as pg
import pyganim as pga
from Box2D import *
from game.Game import Game
from config.Config import BASE_SPEED, HEAL_COOLDOWN, AMMO_COOLDOWN, BASE_DISAPPEAR_TIME, BASE_APPEAR_TIME
from objects.friendly.Player import Player
from objects.platforms.HalfCollidedPlatform import HalfCollidedPlatform
from util.FloatCmp import equals
from util.Rectangle import Rectangle, rectFromSize, iterSum
from util.textures.Textures import AnimationInfo, TextureInfo, AnimationPack, AnimationName


class BasePlatform(HalfCollidedPlatform):
    def __init__(self, game: Game, process, x: float, y: float):
        HalfCollidedPlatform.__init__(self, game, process, x, y, 212, 30,
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
        self.__animation.scale2x()
        self.__animation.play()
        self.__light = pg.transform.scale2x(game.getTextureManager().getTexture(TextureInfo.LIGHT_BASE))
        self.__badBase = pg.transform.scale2x(game.getTextureManager().getTexture(TextureInfo.BAD_BASE))
        self.__turnedOn = False
        self.__player = player
        self.__rect = rectFromSize(x, y, *self.__light.get_size())

        self.__path = []
        self.__originalPath = []
        self.__movingTo = b2Vec2(0, 0)
        self.__pos = b2Vec2(x, y)
        self.__speed = BASE_SPEED

        self.__healCooldown = HEAL_COOLDOWN
        self.__sinceLastHeal = self.__healCooldown
        self.__ammoCooldown = AMMO_COOLDOWN
        self.__sinceLastAmmo = self.__ammoCooldown

        self.__sinceLastDisappear = 0
        self.__disappearMoment = BASE_DISAPPEAR_TIME
        self.__appearMoment = self.__disappearMoment + BASE_APPEAR_TIME

        self.__lowerPlatform = BasePlatform(game, process, x, y)
        self.__upperPlatform = BasePlatform(game, process, x,
                                            y + self.__light.get_size()[1] - self.__lowerPlatform.getAABB().h)

    def isTurnedOn(self):
        return self.__turnedOn

    def updatePosition(self, delta: float):
        direction = self.__movingTo - b2Vec2(*self.__rect.getCenter())
        length = direction.length
        if equals(length, 0) and len(self.__path) != 0:
            self.__setPoint(self.__path.pop())
        if len(self.__path) == 0:
            self.__path = [x for x in self.__originalPath]
        if not equals(length, 0):
            self.__pos += direction / length * self.__speed * min(1, length / self.__speed)
        self.__rect.setPos(*self.__pos.tuple)

    def preUpdatePlatforms(self, delta: float):
        self.__lowerPlatform.setPosition(*self.__rect.pos())
        self.__upperPlatform.setPosition(self.__rect.x,
                                         self.__rect.y + self.__light.get_size()[1] - self.__lowerPlatform.getAABB().h)
        self.__lowerPlatform.preUpdate(delta)
        self.__upperPlatform.preUpdate(delta)

    def preUpdate(self, delta: float):
        self.updatePosition(delta)
        self.__sinceLastDisappear += delta
        self.__sinceLastAmmo += delta
        self.__sinceLastHeal += delta
        if self.__player.getAABB().intersects(self.__rect):
            self.__turnedOn = True
        else:
            self.__turnedOn = False
        self.preUpdatePlatforms(delta)

    def postUpdate(self):
        if self.__sinceLastDisappear > self.__disappearMoment:
            if self.__sinceLastDisappear > self.__appearMoment:
                self.__lowerPlatform.getBody().active = True
                self.__upperPlatform.getBody().active = True
                self.__sinceLastDisappear = 0
            else:
                self.__lowerPlatform.getBody().active = False
                self.__upperPlatform.getBody().active = False
        elif self.__turnedOn:
            if self.__healCooldown <= self.__sinceLastHeal:
                self.__player.heal(1)
                self.__sinceLastHeal = 0
            if self.__ammoCooldown <= self.__sinceLastAmmo:
                self.__player.incrementAmmo()
                self.__sinceLastAmmo = 0
        self.__lowerPlatform.postUpdate()
        self.__upperPlatform.postUpdate()

    def __getDrawPos(self, cameraRect: Rectangle, x: int, y: int) -> tuple:
        x, y = iterSum(map(lambda x: -x, cameraRect.pos()), (x, y))
        return x, cameraRect.h - y

    def draw(self, dst: pg.Surface, cameraRect: Rectangle):
        if cameraRect.intersects(self.__rect):
            pos = self.__getDrawPos(cameraRect, *self.__rect.pos())
            pos = (pos[0], pos[1] - self.__light.get_size()[1])
            self.__animation.blit(dst, pos)
            if self.__sinceLastDisappear > self.__disappearMoment:
                dst.blit(self.__badBase, pos)
            elif self.__turnedOn:
                dst.blit(self.__light, pos)
            self.__lowerPlatform.draw(dst, cameraRect)
            self.__upperPlatform.draw(dst, cameraRect)

    def __setPoint(self, point: tuple):
        self.__movingTo = b2Vec2(point[:2])
        if len(point) == 3:
            self.__speed = point[2]
        else:
            self.__speed = BASE_SPEED

    def setPath(self, path: list):
        # path: list of tuples of 2 float --- points that base will be sent to
        self.__path = list(reversed(path))
        self.__originalPath = [x for x in self.__path]
        if len(self.__path) > 0:
            self.__setPoint(self.__path.pop())
