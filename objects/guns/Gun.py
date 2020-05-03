import pyganim as pga
import pygame as pg
from Box2D import *
from game.Game import Game
from objects.main.InGameObject import InGameObject
from util.box2d.BodyFactory import BodyTemplate
from config.Config import *
from math import *
from util.textures.Textures import AnimationPackInfo, AnimationPack, AnimationName


def getAngle(vector: b2Vec2):  # in degrees (-90; 90), direction 1 or 0
    if vector.length == 0:
        return 1, True
    vector.Normalize()
    phi1 = acos(vector.x)
    phi1 *= 360 / (2 * pi)
    phi2 = asin(vector.y)
    phi2 *= 360 / (2 * pi)
    if phi1 > 90:
        return phi2, False
    else:
        return phi2, True


def biggerNull(x: float):
    if x > 0:
        return 1
    else:
        return 0


class Explode(InGameObject):
    def __init__(self, game, process, animation, body: b2Body, pos: tuple, params: dict):
        InGameObject.__init__(self, game, process, animation, body)
        self.setTransform(pos[0], pos[1])
        self.__process = process
        self.__game = game
        self.__params = params
        self.__life = 0
        self.__body = body

    def preSolve(self, obj, contact: b2Contact, oldManifold: b2Manifold):
        contact.enabled = False
        obj.takeDamage(self.__params["ExplodeDamage"], True)
        if self.__params["bulletType"] == "Gravity":
            posObjX, posObjY = obj.getPosition()
            posOwnX, posOwnY = self.getPosition()
            impulse = b2Vec2(posObjX - posOwnX, 0)
            impulse.Normalize()
            impulse.y = 0.2
            impulse *= 40
            point = b2Vec2(0, 0)
            obj.getBody().ApplyLinearImpulse(impulse, point, False)

    def preUpdate(self, delta: float):
        self.__life += delta

    def postUpdate(self):
        if self.__params["ExplodeTime"] < self.__life:
            self.process.removeObject(self)

    def isLand(self) -> bool:
        return False


class Bullet(InGameObject):
    def __init__(self, game, process, animation,
                 params: dict, owner, body: b2Body):
        InGameObject.__init__(self, game, process, animation, body)
        self.getBody().bullet = True
        self.__process = process
        self.__game = game
        self.__params = params
        self.__owner = owner
        self.__hitOwner = False
        self.__dead = False
        posX, posY = self.__owner.getPosition()
        direction = self.__owner.shootAngle
        if self.__params["bulletType"] == "TwoDirectionExplode":
            direction = b2Vec2(direction.x, 0)
        direction.Normalize()
        posY -= self.getAABB().h / 2
        posX -= 3
        self.setPosition(posX + (30 * direction).x, posY + (30 * direction).y)
        self.getBody().linearVelocity = params["bulletSpeed"] * direction + self.__owner.getBody().linearVelocity

    def preSolve(self, obj, contact: b2Contact, oldManifold: b2Manifold):
        contact.enabled = False

    def beginContact(self, obj, contact: b2Contact):
        if obj == self.__owner and not self.__hitOwner or type(obj) == Explode or type(obj) == Bullet:
            pass
        else:
            obj.takeDamage(self.__params["bulletPower"])
            if self.__params["bulletType"] == "BallisticExplode" or \
                    self.__params["bulletType"] == "TwoDirectionExplode" or \
                    self.__params["bulletType"] == "Gravity":
                self.__dead = True
            else:
                self.process.removeObject(self)

    def endContact(self, obj, contact: b2Contact):
        if obj == self.__owner:
            self.__hitOwner = True

    def postUpdate(self):
        if self.__dead:
            self.__process.addObject(Explode(self.__game, self.__process,
                                             self.__params["ExplodeAnimation"],
                                             self.__process.getFactory().createRectangleBody(b2_staticBody, 150, 150, gravityScale=0),
                                             self.getPosition(), self.__params))
            self.process.removeObject(self)


class Gun:
    def __init__(self, game: Game, process, bulletAnim: AnimationPack,
                 bulletBodyTemplate: BodyTemplate,
                 gunAnim: AnimationPack, params: dict, owner):
        # process: GameProcess
        self.__owner = owner
        self.__game = game
        self.__process = process
        self.__params = params      # params = {"bulletSpeed", "bulletType", "bulletPower"}
                                    # maybe add "deviation" and "angle"
        self.__bulletAnimation = bulletAnim
        self.__gunAnimation = gunAnim
        self.__bulletBody = bulletBodyTemplate
        self.__currAngle = 0
        self.__directedToRight = True

    def spawnBullet(self):
        if not self.__gunAnimation.setAnimation(AnimationName.SHOOT, True):
            self.__spawnBullet()

    def __spawnBullet(self):
        animation = self.__bulletAnimation.getCopy()
        if not self.__directedToRight:
            animation.flip(True)
        bullet = Bullet(self.__game, self.__process, animation,
                        self.__params, self.__owner,
                        self.__bulletBody.createBody(self.__process.getFactory()))
        self.__process.addObject(bullet)

    def postUpdate(self):
        if self.__gunAnimation.isFinished():
            self.__spawnBullet()
            self.__gunAnimation.setAnimation(AnimationName.STAY)

    def draw(self, dst: pg.Surface, pos: tuple):
        self.__gunAnimation.scale((70, 30))
        oldW, oldH = self.__gunAnimation.getSize()
        angle, self.__directedToRight = getAngle(self.__owner.shootAngle)
        if self.__params["bulletType"] == "TwoDirectionExplode":
            angle = 0
        self.__gunAnimation.rotate(angle)
        self.__gunAnimation.flip(not self.__directedToRight)

        newW, newH = self.__gunAnimation.getSize()
        x = (newW - oldW * (1 if self.__directedToRight else -1) * cos(angle / 180 * pi)) / 2
        y = oldH * cos(angle / 180 * pi) / 2
        y = newH - y if angle > 0 else y

        ownerW, ownerH = self.__owner.getAABB().size()
        x += 11 - ownerW if self.__directedToRight else -11
        y += 8

        self.__gunAnimation.blit(dst, (pos[0] - x, pos[1] - y + ownerH / 2))
        self.__gunAnimation.clearTransforms()
