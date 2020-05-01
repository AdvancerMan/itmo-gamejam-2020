import pygame as pg
from Box2D import *
from game.Game import Game
from objects.base.InGameObject import InGameObject
from util.textures.Textures import AnimationInfo


class Player(InGameObject):
    def __init__(self, game: Game, process):
        # process: GameProcess
        InGameObject.__init__(self, game, process,
                              game.getTextureManager().getAnimation(AnimationInfo.PLAYER_ANIMATION),
                              process.getFactory().createRectangleBody(self, b2_dynamicBody, 40, 100))

    def update(self):
        for e in self.process.getEvents():
            if e.type == pg.KEYDOWN:
                if e.key == pg.K_d:
                    self.goRight()
                elif e.key == pg.K_a:
                    self.goLeft()
                elif e.key == pg.K_w:
                    self.jump()
                elif e.key == pg.K_e:
                    self.shoot()

    def goLeft(self):
        pass

    def goRight(self):
        pass

    def jump(self):
        pass

    def shoot(self):
        pass
