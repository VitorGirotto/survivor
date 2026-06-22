import pygame

from constants import ENEMY_SPEED
from entity import Entity
from player import Player


class Enemy(Entity):
    def __init__(
        self,
        name: str,
        x: float,
        y: float,
        player: Player,
        enemies: pygame.sprite.Group,
    ) -> None:
        super().__init__(name, x, y)
        self.player = player
        self.speed = ENEMY_SPEED
        self.enemies = enemies
        self.radius = 24

    def draw(self, screen: pygame.Surface):
        screen.blit(source=self.surf, dest=self.rect)

    def update(self, dt):
        if self.rect.colliderect(self.player.rect):
            return

        direction = self.player.position - self.position

        if direction.length() > 0:
            direction = direction.normalize() * self.speed

        self.position += direction * dt
        self.rect.center = (round(self.position.x), round(self.position.y))
