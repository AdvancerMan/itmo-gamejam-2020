from Box2D import *
from game.Game import Game
from objects.enemy.objects.Enemy import Enemy
from objects.friendly.Player import Player
from util.textures.Textures import AnimationPackInfo


class StupidEnemy(Enemy):
    def __init__(self, game: Game, process, player: Player, x: float, y: float):
        # process: GameProcess
        Enemy.__init__(self, game, process, player,
                       game.getTextureManager().getAnimationPack(AnimationPackInfo.STUPID_ENEMY_ANIMATION),
                       process.getFactory().createRectangleBody(b2_dynamicBody, 40, 100), 0, 0)
        self.setPosition(x, y)

    def think(self) -> set:
        return {"shoot"}
