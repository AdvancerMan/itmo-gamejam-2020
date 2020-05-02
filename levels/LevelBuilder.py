from game.Game import Game
import json
from os.path import join

from objects.platforms.SolidPlatform import SolidPlatform


def loadLevel(levelName: str):   # name without .json
    with open(join("levels", levelName + ".json")) as file:
        return json.load(file)


class Builder:
    def __init__(self, game: Game):
        # process: GameProcess
        self.__game = game

    def build(self, process, levelName: str):
        for plate in loadLevel(levelName)["platforms"]:
            process.addObject(SolidPlatform(self.__game, process, plate["x"], plate["y"], plate["width"], plate["height"]))
