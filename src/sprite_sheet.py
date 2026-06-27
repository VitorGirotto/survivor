from pathlib import Path

import pygame


Frame = tuple[int, int, int, int]


class SpriteSheet:
    def __init__(self, filename: str | Path) -> None:
        self.image = pygame.image.load(filename)
        if pygame.display.get_init() and pygame.display.get_surface() is not None:
            self.image = self.image.convert_alpha()

    def get_sprite(
        self,
        frame: Frame,
        *,
        scale: float = 1,
        colorkey: pygame.Color | str | tuple[int, int, int] | None = None,
    ) -> pygame.Surface:
        sprite = self.image.subsurface(pygame.Rect(frame)).copy()

        if colorkey is not None:
            sprite.set_colorkey(colorkey)

        if scale != 1:
            width = round(sprite.get_width() * scale)
            height = round(sprite.get_height() * scale)
            sprite = pygame.transform.scale(sprite, (width, height))

        return sprite

    def get_sprites(
        self,
        frames: list[Frame] | tuple[Frame, ...],
        *,
        scale: float = 1,
        colorkey: pygame.Color | str | tuple[int, int, int] | None = None,
    ) -> list[pygame.Surface]:
        return [
            self.get_sprite(frame, scale=scale, colorkey=colorkey) for frame in frames
        ]
