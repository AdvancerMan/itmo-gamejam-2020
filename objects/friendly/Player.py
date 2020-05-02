import pygame as pg
from Box2D import *
from game.Game import Game
from objects.base.ActiveObject import ActiveObject
from util.textures.Textures import AnimationPackInfo
from objects.guns.PlayerGuns import *


class Player(ActiveObject):
    def __init__(self, game: Game, process):
        # process: GameProcess
        ActiveObject.__init__(self, game, process,
                              game.getTextureManager().getAnimationPack(AnimationPackInfo.PLAYER_ANIMATION),
                              process.getFactory().createRectangleBody(b2_dynamicBody, 40, 100),
                              200, 400, [UsualGun(game, process, self), BallisticGun(game, process, self)])
        self.__actions = set()

    def preUpdate(self, delta: float):
        super().preUpdate(delta)
        for e in self.process.getEvents():
            if e.type == pg.KEYDOWN or e.type == pg.KEYUP:
                act = self.__actions.add if e.type == pg.KEYDOWN else self.__actions.discard
                if e.key == pg.K_d:
                    act("goRight")
                elif e.key == pg.K_a:
                    act("goLeft")
                elif e.key == pg.K_w:
                    act("jump")
                elif e.key == pg.K_r:
                    act("shoot")
            if e.type == pg.KEYDOWN:
                if e.key == pg.K_e:
                    self.changeGunRight()
                elif e.key == pg.K_q:
                    self.changeGunLeft()
        for action in self.__actions:
            getattr(self, action)()
