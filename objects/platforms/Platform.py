import pygame as pg
from Box2D import *
from game.Game import Game
from objects.base.InGameObject import InGameObject
from util.textures.Textures import AnimationPackInfo


class Platform(InGameObject):
    def __init__(self, game: Game, process, x: float, y: float, width: float, height: float):
        # process: GameProcess
        InGameObject.__init__(self, game, process,
                              game.getTextureManager().getAnimationPack(AnimationPackInfo.PLATFORM_ANIMATION),
                              process.getFactory().createRectangleBody(b2_staticBody, width, height))
        self.setPosition(x, y)
