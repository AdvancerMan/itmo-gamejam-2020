import pyganim as pga
from Box2D import *
from game.Game import Game
from objects.guns.Gun import Gun
from util.box2d.BodyFactory import createRectangleBodyTemplate
from util.textures.Textures import AnimationInfo, AnimationPackInfo


class UsualGun(Gun):
    def __init__(self, game: Game, process):
        Gun.__init__(self, game, process,
                     game.getTextureManager().getAnimationPack(AnimationPackInfo.USUALGUN_BULLET_ANIMATION),
                     createRectangleBodyTemplate(b2_kinematicBody, 10, 10),
                     game.getTextureManager().getAnimationPack(AnimationPackInfo.USUALGUN_ANIMATION),
                     {"bulletSpeed": 200})
