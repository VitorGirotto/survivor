import pygame

from constants import SHOT_RADIUS


class Shot(pygame.sprite.Sprite):
    containers: tuple[pygame.sprite.Group, ...]

    def __init__(
        self,
        x: float,
        y: float,
        direction: pygame.Vector2,
        targets: pygame.sprite.Group,
        *,
        speed: float,
        damage: int,
        max_distance: float | None = None,
        radius: int = SHOT_RADIUS,
    ) -> None:
        if hasattr(self, "containers"):
            super().__init__(*self.containers)
        else:
            super().__init__()

        if direction.length() == 0:
            raise ValueError("Shot direction cannot be zero")

        self.position = pygame.Vector2(x, y)
        self.start_position = pygame.Vector2(x, y)
        self.velocity = direction.normalize() * speed
        self.targets = targets
        self.damage = damage
        self.max_distance = max_distance
        self.radius = radius

        size = self.radius * 2
        self.surf = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.circle(self.surf, "yellow", (self.radius, self.radius), self.radius)
        self.image = self.surf
        self.rect = self.surf.get_rect(center=(round(x), round(y)))

    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(source=self.surf, dest=self.rect)

    def update(self, dt: float) -> None:
        self.position += self.velocity * dt
        self.rect.center = (round(self.position.x), round(self.position.y))

        self._handle_collision()
        self._kill_if_out_of_range()

    def _handle_collision(self) -> None:
        target = self._collided_target()
        if target is None:
            return

        target_health = getattr(target, "health", None)
        if target_health is not None:
            target_health -= self.damage
            setattr(target, "health", target_health)
            if target_health <= 0:
                target.kill()
        else:
            target.kill()

        self.kill()

    def _collided_target(self) -> pygame.sprite.Sprite | None:
        shot_rect = self.rect
        if shot_rect is None:
            return None

        for target in self.targets:
            target_rect = getattr(target, "rect", None)
            if target_rect is not None and shot_rect.colliderect(target_rect):
                return target

        return None

    def _kill_if_out_of_range(self) -> None:
        if self.max_distance is None:
            return

        if self.position.distance_to(self.start_position) >= self.max_distance:
            self.kill()
