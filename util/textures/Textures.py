import pygame as pg
import pyganim as pga
from enum import Enum, IntEnum, auto
from os.path import join


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
        self.__animations = dict.fromkeys((i for i in dir(AnimationName) if i[0] != "_"),
                                          animations[AnimationName.STAY].getCopy())
        self.__animations = dict()
        self.__animations.update(animations)
        breakAnimationLoops(self.__animations)
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

    def clearTransforms(self):
        for anim in self.__animations.values():
            anim.clearTransforms()

    def getSize(self):
        for anim in self.__animations.values():
            return anim.getCurrentFrame().get_size()

    def setAnimation(self, name: AnimationName):
        if self.__playingName != name:
            if name not in self.__animations:
                return
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


def _createPic(*picPath: str) -> str:
    return join(*picPath)


def _createAnimation(rows: int, columns: int, framesDuration: list, *picsPath: str):  # -> (str, function, list<int>)
    assert rows * columns == len(framesDuration)
    picsPath = _createPic(*picsPath)
    return picsPath, lambda: pga.getImagesFromSpriteSheet(picsPath, rows=rows, cols=columns, rects=[]), framesDuration


def _createAnimationPack(*nameAndAnimationInfoArgs) -> dict:
    animations = {}
    for args in nameAndAnimationInfoArgs:
        animations[args[0]] = _createAnimation(*args[1:])
    return animations


class TextureInfo(Enum):
    HEALTH_BAR = _createPic("pics", "Bar", "Hp.png")
    HEALTH_BAR_LOWER = _createPic("pics", "Bar", "Bar.png")
    HEALTH_BAR_UPPER = _createPic("pics", "Bar", "Cap.png")
    GUNS_BACKGROUND = _createPic("pics", "Interface", "Gun_interface.png")
    DETALIZED_GUN1 = _createPic("pics", "Guns", "Big_gravity_gun.png")
    DETALIZED_GUN2 = _createPic("pics", "Guns", "Big_poison_gun.png")
    DETALIZED_GUN3 = _createPic("pics", "Guns", "Big_power_gun.png")
    GUN1 = _createPic("pics", "Guns", "Mini_gravity_gun.png")
    GUN2 = _createPic("pics", "Guns", "Mini_poison_gun.png")
    GUN3 = _createPic("pics", "Guns", "Mini_power_gun.png")
    BACKGROUND = _createPic("pics", "background.png")
    LIGHT_BASE = _createPic("pics", "base", "light.png")


class AnimationInfo(Enum):
    BASE_ANIMATION = _createAnimation(1, 2, [100] * 2, "pics", "base", "base.png")
    FRIEND_ANIMATION = _createAnimation(2, 3, [100] * 6, "pics", "friend.png")


class AnimationPackInfo(Enum):
    PLAYER_ANIMATION = _createAnimationPack(
        (AnimationName.RUN, 1, 4, [200] * 4, "pics", "player", "run.png"),
        (AnimationName.STAY, 1, 1, [100], "pics", "player", "stay.png"),
        (AnimationName.JUMP, 1, 1, [20], "pics", "player", "jump.png"),
        (AnimationName.FALL, 1, 1, [100], "pics", "player", "fall.png"),
        (AnimationName.LANDING, 1, 1, [100], "pics", "player", "land.png")
    )
    HALF_COL_PLATFORM_ANIMATION = _createAnimationPack(
        (AnimationName.STAY, 1, 1, [100], "pics", "platforms", "halfColl.png")
    )
    PLATFORM_ANIMATION = _createAnimationPack(
        (AnimationName.STAY, 1, 1, [100], "pics", "platforms", "Platform.png")
    )
    USUALGUN_BULLET_ANIMATION = _createAnimationPack(
        (AnimationName.STAY, 1, 1, [100], "pics", "friend.png")
    )
    USUALGUN_ANIMATION = _createAnimationPack(
        (AnimationName.STAY, 1, 1, [100], "pics", "hand.png")
    )
    BALLISTICGUN_BULLET_ANIMATION = _createAnimationPack(
        (AnimationName.STAY, 1, 1, [100], "pics", "friend.png")
    )
    BALLISTICGUN_ANIMATION = _createAnimationPack(
        (AnimationName.STAY, 1, 1, [100], "pics", "friend.png")
    )
    POISONGUN_BULLET_ANIMATION = _createAnimationPack(
        (AnimationName.STAY, 1, 1, [100], "pics", "friend.png")
    )
    POISONGUN_ANIMATION = _createAnimationPack(
        (AnimationName.STAY, 1, 1, [100], "pics", "Guns", "Big_gravity_gun.png")
    )
    POISONEXPLODE_ANIMATION = _createAnimationPack(
        (AnimationName.STAY, 1, 1, [100], "pics", "friend.png")
    )
    ANT_ANIMATION = _createAnimationPack(
        (AnimationName.STAY, 1, 7, [100] * 7, "pics", "enemy", "Ant.png"),
        (AnimationName.RUN, 1, 7, [100] * 7, "pics", "enemy", "Ant.png")
    )
    STUPID_ENEMY_ANIMATION = PLAYER_ANIMATION
    ANTHILL_ANIMATION = PLAYER_ANIMATION
