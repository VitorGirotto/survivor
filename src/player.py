import pygame
from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from entity import Entity


class Player(Entity):
    def __init__(self, name: str, x: float, y: float) -> None:
        super().__init__(name, x, y)

    def draw(self, screen: pygame.Surface):
        screen.blit(source=self.surf, dest=self.rect)

    def update(self, dt: float) -> None:
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.position.y -= 150 * dt
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.position.y += 150 * dt
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.position.x -= 150 * dt
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.position.x += 150 * dt

        self.rect.center = (round(self.position.x), round(self.position.y))
