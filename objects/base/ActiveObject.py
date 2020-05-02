import pyganim as pga
from Box2D import *
from game.Game import Game
from objects.base.InGameObject import InGameObject
from objects.guns.UsualGun import UsualGun
from util.FloatCmp import lessOrEquals


class ActiveObject(InGameObject):
    def __init__(self, game: Game, process, animation: pga.PygAnimation, body: b2Body,
                 speed: float, jumpPower: float):
        # process: GameProcess
        InGameObject.__init__(self, game, process, animation, body)
        self.__speed = speed
        self.__jumpPower = jumpPower
        self.__grounds = set()
        self.__gun = UsualGun(game, process)

    def go(self, speed):
        self.getBody().ApplyForceToCenter(b2Vec2(speed, 0), True)

    def goLeft(self):
        self.go(-self.__speed)

    def goRight(self):
        self.go(self.__speed)

    def jump(self):
        if self.isOnGround():
            self.getBody().linearVelocity = b2Vec2(self.getBody().linearVelocity.x, self.__jumpPower)

    def shoot(self):
        self.__gun.spawnBullet()

    def isOnGround(self):
        return len(self.__grounds) > 0

    def beginContact(self, obj, contact: b2Contact):
        aabb = (self.getAABB(), obj.getAABB())
        if lessOrEquals(aabb[1].y + aabb[1].h, aabb[0].y):
            self.__grounds.add(obj)

    def endContact(self, obj, contact: b2Contact):
        self.__grounds.discard(obj)
