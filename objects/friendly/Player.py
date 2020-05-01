from Box2D import *
from game.Game import Game
from objects.base.InGameObject import InGameObject
from util.textures.Textures import AnimationInfo


class Player(InGameObject):
    def __init__(self, game: Game, process):
        # process: GameProcess
        super().__init__(game, process,
                         game.getTextureManager().getAnimation(AnimationInfo.PLAYER_ANIMATION),
                         process.getFactory().createRectangleBody(self, b2_dynamicBody, 40, 100))

    def update(self):
        pass
