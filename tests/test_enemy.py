import pygame

import enemy
from enemy import Enemy
from sprite_frames import ENEMY_ANIMATION_FRAMES


class FakePlayer:
    def __init__(self, center):
        self.position = pygame.Vector2(center)
        self.image = pygame.Surface((20, 20), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=center)


class FakeAnimation:
    def __init__(self, image):
        self.image = image
        self.update_calls = []
        self.reset_calls = 0

    def update(self, dt):
        self.update_calls.append(dt)

    def reset(self):
        self.reset_calls += 1


def make_enemy(center=(0, 0), player_center=(100, 0)):
    enemy_instance = Enemy.__new__(Enemy)
    enemy_instance.name = "ENEMY_PLACEHOLDER"
    enemy_instance.velocity = pygame.Vector2(0, 0)
    enemy_instance.position = pygame.Vector2(center)
    enemy_instance.surf = pygame.Surface((20, 20), pygame.SRCALPHA)
    enemy_instance.rect = enemy_instance.surf.get_rect(center=center)
    enemy_instance.player = FakePlayer(player_center)
    enemy_instance.speed = 70
    enemy_instance.enemies = pygame.sprite.Group()
    enemy_instance.radius = 42
    enemy_instance.health = 10
    enemy_instance.animations = {
        "walk_right": FakeAnimation(pygame.Surface((22, 24), pygame.SRCALPHA)),
        "walk_left": FakeAnimation(pygame.Surface((23, 25), pygame.SRCALPHA)),
    }
    enemy_instance.current_animation_name = "walk_right"
    return enemy_instance


def test_enemy_loads_walk_animations_from_slime_sprite_sheet(monkeypatch):
    loaded_sheets = []
    animation_calls = []

    def fake_entity_init(self, name, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.velocity = pygame.Vector2(0, 0)
        self.position = pygame.Vector2(x, y)
        self.surf = pygame.Surface((20, 20), pygame.SRCALPHA)
        self.rect = self.surf.get_rect(center=(x, y))

    class FakeSpriteSheet:
        def __init__(self, filename):
            loaded_sheets.append(filename)

    class FakeAnimationClass:
        @classmethod
        def from_sprite_sheet(cls, sprite_sheet, frames, frame_duration, *, scale=1):
            animation_calls.append((sprite_sheet, frames, frame_duration, scale))
            return FakeAnimation(pygame.Surface((20, 20), pygame.SRCALPHA))

    monkeypatch.setattr("enemy.Entity.__init__", fake_entity_init)
    monkeypatch.setattr(enemy, "SpriteSheet", FakeSpriteSheet, raising=False)
    monkeypatch.setattr(enemy, "Animation", FakeAnimationClass, raising=False)

    enemy_instance = Enemy(
        "ENEMY_PLACEHOLDER", 0, 0, FakePlayer((100, 0)), pygame.sprite.Group()
    )

    assert loaded_sheets[0].name == "Slime1_Walk_body.png"
    assert enemy_instance.animations.keys() == ENEMY_ANIMATION_FRAMES.keys()
    assert animation_calls[0][1] == ENEMY_ANIMATION_FRAMES["walk_right"]
    assert animation_calls[1][1] == ENEMY_ANIMATION_FRAMES["walk_left"]
    assert enemy_instance.current_animation_name == "walk_right"


def test_enemy_uses_right_walk_animation_when_moving_right():
    enemy_instance = make_enemy(player_center=(100, 0))

    enemy_instance.update(0.1)

    assert enemy_instance.current_animation_name == "walk_right"
    assert enemy_instance.surf is enemy_instance.animations["walk_right"].image
    assert enemy_instance.animations["walk_right"].update_calls == [0.1]


def test_enemy_uses_left_walk_animation_when_moving_left():
    enemy_instance = make_enemy(player_center=(-100, 0))

    enemy_instance.update(0.1)

    assert enemy_instance.current_animation_name == "walk_left"
    assert enemy_instance.surf is enemy_instance.animations["walk_left"].image
    assert enemy_instance.animations["walk_left"].reset_calls == 1
    assert enemy_instance.animations["walk_left"].update_calls == [0.1]
