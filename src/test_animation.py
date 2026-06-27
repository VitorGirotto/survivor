import pygame

from animation import Animation
from sprite_sheet import SpriteSheet


def test_sprite_sheet_cuts_requested_frame(tmp_path):
    sheet_path = tmp_path / "sheet.png"
    sheet = pygame.Surface((20, 10), pygame.SRCALPHA)
    sheet.fill("red", pygame.Rect(0, 0, 10, 10))
    sheet.fill("blue", pygame.Rect(10, 0, 10, 10))
    pygame.image.save(sheet, sheet_path)

    sprite = SpriteSheet(sheet_path).get_sprite((10, 0, 10, 10))

    assert sprite.get_size() == (10, 10)
    assert sprite.get_at((0, 0)) == pygame.Color("blue")


def test_looping_animation_wraps_back_to_first_frame():
    frames = [pygame.Surface((1, 1)) for _ in range(2)]
    animation = Animation(frames, 0.5)

    animation.update(1.0)

    assert animation.image is frames[0]


def test_normal_animation_stops_on_last_frame():
    frames = [pygame.Surface((1, 1)) for _ in range(2)]
    animation = Animation(frames, 0.5, Animation.PlayMode.NORMAL)

    animation.update(2.0)

    assert animation.image is frames[1]
    assert animation.is_finished
