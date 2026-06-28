import pygame

from animation import Animation
from constants import ENEMY_HEALTH, ENEMY_SPEED
from entity import ASSETS_DIR
from entity import Entity
from player import Player
from sprite_frames import ENEMY_ANIMATION_FRAMES
from sprite_sheet import SpriteSheet


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
        self.radius = 42
        self.health = ENEMY_HEALTH
        self.animations = self._load_animations()
        self.current_animation_name = "walk_right"
        self.surf = self.animations[self.current_animation_name].image
        self.rect = self.surf.get_rect(center=(x, y))

    def _load_animations(self) -> dict[str, Animation]:
        sprite_sheet = SpriteSheet(ASSETS_DIR / "Slime1_Walk_body.png")
        return {
            name: Animation.from_sprite_sheet(sprite_sheet, frames, 0.1, scale=1.5)
            for name, frames in ENEMY_ANIMATION_FRAMES.items()
        }

    def _set_animation(self, name: str) -> None:
        if name == self.current_animation_name:
            return

        self.current_animation_name = name
        self.animations[name].reset()

    def draw(self, screen: pygame.Surface):
        screen.blit(source=self.surf, dest=self.rect)

    def update(self, dt):
        # Vector for following the player
        direction_to_player = self.player.position - self.position
        if direction_to_player.length() > 0:
            direction_to_player = direction_to_player.normalize() * self.speed

        if direction_to_player.x < 0:
            self._set_animation("walk_left")
        elif direction_to_player.x > 0:
            self._set_animation("walk_right")

        # Avoind collision with player (Enemy -> Player)
        if self.rect.colliderect(self.player.rect):
            self.animations[self.current_animation_name].update(dt)
            self.surf = self.animations[self.current_animation_name].image
            self.rect = self.surf.get_rect(
                center=(round(self.position.x), round(self.position.y))
            )
            return

        # Repulsion force
        repulsion = pygame.Vector2(0, 0)
        neighbors = 0

        for other in self.enemies:
            if other is self:
                continue

            distance_to_other = self.position.distance_to(other.position)

            # Collision or proximity
            if 0 < distance_to_other < self.radius:
                escape = self.position - other.position
                escape = escape.normalize()

                # Closest = stronger repulsion
                escape /= distance_to_other

                repulsion += escape
                neighbors += 1

        if neighbors > 0:
            repulsion /= neighbors
            if repulsion.length() > 0:
                repulsion = repulsion.normalize() * self.speed * 1.3

        # applying physics for movement
        final_repulsion_force = direction_to_player + repulsion
        if final_repulsion_force.length() > 0:
            self.velocity = final_repulsion_force.normalize() * self.speed
        self.position += self.velocity * dt
        self.animations[self.current_animation_name].update(dt)
        self.surf = self.animations[self.current_animation_name].image
        self.rect = self.surf.get_rect(
            center=(round(self.position.x), round(self.position.y))
        )
