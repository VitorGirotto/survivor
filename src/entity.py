import pygame


class Entity(pygame.sprite.Sprite):
    containers: tuple[pygame.sprite.Group, ...]

    def __init__(self, name: str, x: float, y: float) -> None:
        if hasattr(self, "containers"):
            super().__init__(*self.containers)
        else:
            super().__init__()
        self.name = name
        self.position: pygame.Vector2 = pygame.Vector2(x, y)
        self.surf = pygame.image.load("../assets/" + name + ".png").convert_alpha()
        self.rect = self.surf.get_rect(center=(x, y))

        # self.rect.center = (round(x), round(y))
        def draw(self, screen: pygame.Surface):
            pass

        def update(self, dt: float):
            pass
