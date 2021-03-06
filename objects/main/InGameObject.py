import pygame as pg
from Box2D import *
from game.Game import Game
from config.Config import BOX2D_COEF
from util.FloatCmp import lessOrEquals
from util.Rectangle import Rectangle, rectFromTwoPoints, rectFromSize
from util.textures.Textures import AnimationPack


def toPix(x: float) -> float:
    return x / BOX2D_COEF


def toMeters(x: float) -> float:
    return x * BOX2D_COEF


class InGameObject:
    def __init__(self, game: Game, process, animation: AnimationPack, body: b2Body):
        assert isinstance(animation, AnimationPack)
        # process: GameProcess
        self.__body = body
        self.__killed = False
        body.userData = self
        self.game = game
        self.process = process
        self.__animation = animation
        animation.scale(tuple(map(int, self.getAABB().size())))

    def preUpdate(self, delta: float):
        pass

    def postUpdate(self):
        pass

    def getAnimation(self) -> AnimationPack:
        return self.__animation

    def _draw(self, dst: pg.Surface, aabb: Rectangle, pos: tuple):
        self.__animation.blit(dst, pos)

    def _postDraw(self, dst: pg.Surface, aabb: Rectangle, pos: tuple):
        pass

    def postDraw(self, dst: pg.Surface, cameraRect: Rectangle):
        if not self.__body.active:
            return
        aabb = self.getAABB()
        if aabb.intersects(cameraRect):
            camPos = cameraRect.pos()
            self._postDraw(dst, aabb, (aabb.x - camPos[0], cameraRect.h - aabb.y - aabb.h + camPos[1]))

    def draw(self, dst: pg.Surface, cameraRect: Rectangle):
        if not self.__body.active:
            return
        aabb = self.getAABB()
        if aabb.intersects(cameraRect):
            camPos = cameraRect.pos()
            self._draw(dst, aabb, (aabb.x - camPos[0], cameraRect.h - aabb.y - aabb.h + camPos[1]))

    def getBody(self) -> b2Body:
        return self.__body

    def setTransform(self, x: float, y: float, angle: float = None):
        if angle is None:
            angle = self.__body.angle
        self.__body.transform = b2Vec2(toMeters(x), toMeters(y)), angle

    def setPosition(self, x: float, y: float):
        size = self.getAABB().size()
        self.setTransform(x + size[0] / 2, y + size[1] / 2)

    def isAbove(self, obj):
        objAABB = obj.getAABB()
        return lessOrEquals(objAABB.y + objAABB.h, self.getAABB().y)

    def getAABB(self) -> Rectangle:
        aabb = rectFromTwoPoints(0, 0, 0, 0)
        for fixture in self.__body.fixtures:
            if isinstance(fixture.shape, b2PolygonShape):
                xs = list(map(lambda tpl: tpl[0], fixture.shape.vertices))
                ys = list(map(lambda tpl: tpl[1], fixture.shape.vertices))
                aabb.union(rectFromTwoPoints(min(*xs), min(*ys), max(*xs), max(*ys)))
            elif isinstance(fixture.shape, b2CircleShape):
                r = fixture.shape.radius
                pos = fixture.shape.pos - b2Vec2(r, r)
                aabb.union(rectFromSize(*pos, 2 * r, 2 * r))
            else:
                raise NotImplementedError("Now game supports only polygon and circle shapes")
        return rectFromSize(*map(toPix, [aabb.x, aabb.y, aabb.w, aabb.h])).move(*self.getPosition())

    def getPosition(self):
        return tuple(map(toPix, self.__body.position.tuple))

    def getStrType(self):
        return ""

    def takeDamage(self, amount: float, ignoreInvulnerability: bool = False):
        pass

    def isLand(self) -> bool:
        return True

    def beginContact(self, obj, contact: b2Contact):
        """
        WARNING: You cannot create/destroy Box2D entities inside this callback.
        Called when two fixtures begin to touch.
        copied from https://box2d.org/documentation/classb2_contact_listener.html
        """
        pass

    def endContact(self, obj, contact: b2Contact):
        """
        WARNING: You cannot create/destroy Box2D entities inside this callback.
        Called when two fixtures cease to touch.
        copied from https://box2d.org/documentation/classb2_contact_listener.html
        """
        pass

    def preSolve(self, obj, contact: b2Contact, oldManifold: b2Manifold):
        """
        WARNING: You cannot create/destroy Box2D entities inside this callback.
        This lets you inspect a contact after the solver is finished.
        This is useful for inspecting impulses.
        Note: the contact manifold does not include time of impact impulses,
        which can be arbitrarily large if the sub-step is small.
        Hence the impulse is provided explicitly in a separate data structure.
        Note: this is only called for contacts that are touching, solid, and awake.
        copied from https://box2d.org/documentation/classb2_contact_listener.html
        """
        pass

    def postSolve(self, obj, contact: b2Contact, impulse: b2ContactImpulse):
        """
        WARNING: You cannot create/destroy Box2D entities inside this callback.
        This is called after a contact is updated.
        This allows you to inspect a contact before it goes to the solver.
        If you are careful, you can modify the contact manifold (e.g. disable contact).
        A copy of the old manifold is provided so that you can detect changes.
        Note: this is called only for awake bodies.
        Note: this is called even when the number of contact points is zero.
        Note: this is not called for sensors.
        Note: if you set the number of contact points to zero, you will not get an EndContact callback.
        However, you may get a BeginContact callback the next step.
        copied from https://box2d.org/documentation/classb2_contact_listener.html
        """
        pass

    def isKilled(self) -> bool:
        return self.__killed

    def kill(self):
        self.__killed = True
        self.__body.world.DestroyBody(self.__body)
