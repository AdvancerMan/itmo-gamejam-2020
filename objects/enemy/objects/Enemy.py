import pyganim as pga
from Box2D import *
from game.Game import Game
from objects.base.ActiveObject import ActiveObject
from objects.friendly.Player import Player


class Enemy(ActiveObject):
    def __init__(self, game: Game, process, player: Player,
                 animation: pga.PygAnimation, body: b2Body,
                 speed: float, jumpPower: float):
        # process: GameProcess
        ActiveObject.__init__(self, game, process, animation, body, speed, jumpPower)
        self.player = player
