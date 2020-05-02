import pygame as pg
from Box2D import *
import pyganim as pga
from game.Game import Game
from config.Config import BOX2D_COEF


def toPix(x: float) -> float:
    return x / BOX2D_COEF


def toMeters(x: float) -> float:
    return x * BOX2D_COEF


class InGameObject:
    def __init__(self, game: Game, process, animation: pga.PygAnimation, body: b2Body):
        # process: GameProcess
        self.__body = body
        body.userData = self
        self.game = game
        self.process = process

        self.__animation = animation
        animation.scale(self.getAABB().size)
        animation.play()

    def update(self):
        pass

    def draw(self, dst):
        pos = self.getAABB().bottomleft
        self.__animation.blit(dst, (pos[0], -pos[1]))

    def getBody(self) -> b2Body:
        return self.__body

    def setPosition(self, x: int, y: int, angle: float = None):
        if angle is None:
            angle = self.__body.angle
        self.__body.transform = b2Vec2(toMeters(x), toMeters(y)), angle

    def getAABB(self):
        aabb = pg.Rect(0, 0, 0, 0)
        for fixture in self.__body.fixtures:
            if not isinstance(fixture.shape, b2PolygonShape):
                raise NotImplementedError("TODO")
            xs = list(map(lambda tpl: tpl[0], fixture.shape.vertices))
            ys = list(map(lambda tpl: tpl[1], fixture.shape.vertices))
            x = min(*xs)
            y = min(*ys)
            aabb = aabb.union(pg.Rect(x, y, max(*xs) - x, max(*ys) - y))

        return pg.Rect(*map(toPix, [aabb.x, aabb.y, aabb.w, aabb.h])).move(*self.getPosition())

    def getPosition(self):
        return tuple(map(toPix, self.__body.position.tuple))
