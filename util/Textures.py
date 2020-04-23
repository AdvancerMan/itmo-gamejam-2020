from enum import Enum
from os.path import join


def _createPic(*picPath: str):
    return join(*picPath) + ".png"


def _createAnimation(frameCount: int, framesDuration: list, *picsPath: str):
    picsPath = join(*picsPath)
    return list(zip([_createPic(picsPath + str(i)) for i in range(1, frameCount + 1)], framesDuration))


class TextureInfo(Enum):
    BACKGROUND = _createPic("background")


class AnimationInfo(Enum):
    PLAYER_ANIMATION = _createAnimation(5, [100] * 5, "player")

