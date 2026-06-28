import pygame

from constants import ENEMY_CONTACT_DAMAGE, PLAYER_HEALTH, PLAYER_SHOT_DAMAGE
from game import Game
from player import Player
from shot import Shot


class Target(pygame.sprite.Sprite):
    def __init__(self, center):
        super().__init__()
        self.image = pygame.Surface((20, 20), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=center)
        self.position = pygame.Vector2(center)
        self.health = 10


class FakeAnimation:
    def __init__(self):
        self.image = pygame.Surface((20, 20), pygame.SRCALPHA)

    def reset(self):
        pass

    def update(self, dt):
        pass


class NoKeysPressed:
    def __getitem__(self, key):
        return False


def make_player(center=(0, 0), targets=None, on_target_killed=None):
    player = Player.__new__(Player)
    player.position = pygame.Vector2(center)
    player.surf = pygame.Surface((20, 20), pygame.SRCALPHA)
    player.rect = pygame.Rect(0, 0, 20, 20)
    player.rect.center = center
    player.shot_targets = targets if targets is not None else pygame.sprite.Group()
    player.shot_cooldown_remaining = 0.0
    player.contact_damage_cooldown_remaining = 0.0
    player.health = PLAYER_HEALTH
    player.on_target_killed = on_target_killed
    player.animations = {"idle": FakeAnimation(), "walk_left": FakeAnimation()}
    player.current_animation_name = "idle"
    player.facing_animation_name = "walk_left"
    return player


def test_player_shoots_toward_nearest_enemy():
    shots = pygame.sprite.Group()
    Shot.containers = (shots,)
    far_enemy = Target((100, 0))
    nearest_enemy = Target((0, 50))
    targets = pygame.sprite.Group(far_enemy, nearest_enemy)
    player = make_player(targets=targets)

    player.shoot()

    shot = shots.sprites()[0]
    assert shot.velocity.normalize() == pygame.Vector2(0, 1)


def test_player_does_not_shoot_when_there_are_no_targets():
    shots = pygame.sprite.Group()
    Shot.containers = (shots,)
    player = make_player(targets=pygame.sprite.Group())

    player.shoot()

    assert len(shots) == 0


def test_player_keeps_empty_target_group_so_later_spawned_enemies_can_be_shot():
    shots = pygame.sprite.Group()
    Shot.containers = (shots,)
    targets = pygame.sprite.Group()
    player = make_player(targets=targets)
    targets.add(Target((100, 0)))

    player.shoot()

    assert player.shot_targets is targets
    assert len(shots) == 1


def test_player_constructor_keeps_empty_target_group(monkeypatch):
    def fake_entity_init(self, name, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.velocity = pygame.Vector2(0, 0)
        self.position = pygame.Vector2(x, y)
        self.surf = pygame.Surface((20, 20), pygame.SRCALPHA)
        self.rect = self.surf.get_rect(center=(x, y))

    monkeypatch.setattr("player.Entity.__init__", fake_entity_init)
    monkeypatch.setattr(
        "player.Player._load_animations", lambda self: {"idle": FakeAnimation()}
    )
    targets = pygame.sprite.Group()

    player = Player("PLAYER_PLACEHOLDER", 0, 0, targets)

    assert player.shot_targets is targets


def test_player_update_shoots_automatically_when_cooldown_is_ready(monkeypatch):
    shots = pygame.sprite.Group()
    Shot.containers = (shots,)
    enemy = Target((100, 0))
    player = make_player(targets=pygame.sprite.Group(enemy))
    monkeypatch.setattr(pygame.key, "get_pressed", lambda: NoKeysPressed())

    player.update(0.1)

    assert len(shots) == 1


def test_player_shot_callback_increments_when_enemy_is_killed():
    shots = pygame.sprite.Group()
    Shot.containers = (shots,)
    killed_targets = []
    enemy = Target((100, 0))
    enemy.health = PLAYER_SHOT_DAMAGE
    player = make_player(
        targets=pygame.sprite.Group(enemy), on_target_killed=killed_targets.append
    )

    player.shoot()
    shots.sprites()[0].update(0.45)

    assert killed_targets == [enemy]


def test_player_can_move_through_enemies():
    enemy = Target((25, 0))
    targets = pygame.sprite.Group(enemy)
    player = make_player(targets=targets)

    player._move(pygame.Vector2(1, 0), 1.0, speed=100)

    assert player.position == pygame.Vector2(100, 0)


def test_player_takes_damage_while_touching_enemy():
    enemy = Target((0, 0))
    player = make_player(targets=pygame.sprite.Group(enemy))

    player.apply_contact_damage(0.1)

    assert player.health == PLAYER_HEALTH - ENEMY_CONTACT_DAMAGE


def test_game_is_over_when_player_health_reaches_zero():
    game = Game.__new__(Game)
    game.player = make_player()
    game.player.health = 0

    assert game.is_game_over()
