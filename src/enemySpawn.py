import random
from collections.abc import Callable
import pygame

from enemy import Enemy
from constants import ENEMY_SPAWN_RATE_SECONDS, SCREEN_HEIGHT, SCREEN_WIDTH
from player import Player

Edge = tuple[pygame.Vector2, Callable[[float], pygame.Vector2]]


class MapField(pygame.sprite.Sprite):
    containers: pygame.sprite.Group

    edge: list[Edge] = [
        (
            pygame.Vector2(-1, 0),
            lambda y: pygame.Vector2(-SCREEN_WIDTH - 20, y * SCREEN_HEIGHT),
        ),
        (
            pygame.Vector2(-1, 0),
            lambda y: pygame.Vector2(SCREEN_WIDTH + 20, y * SCREEN_HEIGHT),
        ),
        (
            pygame.Vector2(0, 1),
            lambda x: pygame.Vector2(x * SCREEN_WIDTH, -SCREEN_HEIGHT - 20),
        ),
        (
            pygame.Vector2(0, -1),
            lambda x: pygame.Vector2(x * SCREEN_WIDTH, SCREEN_HEIGHT + 20),
        ),
    ]

    def __init__(self, player, enemies) -> None:
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.spawn_time: float = 0.0
        self.elapsed_time: float = 0.0
        self.spawn_interval: float = ENEMY_SPAWN_RATE_SECONDS
        self.player: Player = player
        self.enemies: pygame.sprite.Group = enemies

    def spawn(
        self,
        name: str,
        position: pygame.Vector2,
    ) -> None:
        Enemy(name, position.x, position.y, self.player, self.enemies)

    def update(self, dt: float) -> None:
        self.elapsed_time += dt
        self.spawn_interval = max(
            0.1,
            ENEMY_SPAWN_RATE_SECONDS - 0.1 * int(self.elapsed_time // 12),
        )
        self.spawn_time += dt
        if self.spawn_time > self.spawn_interval:
            self.spawn_time = 0

            # spawn new enemy at a random edge of the screen
            edge = random.choice(self.edge)
            position = edge[1](random.uniform(0, 1))
            self.spawn("ENEMY_PLACEHOLDER", position)
