import pygame as pg
from game.Game import Game
from process.Process import Process
from process.GameProcess import GameProcess


class MenuProcess(Process):
    def __init__(self, game: Game):
        self.__game = game

    def processEvents(self, events: list):
        for e in events:
            if e.type == pg.QUIT:
                self.__game.stop()
            if e.type == pg.KEYDOWN:
                self.__game.addProcess(GameProcess(self.__game))
