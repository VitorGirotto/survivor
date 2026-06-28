import pygame

from constants import ENEMY_SPAWN_RATE_SECONDS
from enemySpawn import MapField
from game import Game, format_elapsed_time


class FakePlayer:
    position = pygame.Vector2(0, 0)


class FakeTextSurface:
    def get_rect(self, **kwargs):
        return kwargs


class FakeFont:
    def __init__(self):
        self.render_calls = []

    def render(self, text, antialias, color):
        self.render_calls.append((text, antialias, color))
        return FakeTextSurface()


class FakeScreen:
    def __init__(self):
        self.blit_calls = []

    def blit(self, surface, rect):
        self.blit_calls.append((surface, rect))


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


def test_game_score_increments_by_one_per_killed_enemy():
    game = Game.__new__(Game)
    game.score = 0

    game.increase_score(pygame.sprite.Sprite())

    assert game.score == 1


def test_game_draws_score_in_top_left_corner():
    game = Game.__new__(Game)
    game.score = 7
    game.timer_font = FakeFont()
    game.screen = FakeScreen()

    game.draw_score()

    assert game.timer_font.render_calls == [("Score: 7", True, "white")]
    assert game.screen.blit_calls[0][1] == {"topleft": (20, 20)}


def test_game_draws_background_image_at_map_rect():
    game = Game.__new__(Game)
    game.screen = FakeScreen()
    game.map_bg_image = pygame.Surface((100, 80), pygame.SRCALPHA)
    game.rect = game.map_bg_image.get_rect(left=0, top=0)

    game.draw_background()

    assert game.screen.blit_calls == [(game.map_bg_image, game.rect)]


def test_enemy_spawn_interval_gets_half_second_faster_every_15_seconds():
    field = make_map_field()

    field.update(15.0)

    assert field.spawn_interval == ENEMY_SPAWN_RATE_SECONDS - 0.5


def test_enemy_spawn_interval_has_minimum_half_second():
    field = make_map_field()

    field.update(60.0)

    assert field.spawn_interval == 0.5
