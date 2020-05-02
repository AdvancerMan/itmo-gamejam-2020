from Box2D import *
from game.Game import Game
from objects.base.InGameObject import InGameObject
from objects.enemy.objects.StupidEnemy import StupidEnemy
from objects.friendly.Player import Player
from util.box2d.BodyFactory import createRectangleBodyTemplate
from util.textures.AnimationPack import AnimationPack
from util.textures.Textures import AnimationPackInfo


class Spawner(InGameObject):
    SPAWNER_INFO = {
        StupidEnemy: (AnimationPackInfo.STUPID_ENEMY_ANIMATION, createRectangleBodyTemplate(b2_dynamicBody, 40, 100))
    }

    def __init__(self, game: Game, process, player: Player,
                 animation: AnimationPack, body: b2Body, MobConstructor, **kwargs):
        # process: GameProcess
        InGameObject.__init__(self, game, process, animation, body)
        self.__kwargs = kwargs.update({"game": game, "process": process, "player": player})
        self.__Constructor = MobConstructor

    def spawn(self):
        self.__Constructor(animation=Spawner.SPAWNER_INFO[self.__Constructor][0],
                           body=Spawner.SPAWNER_INFO[self.__Constructor][1],
                           **self.__kwargs)
