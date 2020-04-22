import pygame as pg
from util.Logger import logger


class TextureManager:
    def __init__(self):
        self.__textures = {}

    # textureID should be taken from Textures.py
    def getTexture(self, textureID: str) -> pg.Surface:
        texture = self.__textures.get(textureID, None)
        if texture is None:
            try:
                texture = pg.image.load(textureID)
            except pg.error:
                logger.log("Error occured during loading " + textureID)
                texture = pg.Surface((20, 20))
                texture.fill((128, 0, 128))  # purple
            self.__textures[textureID] = texture
        return texture
