from Box2D import *
from game.Game import Game
from objects.base.ActiveObject import ActiveObject
from objects.friendly.Player import Player
from util.textures.AnimationPack import AnimationPack


class Enemy(ActiveObject):
    def __init__(self, game: Game, process, player: Player,
                 animation: AnimationPack, body: b2Body,
                 speed: float, jumpPower: float):
        # process: GameProcess
        ActiveObject.__init__(self, game, process, animation, body, speed, jumpPower)
        self.__player = player

    def preUpdate(self, delta: float):
        self.sense(self.__player, self.process.getObjects())
        self.act(self.think())

    def sense(self, player: Player, objects: set):
        pass

    def think(self) -> set:
        pass

    def act(self, actions: set):
        for action in actions:
            getattr(self, action)()
