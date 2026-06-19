import pygame

from constants import ENEMY_VELOCITY, SCREEN_HEIGHT, SCREEN_WIDTH
from entity import Entity
from player import Player


class Enemy(Entity):
    def __init__(self, name: str, x: float, y: float, player: Player) -> None:
        super().__init__(name, x, y)
        self.player = player
        self.speed = ENEMY_VELOCITY

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
