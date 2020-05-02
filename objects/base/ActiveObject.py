import pygame as pg
import pyganim as pga
from Box2D import *
from game.Game import Game
from objects.base.InGameObject import InGameObject
from objects.guns.UsualGun import UsualGun
from util.FloatCmp import lessOrEquals
from util.Rectangle import Rectangle
from util.textures.AnimationPack import AnimationName, AnimationPack


class ActiveObject(InGameObject):
    def __init__(self, game: Game, process, animation: AnimationPack, body: b2Body,
                 speed: float, jumpPower: float):
        # process: GameProcess
        InGameObject.__init__(self, game, process, animation, body)
        self.__speed = speed
        self.__jumpPower = jumpPower
        self.__grounds = set()
        self.__gun = UsualGun(game, process)
        self.__directedToRight = True
        self.__acting = False

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

    def postUpdate(self):
        self.updateAnimation()

    def go(self, speed):
        if self.isOnGround():
            self.getAnimation().setAnimation(AnimationName.RUN)
        self.getBody().ApplyForceToCenter(b2Vec2(speed, 0), True)
        self.__acting = True

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
        self.__gun.spawnBullet()

    def isOnGround(self):
        return len(self.__grounds) > 0

    def beginContact(self, obj, contact: b2Contact):
        aabb = (self.getAABB(), obj.getAABB())
        if lessOrEquals(aabb[1].y + aabb[1].h, aabb[0].y):
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
