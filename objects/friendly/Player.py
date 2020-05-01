import pygame as pg
from Box2D import *
from game.Game import Game
from objects.base.ActiveObject import ActiveObject
from util.textures.Textures import AnimationInfo


class Player(ActiveObject):
    def __init__(self, game: Game, process):
        # process: GameProcess
        ActiveObject.__init__(self, game, process,
                              game.getTextureManager().getAnimation(AnimationInfo.PLAYER_ANIMATION),
                              process.getFactory().createRectangleBody(self, b2_dynamicBody, 40, 100),
                              200, 100)
        self.__actions = set()

    def update(self):
        for e in self.process.getEvents():
            if e.type == pg.KEYDOWN or e.type == pg.KEYUP:
                act = self.__actions.add if e.type == pg.KEYDOWN else self.__actions.discard
                if e.key == pg.K_d:
                    act("goRight")
                elif e.key == pg.K_a:
                    act("goLeft")
                elif e.key == pg.K_w:
                    act("jump")
                elif e.key == pg.K_e:
                    act("shoot")
        for action in self.__actions:
            getattr(self, action)()
