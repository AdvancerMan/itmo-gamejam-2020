import pyganim as pga
from Box2D import *
from game.Game import Game
from objects.base.InGameObject import InGameObject
from objects.guns.Gun import Gun
from util.textures.Textures import AnimationInfo


class UsualGun(Gun):
    def __init__(self, game: Game, process):
        Gun.__init__(self, game, process,
                     game.getTextureManager().getAnimation(AnimationInfo.USUALGUN_BULLET_ANIMATION),
                     process.getFactory().createRectangleBody(self, b2_staticBody, 100, 10),
                     game.getTextureManager().getAnimation(AnimationInfo.USUALGUN_ANIMATION),
                     process.getFactory().createRectangleBody(self, b2_staticBody, 100, 10),
                     {"bulletSpeed": 10})
