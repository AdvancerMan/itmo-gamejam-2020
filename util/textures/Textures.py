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
    BACKGROUND = _createPic("background.png")


class AnimationInfo(Enum):
    FRIEND_ANIMATION = _createAnimation(2, 3, [100] * 6, "pics", "friend.png")


class AnimationPackInfo(Enum):
    PLAYER_ANIMATION = _createAnimationPack(
        (AnimationName.RUN, 1, 4, [200] * 4, "pics", "Player", "Cosmopoc_walk.png"),
        (AnimationName.STAY, 1, 1, [100], "pics", "Player", "Cosmopoc_static.png"),
        (AnimationName.JUMP, 1, 1, [100], "pics", "Player", "Cosmopoc_jump_1cut.png"),
        (AnimationName.FALL, 1, 1, [100], "pics", "Player", "Cosmopoc_jump_2cut.png"),
        (AnimationName.LANDING, 1, 1, [100], "pics", "Player", "Cosmopoc_jump_3cut.png")
    )
    PLATFORM_ANIMATION = _createAnimationPack(
        (AnimationName.STAY, 1, 1, [100], "pics", "friend.png")
    )
    USUALGUN_BULLET_ANIMATION = _createAnimationPack(
        (AnimationName.STAY, 1, 1, [100], "pics", "friend.png")
    )
    USUALGUN_ANIMATION = _createAnimationPack(
        (AnimationName.STAY, 1, 1, [100], "pics", "friend.png")
    )
    STUPID_ENEMY_ANIMATION = _createAnimationPack(
        (AnimationName.STAY, 2, 3, [100] * 6, "pics", "friend.png")
    )
