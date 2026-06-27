import pygame

from animation import Animation
from constants import (
    PLAYER_SHOT_COOLDOWN_SECONDS,
    PLAYER_SHOT_DAMAGE,
    PLAYER_SHOT_MAX_DISTANCE,
    PLAYER_SHOT_SPEED,
)
from entity import Entity
from entity import ASSETS_DIR
from shot import Shot
from sprite_frames import PLAYER_ANIMATION_FRAMES
from sprite_sheet import SpriteSheet


class Player(Entity):
    def __init__(
        self,
        name: str,
        x: float,
        y: float,
        shot_targets: pygame.sprite.Group | None = None,
    ) -> None:
        super().__init__(name, x, y)
        self.shot_targets = shot_targets or pygame.sprite.Group()
        self.shot_cooldown_remaining = 0.0
        self.animations = self._load_animations()
        self.current_animation_name = "idle"
        self.facing_animation_name = "walk_right"
        self.surf = self.animations[self.current_animation_name].image
        self.rect = self.surf.get_rect(center=(x, y))

    def _load_animations(self) -> dict[str, Animation]:
        sprite_sheet = SpriteSheet(ASSETS_DIR / "char_base_sheet.png")
        return {
            name: Animation.from_sprite_sheet(sprite_sheet, frames, 0.1, scale=1.5)
            for name, frames in PLAYER_ANIMATION_FRAMES.items()
        }

    def _set_animation(self, name: str) -> None:
        if name == self.current_animation_name:
            return

        self.current_animation_name = name
        self.animations[name].reset()

    def draw(self, screen: pygame.Surface):
        screen.blit(source=self.surf, dest=self.rect)

    def shoot(self) -> None:
        direction = pygame.Vector2(1, 0)
        if self.facing_animation_name == "walk_left":
            direction = pygame.Vector2(-1, 0)

        Shot(
            self.position.x,
            self.position.y,
            direction,
            self.shot_targets,
            speed=PLAYER_SHOT_SPEED,
            damage=PLAYER_SHOT_DAMAGE,
            max_distance=PLAYER_SHOT_MAX_DISTANCE,
        )
        self.shot_cooldown_remaining = PLAYER_SHOT_COOLDOWN_SECONDS

    def update(self, dt: float) -> None:
        keys = pygame.key.get_pressed()
        direction = pygame.Vector2(0, 0)
        self.shot_cooldown_remaining = max(0, self.shot_cooldown_remaining - dt)

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

        if keys[pygame.K_SPACE] and self.shot_cooldown_remaining == 0:
            self.shoot()

        self.animations[self.current_animation_name].update(dt)
        self.surf = self.animations[self.current_animation_name].image
        self.rect = self.surf.get_rect(
            center=(round(self.position.x), round(self.position.y))
        )
