import pyganim as pga
import pygame as pg
from Box2D import *
from game.Game import Game
from objects.main.InGameObject import InGameObject
from util.box2d.BodyFactory import BodyTemplate
from config.Config import *
from math import *


def getAngle(vector: b2Vec2):  # in degrees (-90; 90), direction 1 or 0
    if vector.length == 0:
        return (1, True)
    vector.Normalize()
    phi1 = acos(vector.x)
    phi1 *= 360 / (2 * pi)
    phi2 = asin(vector.y)
    phi2 *= 360 / (2 * pi)
    if phi1 > 90:
        return (phi2, False)
    else:
        return (phi2, True)


def biggerNull(x: float):
    if x > 0:
        return 1
    else:
        return 0

class Bullet(InGameObject):
    def __init__(self, game, process, animation: pga.PygAnimation,
                 params: dict, owner, body: b2Body):
        InGameObject.__init__(self, game, process, animation, body)
        self.getBody().bullet = True
        self.__params = params
        self.__owner = owner
        self.__hitOwner = False
        posX, posY = self.__owner.getPosition()
        direction = self.__owner.shootAngle
        direction.Normalize()
        if self.__params["bulletType"] == "OneDirection" or self.__params["bulletType"] == "Ballistic":
            self.setPosition(posX + (50 * direction).x, posY + (50 * direction).y)
            self.getBody().linearVelocity = params["bulletSpeed"] * direction + self.__owner.getBody().linearVelocity

    def preSolve(self, obj, contact: b2Contact, oldManifold: b2Manifold):
        contact.enabled = False

    def beginContact(self, obj, contact: b2Contact):
        if obj == self.__owner and not self.__hitOwner:
            pass
        else:
            obj.takeDamage(self.__params["bulletPower"])
            self.process.removeObject(self)

    def endContact(self, obj, contact: b2Contact):
        if obj == self.__owner:
            self.__hitOwner = True

class Gun:
    def __init__(self, game: Game, process, bulletAnim: pga.PygAnimation,
                 bulletBodyTemplate: BodyTemplate,
                 gunAnim, params: dict, owner):
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
        # self.__gunAnimation.scale((50, 15))

    def spawnBullet(self, owner):
        self.__process.addObject(Bullet(self.__game, self.__process, self.__bulletAnimation,
                                        self.__params, owner,
                                        self.__bulletBody.createBody(self.__process.getFactory())))

    def draw(self, dst: pg.Surface, pos):
        self.__gunAnimation.scale((70, 30))
        posOld = self.__gunAnimation.getSize()
        angle = getAngle(self.__owner.shootAngle)
        self.__gunAnimation.rotozoom(angle[0], 1)
        self.__gunAnimation.flip(not angle[1], 0)
        posNew = self.__gunAnimation.getSize()
        posX = -(posNew[0] - posOld[0] * ((angle[1] - 1/2)*2 * cos(angle[0] / 180 * pi))) / 2
        if biggerNull(angle[0]):
            posY = -posNew[1] + posOld[1] * cos(angle[0] / 180 * pi) / 2
        else:
            posY = -posOld[1] * cos(angle[0] / 180 * pi) / 2
        ownerSize = self.__owner.getAABB()
        # print(ownerSize.h)
        self.__gunAnimation.blit(dst, (pos[0] + posX + ownerSize.w / 2, pos[1] + posY + ownerSize.h / 2))
        self.__gunAnimation.clearTransforms()
