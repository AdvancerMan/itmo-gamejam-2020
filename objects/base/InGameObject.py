import pygame as pg
from Box2D import *
import pyganim as pga
from game.Game import Game
from config.Config import BOX2D_COEF
from util.Rectangle import Rectangle, rectFromTwoPoints, rectFromSize


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
        animation.scale(tuple(map(int, self.getAABB().size())))
        animation.play()

    def update(self):
        pass

    def draw(self, dst: pg.Surface, cameraRect: Rectangle):
        aabb = self.getAABB()
        if aabb.intersects(cameraRect):
            aabb.move(*map(lambda x: -x, cameraRect.pos()))
            self.__animation.blit(dst, (aabb.x, cameraRect.h - aabb.y - aabb.h))

    def getBody(self) -> b2Body:
        return self.__body

    def setPosition(self, x: int, y: int, angle: float = None):
        if angle is None:
            angle = self.__body.angle
        self.__body.transform = b2Vec2(toMeters(x), toMeters(y)), angle

    def getAABB(self) -> Rectangle:
        aabb = rectFromTwoPoints(0, 0, 0, 0)
        for fixture in self.__body.fixtures:
            if not isinstance(fixture.shape, b2PolygonShape):
                # TODO aabb for not polygon shapes
                raise NotImplementedError("TODO")
            xs = list(map(lambda tpl: tpl[0], fixture.shape.vertices))
            ys = list(map(lambda tpl: tpl[1], fixture.shape.vertices))
            aabb.union(rectFromTwoPoints(min(*xs), min(*ys), max(*xs), max(*ys)))
        return rectFromSize(*map(toPix, [aabb.x, aabb.y, aabb.w, aabb.h])).move(*self.getPosition())

    def getPosition(self):
        return tuple(map(toPix, self.__body.position.tuple))
