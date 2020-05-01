from enum import Enum
from os.path import join
import pyganim as pga


def _createPic(*picPath: str) -> str:
    return join(*picPath)


def _createAnimation(rows: int, columns: int, framesDuration: list, *picsPath: str):  # -> (str, function, list<int>)
    assert rows * columns == len(framesDuration)
    picsPath = _createPic(*picsPath)
    return picsPath, lambda: pga.getImagesFromSpriteSheet(picsPath, rows=rows, cols=columns, rects=[]), framesDuration


class TextureInfo(Enum):
    BACKGROUND = _createPic("background.png")


class AnimationInfo(Enum):
    FRIEND_ANIMATION = _createAnimation(2, 3, [100] * 6, "pics", "friend.png")
    PLAYER_ANIMATION = _createAnimation(2, 3, [100] * 6, "pics", "friend.png")
