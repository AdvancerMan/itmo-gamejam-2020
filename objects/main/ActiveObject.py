import pygame as pg
import pyganim as pga
from Box2D import *
from game.Game import Game
from gui.HealthBar import HealthBar
from objects.main.InGameObject import InGameObject
from objects.guns.PlayerGuns import *
from util.FloatCmp import lessOrEquals, less, equals
from util.Rectangle import Rectangle
from util.textures.AnimationPack import AnimationName, AnimationPack
from config.Config import *


class ActiveObject(InGameObject):
    def __init__(self, game: Game, process, animation: AnimationPack, body: b2Body,
                 speed: float, jumpPower: float, guns: list):
        # process: GameProcess
        InGameObject.__init__(self, game, process, animation, body)
        self.__speed = speed
        self.__jumpPower = jumpPower
        self.__grounds = set()
        self.guns = guns
        self.__directedToRight = True
        self.__xVel = 0
        self.__acting = False  # used to make proper animation
        self.__lastShoot = 10   # more then any cooldown
        self.shootAngle = b2Vec2(1, 0)  # shoot direction
        self.__hp = 1.0
        self.__maxHp = 1.0
        self._healthBar = HealthBar(game)

    def resetHp(self, maxHp: float):
        self.__maxHp = maxHp
        self.__hp = maxHp

    def updateAnimation(self):
        if self.getAnimation().isFinished():
            if self.getAnimation().getAnimationName() == AnimationName.JUMP:
                self.getAnimation().setAnimation(AnimationName.FALL)
            elif self.getAnimation().getAnimationName() == AnimationName.LANDING:
                self.getAnimation().setAnimation(AnimationName.STAY)

        if self.getAnimation().getAnimationName() != AnimationName.JUMP and not self.isOnGround():
            self.getAnimation().setAnimation(AnimationName.FALL)

        if self.getAnimation().getAnimationName() \
                not in (AnimationName.JUMP, AnimationName.FALL, AnimationName.LANDING) \
                and not self.__acting:
            self.getAnimation().setAnimation(AnimationName.STAY)
        self.__acting = False

    def preUpdate(self, delta: float):
        self.angleUpdate()
        self.__lastShoot += delta

    def postUpdate(self):
        self.getBody().ApplyLinearImpulse(b2Vec2((self.__xVel - self.getBody().linearVelocity.x) / 5, 0),
                                          self.getBody().worldCenter, True)
        self.__xVel = 0
        self.updateAnimation()

    def go(self, speed):
        if self.isOnGround():
            self.getAnimation().setAnimation(AnimationName.RUN)
        self.__acting = True
        self.__xVel = speed

    def goLeft(self):
        self.setDirection(False)
        self.go(-self.__speed)

    def goRight(self):
        self.setDirection(True)
        self.go(self.__speed)

    def jump(self):
        if self.isOnGround():
            # TODO probably not the best solution
            self.__grounds.clear()

            self.getAnimation().setAnimation(AnimationName.JUMP)
            self.getBody().linearVelocity = b2Vec2(self.getBody().linearVelocity.x, self.__jumpPower)

    def shoot(self):
        if self.__lastShoot > self.guns[0].cooldown:
            self.guns[0].spawnBullet(self)
            self.__lastShoot = 0

    def takeDamage(self, amount: float):
        # TODO invulnerability after taking damage
        self.__hp -= amount       # gameprocess, removeobject
        if self.__hp <= 0:
            self.process.removeObject(self)

    def changeGunRight(self):
        self.__lastShoot = 0
        for i in range(len(self.guns) - 1):
            self.guns[i], self.guns[i + 1] = self.guns[i + 1], self.guns[i]

    def changeGunLeft(self):
        self.__lastShoot = 0
        for i in range(len(self.guns) - 1, 0, -1):
            self.guns[i], self.guns[i - 1] = self.guns[i - 1], self.guns[i]

    def isOnGround(self):
        return len(self.__grounds) > 0

    def beginContact(self, obj, contact: b2Contact):
        if self.isAbove(obj):
            if not self.isOnGround():
                self.getAnimation().setAnimation(AnimationName.LANDING)
            self.__grounds.add(obj)

    def endContact(self, obj, contact: b2Contact):
        self.__grounds.discard(obj)

    def setDirection(self, toRight: bool):
        if toRight != self.__directedToRight:
            self.__directedToRight = toRight
            self.getAnimation().flip(True)

    def isDirectedToRight(self) -> bool:
        return self.__directedToRight

    def angleUpdate(self):
        if self.__directedToRight:
            self.shootAngle = b2Vec2(1, 0)
        else:
            self.shootAngle = b2Vec2(-1, 0)

    def changeDirection(self):
        self.setDirection(not self.__directedToRight)

    def _draw(self, dst: pg.Surface, aabb: Rectangle, pos: tuple):
        super()._draw(dst, aabb, pos)
        size = aabb.size()
        pos = (pos[0] + size[0] / 2 - self._healthBar.getWidth() / 2, pos[1] - self._healthBar.getWidth())
        self._healthBar.draw(dst, pos, self.__hp, self.__maxHp)

    def getSpeed(self) -> float:
        return self.__speed
