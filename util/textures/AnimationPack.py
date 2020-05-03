import pygame as pg
import pyganim as pga
from enum import auto, IntEnum


class AnimationName(IntEnum):
    RUN = auto()
    STAY = auto()
    JUMP = auto()
    FALL = auto()
    LANDING = auto()


def breakAnimationLoops(animations: dict):
    for name in (AnimationName.JUMP, AnimationName.LANDING):
        if name in animations:
            animations[name].loop = False


class AnimationPack:
    def __init__(self, animations: dict):
        for name, anim in animations.items():
            assert isinstance(name, AnimationName)
            assert isinstance(anim, pga.PygAnimation)
        breakAnimationLoops(animations)
        self.__animations = animations
        self.__playingName = AnimationName.STAY
        self.__animation = animations[self.__playingName]
        self.__animation.play()

    def scale(self, size: tuple):
        for anim in self.__animations.values():
            anim.scale(size)

    def rotate(self, angle: float):
        for anim in self.__animations.values():
            anim.rotate(angle)

    def rotozoom(self, angle, scale):
        for anim in self.__animations.values():
            anim.rotozoom(angle, scale)

    def flip(self, xbool, ybool):
        for anim in self.__animations.values():
            anim.flip(xbool, ybool)

    def clearTransforms(self):
        for anim in self.__animations.values():
            anim.clearTransforms()

    def getSize(self):
        for anim in self.__animations.values():
            return anim.getCurrentFrame().get_size()

    def setAnimation(self, name: AnimationName):
        if self.__playingName != name:
            self.__animation.stop()
            self.__playingName = name
            self.__animation = self.__animations[name]
            self.__animation.play()

    def blit(self, dst: pg.Surface, pos: tuple):
        if self.isFinished():
            dst.blit(self.__animation.getCurrentFrame(), pos)
        else:
            self.__animation.blit(dst, pos)

    def flip(self, xbool: bool, ybool: bool = False):
        for anim in self.__animations.values():
            anim.flip(xbool, ybool)

    def isFinished(self) -> bool:
        return self.__animation.state == pga.STOPPED

    def getAnimationName(self) -> AnimationName:
        return self.__playingName
