from Box2D import *
from game.Game import Game
from objects.platforms.Platform import Platform
from util.textures.Textures import AnimationPackInfo


class HalfCollidedPlatform(Platform):
    def __init__(self, game: Game, process, x: float, y: float, width: float, height: float):
        # process: GameProcess
        Platform.__init__(self, game, process,
                          game.getTextureManager().getAnimationPack(AnimationPackInfo.PLATFORM_ANIMATION),
                          x, y, width, height)
        self.__notColliding = set()

    def beginContact(self, obj, contact: b2Contact):
        super().beginContact(obj, contact)
        if obj.isAbove(self):
            self.__notColliding.add(obj)

    def preSolve(self, obj, contact: b2Contact, oldManifold: b2Manifold):
        if obj in self.__notColliding:
            contact.enabled = False

    def endContact(self, obj, contact: b2Contact):
        self.__notColliding.discard(obj)
