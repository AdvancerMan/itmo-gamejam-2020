from Box2D import *


class InGameObject:
    def __init__(self, body: b2Body):
        self.__body = body

    def getBody(self) -> b2Body:
        return self.__body

    def setPosition(self, x: int, y: int, angle: float = None):
        if angle is None:
            angle = self.__body.angle
        self.__body.transform = b2Vec2(x, y), angle
