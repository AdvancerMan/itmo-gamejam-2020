import pygame as pg
import pyganim as pga
from enum import auto, IntEnum


class AnimationName(IntEnum):
    RUN = auto()
    STAY = auto()
    JUMP = auto()
    FALL = auto()
    LANDING = auto()


class AnimationPack:
    def __init__(self, animations: dict):
        for name, anim in animations.items():
            assert isinstance(name, AnimationName)
            assert isinstance(anim, pga.PygAnimation)
        self.__animations = animations
        self.__animation = next(iter(animations.values()))
        self.__animation.play()
        self.__playingName = AnimationName.STAY

    def scale(self, size: tuple):
        for anim in self.__animations.values():
            anim.scale(size)

    def setAnimation(self, name: AnimationName):
        if self.__playingName != name:
            self.__animation.stop()
            self.__playingName = name
            self.__animation = self.__animations[name]
            self.__animation.play()

    def blit(self, dst: pg.Surface, pos: tuple):
        self.__animation.blit(dst, pos)

    def flip(self, xbool: bool, ybool: bool = False):
        for anim in self.__animations.values():
            anim.flip(xbool, ybool)

    def isFinished(self) -> bool:
        return self.__animation.isFinished()

    def getAnimationName(self) -> AnimationName:
        return self.__playingName
