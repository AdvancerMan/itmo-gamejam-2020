import pygame as pg
import pyganim as pga
from util.Logger import log
from util.textures.Textures import TextureInfo, AnimationInfo, AnimationPackInfo, AnimationPack, AnimationName
from traceback import format_exc
from os.path import join


class TextureManager:
    def __init__(self):
        self.__textures = {}

    def getAnimationPack(self, animationPackInfo: AnimationPackInfo) -> AnimationPack:
        animationInfos = animationPackInfo.value
        animations = {}
        for name, animationInfo in animationInfos.items():
            animations[name] = self.__getAnimation(*animationInfo)
        return AnimationPack(animations)

    def getAnimation(self, animationInfo: AnimationInfo) -> pga.PygAnimation:
        return self.__getAnimation(*animationInfo.value)

    def __getAnimation(self, path: str, loadTexture, duration: list) -> pga.PygAnimation:
        textures = self.__getTexture(path, loadTexture)
        if len(textures) != len(duration):
            textures = textures * len(duration)
        return pga.PygAnimation(list(zip(textures, duration)))

    def getTexture(self, textureInfo: TextureInfo) -> pg.Surface:
        return self.__getTexture(
            textureInfo.value,
            lambda: [pg.image.load(textureInfo.value)]
        )[0]

    def __getTexture(self, path: str, loadTexture) -> list:  # list of pg.Surface:
        texture = self.__textures.get(path, None)
        if texture is None:
            try:
                texture = loadTexture()
            except pg.error:
                log("Error occurred during loading %s:" % path)
                log(format_exc())
                texture = [pg.Surface((20, 20))]
                texture[0].fill((128, 0, 128))  # purple
            self.__textures[path] = texture
        return list(map(lambda txt: txt.copy(), texture))

    def getNumbers(self):
        path = join("pics", "Interface", "0123456789.png")
        return self.__getTexture(path, lambda: pga.getImagesFromSpriteSheet(path, rows=1, cols=10, rects=[]))
