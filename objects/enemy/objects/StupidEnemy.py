from Box2D import *
from game.Game import Game
from objects.enemy.objects.Enemy import Enemy
from objects.friendly.Player import Player
from util.textures.Textures import AnimationPackInfo
from objects.guns.PlayerGuns import *
from config.Config import *


class StupidEnemy(Enemy):
    def __init__(self, game: Game, process, player: Player, animation, body, gun, x: float, y: float):
        # process: GameProcess
        Enemy.__init__(self, game, process, player, animation, body, 8, 40, [gun])
        self.setPosition(x, y)
        self.hp = self.resetHp(STUPID_ENEMY_HP)

    def think(self) -> set:
        return {"shoot"}


class StupidEnemyStaying(StupidEnemy):
    def __init__(self, game: Game, process, player: Player, x: float, y: float):
        super().__init__(game, process, player,
                         game.getTextureManager().getAnimationPack(AnimationPackInfo.BIG_ENEMY_ANIMATION),
                         process.getFactory().createRectangleBody(b2_dynamicBody, 106, 96),
                         BigEnemyGun(game, process, self), x, y)

    def think(self) -> set:
        result = super().think()
        if self._playerToRight != self.isDirectedToRight():
            result.add("changeDirection")
        return result


class StupidEnemyRunningTo(StupidEnemy):
    def __init__(self, game: Game, process, player: Player, x: float, y: float):
        super().__init__(game, process, player,
                         game.getTextureManager().getAnimationPack(AnimationPackInfo.ENEMY_ANIMATION),
                         process.getFactory().createRectangleBody(b2_dynamicBody, 63, 81),
                         EnemyGun(game, process, self), x, y)

    def think(self) -> set:
        result = super().think()
        if self._playerToRight:
            result.add("goRight")
        else:
            result.add("goLeft")
        return result


class StupidEnemyRunningFrom(StupidEnemy):
    def __init__(self, game: Game, process, player: Player, x: float, y: float):
        super().__init__(game, process, player,
                         game.getTextureManager().getAnimationPack(AnimationPackInfo.STUPID_ENEMY_ANIMATION),
                         process.getFactory().createRectangleBody(b2_dynamicBody, 40, 100),
                         UsualGun(game, process, self), x, y)

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
