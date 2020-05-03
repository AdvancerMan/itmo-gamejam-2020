import pygame as pg
from game.Game import Game
from process.Process import Process
from process.GameProcess import GameProcess
from os.path import join


def _createPath(*picPath: str) -> str:
    return join(*picPath)


class MenuProcess(Process):
    def __init__(self, game: Game):
        self.__game = game
        pg.mixer.init()
        pg.mixer.music.load(_createPath('music', 'main_menu.mp3'))
        pg.mixer.music.play()

    def processEvents(self, events: list):
        for e in events:
            if e.type == pg.QUIT:
                pg.mixer.music.stop()
                self.__game.stop()
            if e.type == pg.KEYDOWN:
                pg.mixer.music.stop()
                self.__game.addProcess(GameProcess(self.__game))
