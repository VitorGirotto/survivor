from sprite_sheet import Frame


PLAYER_IDLE: list[Frame] = [(24, 14, 16, 31)]

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
    "walk_left": PLAYER_WALK_LEFT,
    "walk_right": PLAYER_WALK_RIGHT,
}
