import pygame as pg
from game.Game import Game
from process.MenuProcess import MenuProcess

pg.init()
game = Game()
game.run(MenuProcess(game))
pg.quit()
