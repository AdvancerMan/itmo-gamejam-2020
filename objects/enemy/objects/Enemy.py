from Box2D import *
from game.Game import Game
from objects.main.ActiveObject import ActiveObject
from objects.friendly.Player import Player
from util.textures.AnimationPack import AnimationPack


class Enemy(ActiveObject):
    def __init__(self, game: Game, process, player: Player,
                 animation: AnimationPack, body: b2Body,
                 speed: float, jumpPower: float, guns: list):
        # process: GameProcess
        ActiveObject.__init__(self, game, process, animation, body, speed, jumpPower, guns)
        self.__player = player
        self._playerToRight = False

    def preUpdate(self, delta: float):
        super().preUpdate(delta)
        self.sense(self.__player, self.process.getObjects())
        self.act(self.think())

    def sense(self, player: Player, objects: set):
        self._playerToRight = player.getPosition()[0] >= self.getPosition()[0]

    def think(self) -> set:
        return set()

    def act(self, actions: set):
        for action in actions:
            getattr(self, action)()
