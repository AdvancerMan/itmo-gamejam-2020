from Box2D import *
from game.Game import Game
import pyganim as pga


class InGameObject:
    def __init__(self, game: Game, animation: pga.PygAnimation, body: b2Body):
        self.__body = body
        self.__game = game
        self.__animation = animation

    def update(self):
        pass

    def draw(self, dst):
        self.__animation.blit(dst, self.__body.position)

    def getBody(self) -> b2Body:
        return self.__body

    def setPosition(self, x: int, y: int, angle: float = None):
        if angle is None:
            angle = self.__body.angle
        self.__body.transform = b2Vec2(x, y), angle
