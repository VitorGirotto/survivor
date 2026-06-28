from constants import SCREEN_HEIGHT
from menu import Menu


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


def test_menu_draws_wasd_movement_hint_in_bottom_left_corner():
    menu = Menu.__new__(Menu)
    menu.screen = FakeScreen()
    menu.hint_font = FakeFont()

    menu.draw_movement_hint()

    assert menu.hint_font.render_calls == [
        ("Use WASD for Player movement", True, "white")
    ]
    assert menu.screen.blit_calls[0][1] == {"bottomleft": (20, SCREEN_HEIGHT - 20)}
