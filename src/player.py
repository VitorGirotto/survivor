import pygame
from constants import PLAYER_CENTERED_POS
from entity import Entity


class Player(Entity):
    def __init__(self, name: str, x: float, y: float) -> None:
        super().__init__(name, x, y)
        self.rect.center = PLAYER_CENTERED_POS

    def draw(self, screen: pygame.Surface):
        screen.blit(source=self.surf, dest=self.rect)

    def update(self, *args: Any, **kwargs: Any) -> None:
        return super().update(*args, **kwargs)
