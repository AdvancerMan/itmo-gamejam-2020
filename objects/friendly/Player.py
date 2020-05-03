import pygame as pg
from Box2D import *
from game.Game import Game
from gui.GunsList import GunsList
from objects.main.ActiveObject import ActiveObject
from util.Rectangle import Rectangle
from util.textures.Textures import AnimationPackInfo
from objects.guns.PlayerGuns import *
from config.Config import *


class Player(ActiveObject):
    def __init__(self, game: Game, process, guiGuns: GunsList):
        # process: GameProcess
        ActiveObject.__init__(self, game, process,
                              game.getTextureManager().getAnimationPack(AnimationPackInfo.PLAYER_ANIMATION),
                              process.getFactory().createRectangleBody(b2_dynamicBody, 40, 100),
                              20, 40, [PoisonGun(game, process, self), PowerGun(game, process, self), BallisticGun(game, process, self)])
        self.__actions = set()
        self.resetHp(PLAYER_HP)
        self.__guiGuns = guiGuns

    def angleUpdate(self):
        self.shootAngle = 0
        posMX, posMY = pg.mouse.get_pos()
        self.shootAngle = b2Vec2(posMX - WINDOW_RESOLUTION[0] / 2, WINDOW_RESOLUTION[1] / 2 - posMY)
        self.setDirection(self.shootAngle.x > 0)

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

    def draw(self, dst: pg.Surface, cameraRect: Rectangle):
        super().draw(dst, cameraRect)
        self.__guiGuns.draw(dst, 0) # TODO ammoRemaining

    def changeGunLeft(self):
        super().changeGunLeft()
        self.__guiGuns.switchLeft()

    def changeGunRight(self):
        super().changeGunRight()
        self.__guiGuns.switchRight()

    def goLeft(self):
        self.go(-self.getSpeed())

    def goRight(self):
        self.go(self.getSpeed())
