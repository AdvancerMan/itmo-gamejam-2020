import pygame as pg
from Box2D import *
from game.Game import Game
from gui.HealthBar import HealthBar
from objects.main.InGameObject import InGameObject
from objects.friendly.Player import Player
from util.Rectangle import Rectangle
from util.textures.Textures import AnimationPack


class Spawner(InGameObject):
    def __init__(self, game: Game, process, player: Player, health: float,
                 animation: AnimationPack, body: b2Body, MobConstructor, **kwargs):
        # process: GameProcess
        InGameObject.__init__(self, game, process, animation, body)
        kwargs.update({"game": game, "process": process, "player": player})
        self.__kwargs = kwargs
        self.__Constructor = MobConstructor
        self.__cooldown = 2
        self.__sinceLastSpawn = self.__cooldown
        self.__health = health
        self.__maxHealth = health
        self.__invulnerabilityTime = 0.1
        self.__sinceLastHit = self.__invulnerabilityTime
        self._healthBar = HealthBar(game)

    def preUpdate(self, delta: float):
        self.__sinceLastHit += delta
        self.__sinceLastSpawn += delta
        if self.__sinceLastSpawn >= self.__cooldown:
            self.__sinceLastSpawn = 0
            self.spawn()

    def postUpdate(self):
        if self.__health < 0:
            self.process.removeObject(self)

    def spawn(self):
        self.process.addObject(self.__Constructor(**self.__kwargs))

    def preSolve(self, obj, contact: b2Contact, oldManifold: b2Manifold):
        contact.enabled = False

    def isLand(self) -> bool:
        return False

    def takeDamage(self, amount: float, ignoreInvulnerability: bool = False):
        if ignoreInvulnerability or self.__sinceLastHit > self.__invulnerabilityTime:
            self.__sinceLastHit = 0
            self.__health -= amount

    def _postDraw(self, dst: pg.Surface, aabb: Rectangle, pos: tuple):
        size = aabb.size()
        pos = (pos[0] + size[0] / 2 - self._healthBar.getWidth() / 2, pos[1] - self._healthBar.getWidth())
        self._healthBar.draw(dst, pos, self.__health, self.__maxHealth)
