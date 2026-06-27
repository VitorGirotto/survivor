import pygame

from animation import Animation
from entity import Entity
from entity import ASSETS_DIR
from sprite_frames import PLAYER_ANIMATION_FRAMES
from sprite_sheet import SpriteSheet


class Player(Entity):
    def __init__(self, name: str, x: float, y: float) -> None:
        super().__init__(name, x, y)
        self.animations = self._load_animations()
        self.current_animation_name = "idle"
        self.facing_animation_name = "walk_right"
        self.surf = self.animations[self.current_animation_name].image
        self.rect = self.surf.get_rect(center=(x, y))

    def _load_animations(self) -> dict[str, Animation]:
        sprite_sheet = SpriteSheet(ASSETS_DIR / "char_base_sheet.png")
        return {
            name: Animation.from_sprite_sheet(sprite_sheet, frames, 0.1)
            for name, frames in PLAYER_ANIMATION_FRAMES.items()
        }

    def _set_animation(self, name: str) -> None:
        if name == self.current_animation_name:
            return

        self.current_animation_name = name
        self.animations[name].reset()

    def draw(self, screen: pygame.Surface):
        screen.blit(source=self.surf, dest=self.rect)

    def update(self, dt: float) -> None:
        keys = pygame.key.get_pressed()
        direction = pygame.Vector2(0, 0)

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            direction.y -= 1
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            direction.y += 1
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            direction.x -= 1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            direction.x += 1

        if direction.length() > 0:
            direction = direction.normalize()
            self.position += direction * 150 * dt

            if direction.x < 0:
                self.facing_animation_name = "walk_left"
            elif direction.x > 0:
                self.facing_animation_name = "walk_right"

            self._set_animation(self.facing_animation_name)
        else:
            self._set_animation("idle")

        self.animations[self.current_animation_name].update(dt)
        self.surf = self.animations[self.current_animation_name].image
        self.rect = self.surf.get_rect(
            center=(round(self.position.x), round(self.position.y))
        )
