import pygame as pg
from game.Game import Game
from process.Process import Process
from objects.platforms.Platform import Platform
import json
from os.path import join


class Builder:
    def __init__(self, game: Game, process, name):
        # process: GameProcess
        self.__game = game
        self.__process = process
        self.__data = dict()
        self.putLevel(name)
        self.build()

    def putLevel(self,levelName):   # name without .json
        with open(join("levels", levelName + ".json")) as file:
            self.__data = json.load(file)

    def build(self):
        for plate in self.__data["platforms"]:
            self.__process.addObject(Platform(self.__game, self.__process, plate["posX"], plate["posY"]))

