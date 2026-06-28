from sprite_sheet import Frame


PLAYER_IDLE: list[Frame] = [(24, 14, 16, 31)]

PLAYER_WALK_DOWN: list[Frame] = [
    (22, 270, 18, 33),
    (86, 269, 18, 33),
    (151, 269, 18, 33),
    (216, 269, 18, 33),
    (279, 269, 18, 33),
    (342, 269, 19, 33),
]

PLAYER_WALK_UP: list[Frame] = [
    (22, 333, 18, 33),
    (86, 333, 18, 33),
    (151, 333, 18, 33),
    (216, 333, 18, 33),
    (279, 333, 18, 33),
    (342, 333, 19, 33),
]

PLAYER_WALK_RIGHT: list[Frame] = [
    (23, 397, 18, 33),
    (88, 397, 18, 33),
    (152, 397, 18, 33),
    (216, 397, 18, 33),
    (279, 397, 18, 33),
    (342, 397, 19, 33),
]

PLAYER_WALK_LEFT: list[Frame] = [
    (23, 461, 18, 33),
    (86, 461, 18, 33),
    (150, 461, 18, 33),
    (214, 461, 18, 33),
    (279, 461, 18, 33),
    (343, 461, 19, 33),
]

PLAYER_ANIMATION_FRAMES: dict[str, list[Frame]] = {
    "idle": PLAYER_IDLE,
    "walk_up": PLAYER_WALK_UP,
    "walk_down": PLAYER_WALK_DOWN,
    "walk_left": PLAYER_WALK_LEFT,
    "walk_right": PLAYER_WALK_RIGHT,
}

ENEMY_WALK_RIGHT: list[Frame] = [
    (21, 209, 22, 24),
    (87, 209, 22, 24),
    (153, 209, 22, 24),
    (217, 209, 22, 24),
    (281, 208, 25, 25),
    (342, 208, 25, 25),
    (403, 214, 26, 20),
    (465, 213, 26, 20),
]

ENEMY_WALK_LEFT: list[Frame] = [
    (21, 145, 22, 24),
    (82, 145, 22, 24),
    (143, 145, 22, 24),
    (208, 144, 22, 24),
    (270, 145, 25, 25),
    (337, 144, 25, 25),
    (404, 152, 26, 20),
    (470, 152, 26, 20),
]

ENEMY_ANIMATION_FRAMES: dict[str, list[Frame]] = {
    "walk_right": ENEMY_WALK_RIGHT,
    "walk_left": ENEMY_WALK_LEFT,
}
