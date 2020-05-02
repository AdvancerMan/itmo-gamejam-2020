from game.Game import Game
from objects.platforms.Platform import Platform
import json
from os.path import join


def loadLevel(levelName: str):   # name without .json
    with open(join("levels", levelName + ".json")) as file:
        return json.load(file)


class Builder:
    def __init__(self, game: Game):
        # process: GameProcess
        self.__game = game

    def build(self, process, levelName: str):
        for plate in loadLevel(levelName)["platforms"]:
            process.addObject(Platform(self.__game, process, plate["posX"], plate["posY"]))
