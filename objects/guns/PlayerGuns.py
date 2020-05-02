import pyganim as pga
from Box2D import *
from game.Game import Game
from objects.guns.Gun import Gun
from util.textures.Textures import AnimationInfo, AnimationPackInfo


class UsualGun(Gun):
    def __init__(self, game: Game, process):
        Gun.__init__(self, game, process,
                     game.getTextureManager().getAnimationPack(AnimationPackInfo.USUALGUN_BULLET_ANIMATION),
                     process.getFactory().createRectangleBodyTemplate(b2_kinematicBody, 10, 10),
                     game.getTextureManager().getAnimationPack(AnimationPackInfo.USUALGUN_ANIMATION),
                     {"bulletSpeed": 800, "bulletType": "OneDirection"})


class BallisticGun(Gun):
    def __init__(self, game: Game, process):
        Gun.__init__(self, game, process,
                     game.getTextureManager().getAnimationPack(AnimationPackInfo.BALLISTICGUN_BULLET_ANIMATION),
                     process.getFactory().createRectangleBodyTemplate(b2_dynamicBody, 10, 10),
                     game.getTextureManager().getAnimationPack(AnimationPackInfo.BALLISTICGUN_ANIMATION),
                     {"bulletSpeed": 800, "bulletType": "Ballistic"})