import pygame as pg
import pyganim as pga
from enum import auto, IntEnum


class AnimationName(IntEnum):
    RUN = auto()
    STAY = auto()
    FALL = auto()
    JUMP = auto()


class AnimationPack:
    def __init__(self, animations: dict):
        for name, anim in animations.items():
            assert isinstance(name, AnimationName)
            assert isinstance(anim, pga.PygAnimation)
        self.__animations = animations
        self.__animation = next(iter(animations.keys()))

    def setAnimation(self, name: AnimationName):
        self.__animation.stop()
        self.__animation = self.__animations[name]
        self.__animation.play()

    def blit(self, dst: pg.Surface, pos: tuple):
        self.__animation.blit(dst, pos)
