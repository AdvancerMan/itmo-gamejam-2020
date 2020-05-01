import pyganim as pga
from Box2D import *
from game.Game import Game
from objects.base.InGameObject import InGameObject
from objects.guns.UsualGun import UsualGun

class ActiveObject(InGameObject):
    def __init__(self, game: Game, process, animation: pga.PygAnimation, body: b2Body,
                 speed: float, jumpPower: float):
        # process: GameProcess
        InGameObject.__init__(self, game, process, animation, body)
        self.__speed = speed
        self.__jumpPower = jumpPower
        self.__gun = UsualGun(game, process)

    def go(self, speed):
        self.getBody().ApplyLinearImpulse(b2Vec2(speed * self.getBody().mass, 0), b2Vec2(0, 0), True)

    def goLeft(self):
        self.go(-self.__speed)

    def goRight(self):
        self.go(self.__speed)

    def jump(self):
        self.getBody().ApplyLinearImpulse(b2Vec2(0, self.__jumpPower * self.getBody().mass), b2Vec2(), True)

    def shoot(self):
        self.__gun.spawnBullet()
        pass
