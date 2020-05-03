import pyganim as pga
from Box2D import *
from game.Game import Game
from objects.guns.Gun import Gun
from util.box2d.BodyFactory import createRectangleBodyTemplate
from util.textures.Textures import AnimationInfo, AnimationPackInfo


class UsualGun(Gun):
    def __init__(self, game: Game, process, owner):
        Gun.__init__(self, game, process,
                     game.getTextureManager().getAnimationPack(AnimationPackInfo.USUALGUN_BULLET_ANIMATION),
                     createRectangleBodyTemplate(b2_dynamicBody, 10, 10, gravityScale=0),
                     game.getTextureManager().getAnimationPack(AnimationPackInfo.USUALGUN_ANIMATION),
                     {"bulletSpeed": 80, "bulletType": "AllDirection", "bulletPower": 5}, owner)
        self.cooldown = 0.3


class BallisticGun(Gun):
    def __init__(self, game: Game, process, owner):
        Gun.__init__(self, game, process,
                     game.getTextureManager().getAnimationPack(AnimationPackInfo.BALLISTICGUN_BULLET_ANIMATION),
                     createRectangleBodyTemplate(b2_dynamicBody, 10, 10),
                     game.getTextureManager().getAnimationPack(AnimationPackInfo.BALLISTICGUN_ANIMATION),
                     {"bulletSpeed": 40, "bulletType": "Ballistic", "bulletPower": 20}, owner)
        self.cooldown = 0.7


class PoisonGun(Gun):
    def __init__(self, game: Game, process, owner):
        Gun.__init__(self, game, process,
                     game.getTextureManager().getAnimationPack(AnimationPackInfo.POISONGUN_BULLET_ANIMATION),
                     createRectangleBodyTemplate(b2_dynamicBody, 10, 10),
                     game.getTextureManager().getAnimationPack(AnimationPackInfo.POISONGUN_ANIMATION),
                     {"bulletSpeed": 40, "bulletType": "BallisticExplode", "bulletPower": 20}, owner)
        self.cooldown = 0.7

class PowerGun(Gun):
    def __init__(self, game: Game, process, owner):
        Gun.__init__(self, game, process,
                     game.getTextureManager().getAnimationPack(AnimationPackInfo.POWERGUN_BULLET_ANIMATION),
                     createRectangleBodyTemplate(b2_dynamicBody, 30, 30, gravityScale=0),
                     game.getTextureManager().getAnimationPack(AnimationPackInfo.POWERGUN_ANIMATION),
                     {"bulletSpeed": 80, "bulletType": "TwoDirection", "bulletPower": 5}, owner)
        self.cooldown = 1
