from game.Game import Game
from objects.platforms.Platform import Platform
from util.textures.Textures import AnimationPackInfo


class SolidPlatform(Platform):
    def __init__(self, game: Game, process, x: float, y: float, width: float, height: float):
        # process: GameProcess
        Platform.__init__(self, game, process,
                          game.getTextureManager().getAnimationPack(AnimationPackInfo.PLATFORM_ANIMATION),
                          x, y, width, height)
