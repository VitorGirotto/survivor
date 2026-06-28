import pygame

from shot import Shot


class DamageableTarget(pygame.sprite.Sprite):
    def __init__(self, center=(0, 0), health=10):
        super().__init__()
        self.image = pygame.Surface((20, 20), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=center)
        self.position = pygame.Vector2(center)
        self.health = health


class TargetWithoutHealth(pygame.sprite.Sprite):
    def __init__(self, center=(0, 0)):
        super().__init__()
        self.image = pygame.Surface((20, 20), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=center)
        self.position = pygame.Vector2(center)


def make_shot(*args, **kwargs):
    shots = pygame.sprite.Group()
    Shot.containers = (shots,)
    shot = Shot(*args, **kwargs)
    return shot, shots


def test_shot_moves_in_direction_using_speed_and_dt():
    targets = pygame.sprite.Group()
    shot, _shots = make_shot(
        10, 20, pygame.Vector2(1, 0), targets, speed=100, damage=3
    )

    shot.update(0.5)

    assert shot.position == pygame.Vector2(60, 20)
    assert shot.rect.center == (60, 20)


def test_shot_damages_target_and_disappears_on_collision():
    target = DamageableTarget(center=(20, 20), health=10)
    targets = pygame.sprite.Group(target)
    shot, shots = make_shot(
        20, 20, pygame.Vector2(1, 0), targets, speed=100, damage=4
    )

    shot.update(0.1)

    assert target.health == 6
    assert shot not in shots
    assert target.alive()


def test_shot_kills_target_when_damage_reduces_health_to_zero():
    target = DamageableTarget(center=(20, 20), health=4)
    targets = pygame.sprite.Group(target)
    shot, _shots = make_shot(
        20, 20, pygame.Vector2(1, 0), targets, speed=100, damage=4
    )

    shot.update(0.1)

    assert target.health == 0
    assert not target.alive()


def test_shot_calls_callback_when_damage_kills_target():
    killed_targets = []
    target = DamageableTarget(center=(20, 20), health=4)
    targets = pygame.sprite.Group(target)
    shot, _shots = make_shot(
        20,
        20,
        pygame.Vector2(1, 0),
        targets,
        speed=100,
        damage=4,
        on_target_killed=killed_targets.append,
    )

    shot.update(0.1)

    assert killed_targets == [target]


def test_shot_does_not_call_callback_when_target_survives():
    killed_targets = []
    target = DamageableTarget(center=(20, 20), health=10)
    targets = pygame.sprite.Group(target)
    shot, _shots = make_shot(
        20,
        20,
        pygame.Vector2(1, 0),
        targets,
        speed=100,
        damage=4,
        on_target_killed=killed_targets.append,
    )

    shot.update(0.1)

    assert killed_targets == []


def test_shot_can_collide_with_entity_without_health():
    target = TargetWithoutHealth(center=(20, 20))
    targets = pygame.sprite.Group(target)
    shot, _shots = make_shot(
        20, 20, pygame.Vector2(1, 0), targets, speed=100, damage=4
    )

    shot.update(0.1)

    assert not shot.alive()
    assert not target.alive()
