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
                     {"bulletSpeed": 40, "bulletType": "BallisticExplode", "bulletPower": 20,
                      "ExplodeTime": 5.0, "ExplodeDamage": 0.2,
                      "ExplodeAnimation": game.getTextureManager().getAnimationPack(AnimationPackInfo.POISONEXPLODE_ANIMATION)},
                     owner)
        self.cooldown = 0.7


class PowerGun(Gun):
    def __init__(self, game: Game, process, owner):
        Gun.__init__(self, game, process,
                     game.getTextureManager().getAnimationPack(AnimationPackInfo.POWERGUN_BULLET_ANIMATION),
                     createRectangleBodyTemplate(b2_dynamicBody, 30, 30, gravityScale=0),
                     game.getTextureManager().getAnimationPack(AnimationPackInfo.POWERGUN_ANIMATION),
                     {"bulletSpeed": 80, "bulletType": "TwoDirectionExplode", "bulletPower": 30,
                      "ExplodeTime": 0.4, "ExplodeDamage": 2,
                      "ExplodeAnimation": game.getTextureManager().getAnimationPack(AnimationPackInfo.POWER_EXPLODE_BULLET_ANIMATION)},
                     owner)
        self.cooldown = 1


class GravityGun(Gun):
    def __init__(self, game: Game, process, owner):
        Gun.__init__(self, game, process,
                     game.getTextureManager().getAnimationPack(AnimationPackInfo.GRAVITYGUN_BULLET_ANIMATION),
                     createRectangleBodyTemplate(b2_dynamicBody, 1, 1, gravityScale=0),
                     game.getTextureManager().getAnimationPack(AnimationPackInfo.GRAVITYGUN_ANIMATION),
                     {"bulletSpeed": 80, "bulletType": "Gravity", "bulletPower": 0,
                      "ExplodeTime": 0.2, "ExplodeDamage": 0,
                      "ExplodeAnimation": game.getTextureManager().getAnimationPack(AnimationPackInfo.GRAVITY_EXPLODE_BULLET_ANIMATION)},
                     owner)
        self.cooldown = 0.5
