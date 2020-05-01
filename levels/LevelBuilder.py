import pygame as pg
from game.Game import Game
from process.Process import Process
from objects.platforms.Platform import Platform
import json
from os.path import join


class Level:
    def __init__(self, game: Game, process):
        # process: GameProcess
        self.__game = game
        self.__process = process
        self.__data = dict()

    def putLevel(self, name):   # name without .json
        with open(join("levels", name + ".json")) as file:
            self.__data = json.load(file)

    def build(self):
        for plate in self.__data["platforms"]:
            self.__process.addObject(Platform(self.__game, self.__process, plate["posX"], plate["posY"]))


class Builder:
    def __init__(self, game: Game, process, name):
        self.__level = Level(game, process)
        self.__level.putLevel(name)
        self.__level.build()
