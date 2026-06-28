import pygame

from constants import ENEMY_SPAWN_RATE_SECONDS
from enemySpawn import MapField
from game import format_elapsed_time


class FakePlayer:
    position = pygame.Vector2(0, 0)


def make_map_field():
    field = MapField.__new__(MapField)
    field.spawn_time = 0.0
    field.elapsed_time = 0.0
    field.player = FakePlayer()
    field.enemies = pygame.sprite.Group()
    field.spawn_count = 0

    def fake_spawn(name, position):
        field.spawn_count += 1

    field.spawn = fake_spawn
    return field


def test_format_elapsed_time_as_minutes_and_seconds():
    assert format_elapsed_time(0) == "00:00"
    assert format_elapsed_time(65.9) == "01:05"
    assert format_elapsed_time(600) == "10:00"


def test_enemy_spawn_interval_gets_half_second_faster_every_15_seconds():
    field = make_map_field()

    field.update(15.0)

    assert field.spawn_interval == ENEMY_SPAWN_RATE_SECONDS - 0.5


def test_enemy_spawn_interval_has_minimum_half_second():
    field = make_map_field()

    field.update(60.0)

    assert field.spawn_interval == 0.5
