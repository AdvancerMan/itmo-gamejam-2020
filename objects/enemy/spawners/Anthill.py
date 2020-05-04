from Box2D import *
from game.Game import Game
from objects.enemy.objects.Ant import Ant
from objects.enemy.spawners.Spawner import Spawner
from objects.friendly.Player import Player
from util.textures.Textures import AnimationPackInfo


class Anthill(Spawner):
    def __init__(self, game: Game, process, player: Player, x: float, y: float):
        Spawner.__init__(self, game, process, player, 100,
                         game.getTextureManager().getAnimationPack(AnimationPackInfo.ANTHILL_ANIMATION),
                         process.getFactory().createRectangleBody(b2_staticBody, 51, 39),
                         Ant, x=x + 20, y=y + 25)
        self.setPosition(x, y)
