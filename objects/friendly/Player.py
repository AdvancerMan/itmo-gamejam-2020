import pygame as pg
from Box2D import *
from game.Game import Game
from objects.base.ActiveObject import ActiveObject
from util.textures.Textures import AnimationPackInfo
from objects.guns.PlayerGuns import *
from config.Config import *


class Player(ActiveObject):
    def __init__(self, game: Game, process):
        # process: GameProcess
        ActiveObject.__init__(self, game, process,
                              game.getTextureManager().getAnimationPack(AnimationPackInfo.PLAYER_ANIMATION),
                              process.getFactory().createRectangleBody(b2_dynamicBody, 40, 100),
                              20, 40, [UsualGun(game, process, self), BallisticGun(game, process, self)])
        self.__actions = set()
        self.hp = PLAYER_HP
        self.maxHp = PLAYER_HP

    def angleUpdate(self):
        self.shootAngle = 0
        posMX, posMY = pg.mouse.get_pos()
        self.shootAngle = b2Vec2(posMX - WINDOW_RESOLUTION[0] / 2, WINDOW_RESOLUTION[1] / 2 - posMY)

    def preUpdate(self, delta: float):
        super().preUpdate(delta)
        for e in self.process.getEvents():
            act = self.__actions.add if e.type in (pg.KEYDOWN, pg.MOUSEBUTTONDOWN) else self.__actions.discard
            if e.type in (pg.KEYDOWN, pg.KEYUP):
                if e.key == pg.K_d:
                    act("goRight")
                elif e.key == pg.K_a:
                    act("goLeft")
                elif e.key == pg.K_w:
                    act("jump")
                elif e.key == pg.K_r:
                    act("shoot")
            elif e.type in (pg.MOUSEBUTTONDOWN, pg.MOUSEBUTTONUP):
                if e.button == pg.BUTTON_LEFT:
                    act("shoot")

            if e.type == pg.KEYDOWN:
                if e.key == pg.K_e:
                    self.changeGunRight()
                elif e.key == pg.K_q:
                    self.changeGunLeft()
        for action in self.__actions:
            getattr(self, action)()
