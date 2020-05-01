from Box2D import *
from game.Game import Game
from objects.enemy.Enemy import Enemy
from objects.friendly.Player import Player
from util.textures.Textures import AnimationInfo


class StupidEnemy(Enemy):
    def __init__(self, game: Game, process, player: Player):
        # process: GameProcess
        Enemy.__init__(self, game, process, player,
                       game.getTextureManager().getAnimation(AnimationInfo.STUPID_ENEMY_ANIMATION),
                       process.getFactory().createRectangleBody(self, b2_dynamicBody, 40, 100),
                       40, 80)
