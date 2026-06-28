from pathlib import Path

import pygame


def _resolve_assets_dir() -> Path:
    module_dir = Path(__file__).resolve().parent
    source_assets_dir = module_dir.parent / "assets"
    packaged_assets_dir = module_dir / "assets"

    if source_assets_dir.exists():
        return source_assets_dir
    return packaged_assets_dir


ASSETS_DIR = _resolve_assets_dir()


class Entity(pygame.sprite.Sprite):
    containers: tuple[pygame.sprite.Group, ...]

    def __init__(self, name: str, x: float, y: float) -> None:
        if hasattr(self, "containers"):
            super().__init__(*self.containers)
        else:
            super().__init__()
        self.name = name
        self.velocity = pygame.Vector2(0, 0)
        self.position: pygame.Vector2 = pygame.Vector2(x, y)
        self.surf = pygame.image.load(ASSETS_DIR / f"{name}.png").convert_alpha()
        self.rect = self.surf.get_rect(center=(x, y))

    # self.rect.center = (round(x), round(y))
    def draw(self, screen: pygame.Surface):
        pass

    def update(self, dt: float):
        pass
