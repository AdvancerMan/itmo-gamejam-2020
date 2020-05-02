import pygame as pg
import pyganim as pga
from Box2D import *
from game.Game import Game
from objects.base.InGameObject import InGameObject
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
        self.hp = PLAYER_HP

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

    def draw(self, dst: pg.Surface, cameraRect: Rectangle):
        InGameObject.draw(self, dst, cameraRect)
