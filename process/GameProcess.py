import pygame as pg

from config.Config import WINDOW_RESOLUTION, BASE_START_POS
from game.Game import Game
from gui.GunsList import GunsList
from objects.base.Base import Base
from objects.main.InGameObject import InGameObject
from objects.platforms.Platform import Platform
from process.Process import Process
from Box2D import *

from util.Rectangle import rectFromSize
from util.box2d.BodyFactory import BodyFactory
from objects.friendly.Player import Player
from levels.LevelBuilder import Builder
from util.box2d.ContactListener import ContactListener
from util.textures.Textures import TextureInfo
from os.path import join


def _createPath(*picPath: str) -> str:
    return join(*picPath)


class GameProcess(Process):
    SAFE_RADIUS2 = 3000 * 3000

    def __init__(self, game: Game):
        self.__world = b2World((0, -100))
        self.__contactListener = ContactListener()
        self.__world.contactListener = self.__contactListener
        self.__factory = BodyFactory(self.__world)
        self.__background = pg.transform.scale(
            game.getTextureManager()
                .getTexture(TextureInfo.BACKGROUND),
            WINDOW_RESOLUTION
        )

        self.__game = game
        self.__events = []
        self.__justCreatedObjects = set()
        self.__removedObjects = set()
        self.__objects = set()
        self.__cameraRect = rectFromSize(0, -WINDOW_RESOLUTION[1], *WINDOW_RESOLUTION)

        self.__player = Player(game, self, GunsList(game, (20, 20)))
        self.addObject(self.__player)
        self.__base = Base(game, self, *BASE_START_POS, self.__player)

        self.__builder = Builder(game)
        self.__builder.build(self, self.__player, self.__base, "L1")

        pg.mixer.music.load(_createPath('music', 'fight.mp3'))
        pg.mixer.music.play()

    def centerCameraAt(self, x: float, y: float):
        self.__cameraRect.centerAt(x, y)

    def centerCameraAtObj(self, obj: InGameObject):
        self.centerCameraAt(*obj.getPosition())

    def getFactory(self) -> BodyFactory:
        return self.__factory

    def getObjects(self) -> set:
        return self.__objects

    def addObject(self, obj):
        # obj: InGameObject
        self.__justCreatedObjects.add(obj)

    def removeObject(self, obj):
        self.__removedObjects.add(obj)

    def processEvents(self, events: list):
        for e in events:
            if e.type == pg.QUIT:
                self.__game.stop()
        self.__events = events

    def getEvents(self) -> list:
        return self.__events

    def update(self, delta: float):
        if self.__player.isKilled():
            self.__game.replaceProcess(GameProcess(self.__game))
        self.__base.preUpdate(delta)
        for obj in self.__objects:
            obj.preUpdate(delta)

        self.__objects = self.__objects.union(self.__justCreatedObjects)
        self.__justCreatedObjects.clear()
        self.__world.Step(delta, 10, 10)

        self.__base.postUpdate()
        for obj in self.__objects:
            obj.postUpdate()
            self.checkRadius(obj)

        self.__events = []
        self.centerCameraAtObj(self.__player)

    def checkRadius(self, obj):
        if b2Vec2(*obj.getPosition()).lengthSquared >= GameProcess.SAFE_RADIUS2:
            if obj == self.__player:
                obj.setPosition(0, 0)
            else:
                self.removeObject(obj)

    def draw(self, dst: pg.Surface):
        backgroundW = self.__background.get_size()[0]
        backgroundX = self.__cameraRect.x // 10 // backgroundW * backgroundW - self.__cameraRect.x // 10
        if backgroundX < 0:
            backgroundX += backgroundW

        dst.blit(self.__background, (backgroundX, 0))
        dst.blit(self.__background, (backgroundX - backgroundW, 0))

        self.__base.draw(dst, self.__cameraRect)
        for obj in self.__objects:
            obj.draw(dst, self.__cameraRect)
        for obj in self.__objects:
            obj.postDraw(dst, self.__cameraRect)
        self.__removeObjects()

    def __removeObjects(self):
        self.__objects.symmetric_difference_update(self.__removedObjects)
        for object in self.__removedObjects:
            object.kill()
        self.__removedObjects.clear()
