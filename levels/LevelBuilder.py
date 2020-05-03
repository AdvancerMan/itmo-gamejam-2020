from game.Game import Game
import json
from os.path import join

from objects.enemy.objects.Ant import Ant
from objects.enemy.objects.Enemy import Enemy
from objects.enemy.objects.StupidEnemy import StupidEnemy, StupidEnemyStaying, StupidEnemyRunningTo, \
    StupidEnemyRunningFrom
from objects.enemy.spawners.Anthill import Anthill
from objects.enemy.spawners.Spawner import Spawner
from objects.friendly.Player import Player
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
            "halfCol": HalfCollidedPlatform,
            "stupidStaying": StupidEnemyStaying,
            "stupidRunningTo": StupidEnemyRunningTo,
            "stupidRunningFrom": StupidEnemyRunningFrom,
            "ant": Ant,
            "anthill": Anthill
        }

    def build(self, process, player: Player, levelName: str):
        for class_name, objs in loadLevel(levelName).items():
            Constructor = self.__objects[class_name]
            for args in objs:
                if isinstance(args, dict):
                    if issubclass(Constructor, (Enemy, Spawner)):
                        args["player"] = player
                    process.addObject(Constructor(self.__game, process, **args))
                else:
                    if issubclass(Constructor, (Enemy, Spawner)):
                        process.addObject(Constructor(self.__game, process, player, *args))
                    else:
                        process.addObject(Constructor(self.__game, process, *args))
