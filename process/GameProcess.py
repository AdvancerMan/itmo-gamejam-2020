import pygame as pg
from game.Game import Game
from process.Process import Process
from Box2D import *
from util.box2d.BodyFactory import BodyFactory
from objects.friendly.Player import Player


class GameProcess(Process):
    def __init__(self, game: Game):
        self.__world = b2World()
        self.__factory = BodyFactory(self.__world)
        self.__game = game
        self.__objects = set()
        self.__player = Player(game, self)
        self.addObject(self.__player)
        self.__events = []

    def getFactory(self) -> BodyFactory:
        return self.__factory

    def addObject(self, obj):
        # obj: InGameObject
        self.__objects.add(obj)

    def processEvents(self, events: list):
        for e in events:
            if e.type == pg.QUIT:
                self.__game.stop()
        self.__events = events

    def getEvents(self) -> list:
        return self.__events

    def update(self, delta: float):
        for obj in self.__objects:
            obj.update()
        self.__world.Step(delta, 10, 10)
        self.__events = []

    def draw(self, dst: pg.Surface):
        for obj in self.__objects:
            obj.draw(dst)
