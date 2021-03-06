from Box2D import *

from config.Config import ANT_HP
from game.Game import Game
from objects.enemy.objects.Enemy import Enemy, b2Contact, b2Manifold
from objects.friendly.Player import Player
from util.FloatCmp import lessOrEquals
from util.textures.Textures import AnimationPackInfo


class Ant(Enemy):
    def __init__(self, game: Game, process, player: Player, x: float, y: float):
        Enemy.__init__(self, game, process, player,
                       game.getTextureManager().getAnimationPack(AnimationPackInfo.ANT_ANIMATION),
                       process.getFactory().createRectangleBody(b2_dynamicBody, 22, 18), 10, 0, [])
        self.setPosition(x, y)
        self.resetHp(ANT_HP)

    def think(self) -> set:
        return {"goRight" if self._playerToRight else "goLeft"}

    def beginContact(self, obj, contact: b2Contact):
        aabbs = (self.getAABB(), obj.getAABB())
        if lessOrEquals(aabbs[0].x + aabbs[0].w, aabbs[1].x):
            self.changeDirection()

    def preSolve(self, obj, contact: b2Contact, oldManifold: b2Manifold):
        if isinstance(obj, Player):
            obj.takeDamage(3)
