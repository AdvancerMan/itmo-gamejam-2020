import pyganim as pga
from Box2D import *
from game.Game import Game
from objects.base.InGameObject import InGameObject


class Bullet(InGameObject):
    def __init__(self, game, process, animation: pga.PygAnimation,
                 speed: float, body: b2Body):
        InGameObject.__init__(self, game, process, animation, body)

        self.getBody().linearVelocity = b2Vec2(100.0, 0.0)  # TODO fix speed

        self.setPosition(100, -100, 0)


class Gun:
    def __init__(self, game: Game, process, bulletanim: pga.PygAnimation, bulletbody: b2Body,
                 gunanim: pga.PygAnimation, gunbody: b2Body, params: dict):
        # process: GameProcess
        self.__game = game
        self.__process = process
        self.__params = params      # params = {"bulletSpeed"}
                                    # maybe add "deviation" and "angle"?
        self.__bulletAnimation = bulletanim
        self.__gunAnimation = gunanim
        self.__bulletBody = bulletbody
        self.__gunBody = gunbody

    def spawnBullet(self):
        # print(self.__params['bulletSpeed'])
        self.__process.addObject(Bullet(self.__game, self.__process, self.__bulletAnimation,
                                        self.__params['bulletSpeed'], self.__bulletBody))
