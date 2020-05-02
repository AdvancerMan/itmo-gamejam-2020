import pygame as pg
from game.Game import Game
from process.Process import Process
from Box2D import *
from util.box2d.BodyFactory import BodyFactory
from objects.friendly.Player import Player
from levels.LevelBuilder import Builder


class GameProcess(Process):
    def __init__(self, game: Game):
        self.__world = b2World((0, -350))
        self.__factory = BodyFactory(self.__world)
        self.__game = game
        self.__justCreatedObjs = set()
        self.__objects = set()
        self.__player = Player(game, self)
        self.addObject(self.__player)
        self.__events = []
        self.__builder = Builder(game)
        self.__builder.build(self, "L1")

    def getFactory(self) -> BodyFactory:
        return self.__factory

    def addObject(self, obj):
        # obj: InGameObject
        self.__justCreatedObjs.add(obj)

    def processEvents(self, events: list):
        for e in events:
            if e.type == pg.QUIT:
                self.__game.stop()
        self.__events = events

    def getEvents(self) -> list:
        return self.__events

    def update(self, delta: float):
        self.__objects = self.__objects.union(self.__justCreatedObjs)
        self.__justCreatedObjs.clear()
        for obj in self.__objects:
            obj.update()
        self.__world.Step(delta, 10, 10)
        self.__events = []

    def draw(self, dst: pg.Surface):
        for obj in self.__objects:
            obj.draw(dst)
