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
    def __init__(self, game, process, animation, body: b2Body, pos: tuple):
        InGameObject.__init__(self, game, process, animation, body)
        self.setPosition(pos[0], pos[1])

    def preSolve(self, obj, contact: b2Contact, oldManifold: b2Manifold):
        contact.enabled = False
        obj.takeDamage(0.1)

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
        if self.__params["bulletType"] == "TwoDirection":
            direction = b2Vec2(direction.x, 0)
        direction.Normalize()
        posY -= self.getAABB().h / 2
        self.setPosition(posX + (30 * direction).x, posY + (30 * direction).y)
        self.getBody().linearVelocity = params["bulletSpeed"] * direction + self.__owner.getBody().linearVelocity

    def preSolve(self, obj, contact: b2Contact, oldManifold: b2Manifold):
        if self.__params["bulletType"] != "BallisticExplode":
            contact.enabled = False

    def beginContact(self, obj, contact: b2Contact):
        if obj == self.__owner and not self.__hitOwner or type(obj) == Explode or type(obj) == Bullet:
            pass
        else:
            obj.takeDamage(self.__params["bulletPower"])
            if self.__params["bulletType"] == "BallisticExplode":
                self.__dead = True
            else:
                self.process.removeObject(self)

    def endContact(self, obj, contact: b2Contact):
        if obj == self.__owner:
            self.__hitOwner = True

    def postUpdate(self):
        if self.__dead:
            self.__process.addObject(Explode(self.__game, self.__process,
                                             self.__game.getTextureManager().getAnimationPack(
                                                 AnimationPackInfo.POISONEXPLODE_ANIMATION),
                                             self.__process.getFactory().createRectangleBody(b2_dynamicBody, 50, 50, gravityScale=0),
                                             self.getPosition()))
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

    def spawnBullet(self):
        self.__gunAnimation.setAnimation(AnimationName.SHOOT, True)

    def __spawnBullet(self):
        self.__process.addObject(Bullet(self.__game, self.__process, self.__bulletAnimation,
                                        self.__params, self.__owner,
                                        self.__bulletBody.createBody(self.__process.getFactory())))

    def postUpdate(self):
        if self.__gunAnimation.isFinished():
            self.__spawnBullet()
            self.__gunAnimation.setAnimation(AnimationName.STAY)

    def draw(self, dst: pg.Surface, pos):
        self.__gunAnimation.scale((70, 30))
        posOld = self.__gunAnimation.getSize()
        angle = getAngle(self.__owner.shootAngle)
        if self.__params["bulletType"] == "TwoDirection":
            angle = (0, angle[1])
        self.__gunAnimation.rotozoom(angle[0], 1)
        self.__gunAnimation.flip(not angle[1])
        posNew = self.__gunAnimation.getSize()
        posX = -(posNew[0] - posOld[0] * ((angle[1] - 1/2)*2 * cos(angle[0] / 180 * pi))) / 2
        if angle[0] > 0:
            posY = -posNew[1] + posOld[1] * cos(angle[0] / 180 * pi) / 2
        else:
            posY = -posOld[1] * cos(angle[0] / 180 * pi) / 2
        ownerSize = self.__owner.getAABB()
        self.__gunAnimation.blit(dst, (pos[0] + posX + ownerSize.w / 2, pos[1] + posY + ownerSize.h / 2))
        self.__gunAnimation.clearTransforms()
