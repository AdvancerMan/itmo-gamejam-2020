from game.Game import Game
import json
from os.path import join

from objects.platforms.HalfCollidedPlatform import HalfCollidedPlatform
from objects.platforms.SolidPlatform import SolidPlatform


def loadLevel(levelName: str):   # name without .json
    with open(join("levels", levelName + ".json")) as file:
        return json.load(file)


class Builder:
    def __init__(self, game: Game):
        # process: GameProcess
        self.__game = game
        self.__objects = {
            "solid": SolidPlatform,
            "halfCol": HalfCollidedPlatform
        }

    def build(self, process, levelName: str):
        for class_name, objs in loadLevel(levelName).items():
            Constructor = self.__objects[class_name]
            for kwargs in objs:
                process.addObject(Constructor(self.__game, process, **kwargs))
