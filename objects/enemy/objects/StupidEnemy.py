from Box2D import *
from game.Game import Game
from objects.enemy.objects.Enemy import Enemy
from objects.friendly.Player import Player
from util.textures.Textures import AnimationPackInfo
from objects.guns.PlayerGuns import *
from config.Config import *


class StupidEnemy(Enemy):
    def __init__(self, game: Game, process, player: Player, x: float, y: float):
        # process: GameProcess
        Enemy.__init__(self, game, process, player,
                       game.getTextureManager().getAnimationPack(AnimationPackInfo.STUPID_ENEMY_ANIMATION),
                       process.getFactory().createRectangleBody(b2_dynamicBody, 40, 100), 15, 40, [UsualGun(game, process, self)])
        self.setPosition(x, y)
        self.hp = STUPID_ENEMY_HP
        self._playerToRight = False

    def sense(self, player: Player, objects: set):
        self._playerToRight = player.getPosition()[0] >= self.getPosition()[0]

    def think(self) -> set:
        return {"shoot"}


class StupidEnemyStaying(StupidEnemy):
    def think(self) -> set:
        result = super().think()
        if self._playerToRight != self.isDirectedToRight():
            result.add("changeDirection")
        return result


class StupidEnemyRunningTo(StupidEnemy):
    def think(self) -> set:
        result = super().think()
        if self._playerToRight:
            result.add("goRight")
        else:
            result.add("goLeft")
        return result


class StupidEnemyRunningFrom(StupidEnemy):
    def angleUpdate(self):
        if self.isDirectedToRight():
            self.shootAngle = b2Vec2(-1, 0)
        else:
            self.shootAngle = b2Vec2(1, 0)

    def think(self) -> set:
        result = super().think()
        if not self._playerToRight:
            result.add("goRight")
        else:
            result.add("goLeft")
        return result
