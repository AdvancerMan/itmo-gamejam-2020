import pygame as pg
from Box2D import *
from game.Game import Game
from objects.base.InGameObject import InGameObject
from util.textures.Textures import AnimationInfo


class Platform(InGameObject):
    def __init__(self, game: Game, process, posX: int, posY: int):
        # process: GameProcess
        InGameObject.__init__(self, game, process,
                              game.getTextureManager().getAnimation(AnimationInfo.PLATFORM_ANIMATION),
                              process.getFactory().createRectangleBody(b2_staticBody, 100, 10))
        self.setPosition(posX, posY, 0)
