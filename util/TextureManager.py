import pygame as pg
import pyganim as pga
from util.Logger import log
from util.Textures import TextureInfo, AnimationInfo


class TextureManager:
    def __init__(self):
        self.__textures = {}

    def getAnimation(self, animationInfo: AnimationInfo) -> pga.PygAnimation:
        return pga.PygAnimation(list(map(
            lambda pathToDuration: (self.__getTexture(pathToDuration[0]), pathToDuration[1]),
            animationInfo.value
        )))

    def getTexture(self, textureInfo: TextureInfo) -> pg.Surface:
        return self.__getTexture(textureInfo.value)

    def __getTexture(self, path: str) -> pg.Surface:
        texture = self.__textures.get(path, None)
        if texture is None:
            try:
                texture = pg.image.load(path)
            except pg.error:
                log("Error occurred during loading " + path)
                texture = pg.Surface((20, 20))
                texture.fill((128, 0, 128))  # purple
            self.__textures[path] = texture
        return texture.copy()
