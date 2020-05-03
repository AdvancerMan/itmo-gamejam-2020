from Box2D import *
from game.Game import Game
from objects.main.InGameObject import InGameObject
from util.textures.AnimationPack import AnimationPack


class Platform(InGameObject):
    def __init__(self, game: Game, process, animation: AnimationPack, x: float, y: float, width: float, height: float):
        # process: GameProcess
        InGameObject.__init__(self, game, process, animation,
                              process.getFactory().createRectangleBody(b2_staticBody, width, height))
        self.setPosition(x, y)
