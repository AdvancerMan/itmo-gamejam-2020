import pyganim as pga
from Box2D import *
from game.Game import Game
from objects.base.InGameObject import InGameObject
from util.box2d.BodyFactory import BodyTemplate


class Bullet(InGameObject):
    def __init__(self, game, process, animation: pga.PygAnimation,
                 params: dict, owner, body: b2Body):
        InGameObject.__init__(self, game, process, animation, body)
        posX, posY = owner.getPosition()
        direction = owner.shootAngle
        if params["bulletType"] == "OneDirection":
            self.setPosition(posX + 100, posY)
            self.getBody().linearVelocity = params["bulletSpeed"] * direction
        if params["bulletType"] == "Ballistic":
            self.getBody().linearVelocity = params["bulletSpeed"] * direction
            self.setPosition(posX + 100, posY)


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
        self.__params = params      # params = {"bulletSpeed", "bulletType"}
                                    # maybe add "deviation" and "angle"
        self.__bulletAnimation = bulletAnim
        self.__gunAnimation = gunAnim
        self.__bulletBody = bulletBodyTemplate

    def spawnBullet(self, owner):
        self.__process.addObject(Bullet(self.__game, self.__process, self.__bulletAnimation,
                                        self.__params, owner,
                                        self.__bulletBody.createBody(self.__process.getFactory())))
