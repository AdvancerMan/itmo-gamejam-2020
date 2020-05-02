import pyganim as pga
from Box2D import *
from game.Game import Game
from objects.base.InGameObject import InGameObject
from util.box2d.BodyFactory import BodyTemplate


class Bullet(InGameObject):
    def __init__(self, game, process, animation: pga.PygAnimation,
                 params: dict, owner, body: b2Body):
        InGameObject.__init__(self, game, process, animation, body)
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
    """
    :NOTE:
    Gun shouldn't have body, body is a physical object
    which is used to compute collisions.
    Gun shouldn't collide with any objects.
    (Probably that strange object on (0, 0) was gun body)

    If you create body and reuse it in Bullet
    you would get many objects on the same body
    so you should use something like body template

    Variables should be named in camelCase or i_dont_know_name_of_this_case
    """

    def __init__(self, game: Game, process, bulletAnim: pga.PygAnimation,
                 bulletBodyTemplate: BodyTemplate,
                 gunAnim: pga.PygAnimation, params: dict, owner):
        # process: GameProcess
        self.__owner = owner
        self.__game = game
        self.__process = process
        self.__params = params      # params = {"bulletSpeed", "bulletType", "bulletPower"}
                                    # maybe add "deviation" and "angle"
        self.__bulletAnimation = bulletAnim
        self.__gunAnimation = gunAnim
        self.__bulletBody = bulletBodyTemplate

    def spawnBullet(self, owner):
        self.__process.addObject(Bullet(self.__game, self.__process, self.__bulletAnimation,
                                        self.__params, owner,
                                        self.__bulletBody.createBody(self.__process.getFactory())))
