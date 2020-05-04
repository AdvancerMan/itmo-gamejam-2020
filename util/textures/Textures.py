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
    SHOOT = auto()


def breakAnimationLoops(animations: dict):
    for name in (AnimationName.JUMP, AnimationName.LANDING, AnimationName.SHOOT):
        if name in animations:
            animations[name].loop = False


class AnimationPack:
    def __init__(self, animations: dict):
        for name, anim in animations.items():
            assert isinstance(name, AnimationName)
            assert isinstance(anim, pga.PygAnimation)
        self.__animations = animations
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

    def setAnimation(self, name: AnimationName, restartAnimation: bool = False) -> bool:
        if self.__playingName != name or restartAnimation:
            if name not in self.__animations:
                return False
            self.__animation.stop()
            self.__playingName = name
            self.__animation = self.__animations[name]
            self.__animation.play()
            return True
        return False

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

    def getCopy(self):
        copied = {}
        for name, anim in self.__animations.items():
            copied[name] = anim.getCopy()
        return AnimationPack(copied)


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
    DETALIZED_GUN1 = _createPic("pics", "Guns", "Big_poison_gun.png")
    DETALIZED_GUN2 = _createPic("pics", "Guns", "Big_power_gun.png")
    DETALIZED_GUN3 = _createPic("pics", "Guns", "Big_gravity_gun.png")
    GUN1 = _createPic("pics", "Guns", "Mini_poison_gun.png")
    GUN2 = _createPic("pics", "Guns", "Mini_power_gun.png")
    GUN3 = _createPic("pics", "Guns", "Mini_gravity_gun.png")
    BACKGROUND = _createPic("pics", "background.png")
    LIGHT_BASE = _createPic("pics", "base", "light.png")
    BAD_BASE = _createPic("pics", "base", "light.png")


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
        (AnimationName.STAY, 1, 1, [100], "pics", "Bullet", "poison_bullet.png")
    )
    POISONGUN_ANIMATION = _createAnimationPack(
        (AnimationName.STAY, 1, 1, [100], "pics", "Guns", "poison_gun_static.png"),
        (AnimationName.SHOOT, 1, 6, [30] * 6, "pics", "Guns", "poison_gun_animation.png")
    )
    POISONEXPLODE_ANIMATION = _createAnimationPack(
        (AnimationName.STAY, 1, 1, [100], "pics", "Bullet", "poison_bullet_bang.png")
    )
    POWERGUN_ANIMATION = _createAnimationPack(
        (AnimationName.STAY, 1, 1, [100], "pics", "Guns", "power_gun_static.png"),
        (AnimationName.SHOOT, 1, 6, [30] * 6, "pics", "Guns", "power_gun_animation.png")
    )
    POWERGUN_BULLET_ANIMATION = _createAnimationPack(
        (AnimationName.STAY, 1, 2, [100] * 2, "pics", "Bullet", "power_bullet.png")
    )
    POWER_EXPLODE_BULLET_ANIMATION = _createAnimationPack(
        (AnimationName.STAY, 1, 6, [100] * 6, "pics", "Bullet", "power_bullet_bang.png")
    )
    GRAVITYGUN_ANIMATION = _createAnimationPack(
        (AnimationName.STAY, 1, 1, [100], "pics", "Guns", "gravity_gun_static.png"),
        (AnimationName.SHOOT, 1, 4, [30] * 4, "pics", "Guns", "gravity_gun_animation.png")
    )
    GRAVITYGUN_BULLET_ANIMATION = _createAnimationPack(
        (AnimationName.STAY, 1, 1, [100], "pics", "Bullet", "gravity_bullet.png")
    )
    GRAVITY_EXPLODE_BULLET_ANIMATION = _createAnimationPack(
        (AnimationName.STAY, 1, 4, [50] * 4, "pics", "Bullet", "Gravity_bullet_bang.png")
    )
    ANT_ANIMATION = _createAnimationPack(
        (AnimationName.STAY, 1, 7, [100] * 7, "pics", "enemy", "Ant.png"),
    )
    BIG_ENEMY_ANIMATION = _createAnimationPack(
        (AnimationName.STAY, 1, 1, [100], "pics", "enemy", "Big_enemy.png")
    )
    BIG_ENEMY_BULLET_ANIMATION = _createAnimationPack(
        (AnimationName.STAY, 1, 1, [100], "pics", "Bullet", "Big_enemy_bullet.png")
    )
    ENEMY_BULLET_ANIMATION = _createAnimationPack(
        (AnimationName.STAY, 1, 1, [100], "pics", "Bullet", "enemy_bullet.png")
    )
    BIG_ENEMY_GUN_ANIMATION = _createAnimationPack(
        (AnimationName.STAY, 1, 1, [100], "pics", "enemy", "Big_enemy_gun_static.png"),
        (AnimationName.SHOOT, 1, 5, [30] * 5, "pics", "enemy", "Big_enemy_gun_animation.png")
    )
    ENEMY_ANIMATION = _createAnimationPack(
        (AnimationName.STAY, 1, 5, [100] * 5, "pics", "enemy", "enemy_run.png")
    )
    ENEMY_GUN_ANIMATION = _createAnimationPack(
        (AnimationName.STAY, 1, 1, [100], "pics", "enemy", "enemy_gun_static.png"),
        (AnimationName.SHOOT, 1, 5, [30] * 5, "pics", "enemy", "enemy_gun.png")
    )
    STUPID_ENEMY_ANIMATION = PLAYER_ANIMATION
    ANTHILL_ANIMATION = _createAnimationPack(
        (AnimationName.STAY, 1, 1, [100], "pics", "enemy", "Ant_hill.png")
    )
