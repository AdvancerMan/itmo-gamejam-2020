import pyganim as pga
from enum import Enum
from os.path import join
from util.textures.AnimationPack import AnimationName


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
    DETALIZED_GUN1 = _createPic("health.png")
    DETALIZED_GUN2 = _createPic("health.png")
    DETALIZED_GUN3 = _createPic("health.png")
    GUN1 = _createPic("health.png")
    GUN2 = _createPic("health.png")
    GUN3 = _createPic("health.png")
    BACKGROUND = _createPic("background.png")


class AnimationInfo(Enum):
    FRIEND_ANIMATION = _createAnimation(2, 3, [100] * 6, "pics", "friend.png")


class AnimationPackInfo(Enum):
    PLAYER_ANIMATION = _createAnimationPack(
        (AnimationName.RUN, 1, 4, [200] * 4, "pics", "player", "run.png"),
        (AnimationName.STAY, 1, 1, [100], "pics", "player", "stay.png"),
        (AnimationName.JUMP, 1, 1, [20], "pics", "player", "jump.png"),
        (AnimationName.FALL, 1, 1, [100], "pics", "player", "fall.png"),
        (AnimationName.LANDING, 1, 1, [100], "pics", "player", "land.png")
    )
    PLATFORM_ANIMATION = _createAnimationPack(
        (AnimationName.STAY, 1, 1, [100], "pics", "platforms", "halfColl.png")
    )
    USUALGUN_BULLET_ANIMATION = _createAnimationPack(
        (AnimationName.STAY, 1, 1, [100], "pics", "friend.png")
    )
    USUALGUN_ANIMATION = _createAnimationPack(
        (AnimationName.STAY, 1, 1, [100], "pics", "friend.png")
    )
    BALLISTICGUN_BULLET_ANIMATION = _createAnimationPack(
        (AnimationName.STAY, 1, 1, [100], "pics", "friend.png")
    )
    BALLISTICGUN_ANIMATION = _createAnimationPack(
        (AnimationName.STAY, 1, 1, [100], "pics", "friend.png")
    )
    STUPID_ENEMY_ANIMATION = PLAYER_ANIMATION
    ANT_ANIMATION = PLAYER_ANIMATION
    ANTHILL_ANIMATION = PLAYER_ANIMATION
