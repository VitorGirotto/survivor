from sprite_sheet import Frame


PLAYER_IDLE: list[Frame] = [(0, 0, 64, 64)]

PLAYER_WALK_RIGHT: list[Frame] = [
    (0, 384, 64, 64),
    (64, 384, 64, 64),
    (128, 384, 64, 64),
    (192, 384, 64, 64),
    (256, 384, 64, 64),
    (320, 384, 64, 64),
]

PLAYER_WALK_LEFT: list[Frame] = [
    (0, 448, 64, 64),
    (64, 448, 64, 64),
    (128, 448, 64, 64),
    (192, 448, 64, 64),
    (256, 448, 64, 64),
    (320, 448, 64, 64),
]

PLAYER_ANIMATION_FRAMES: dict[str, list[Frame]] = {
    "idle": PLAYER_IDLE,
    "walk_left": PLAYER_WALK_LEFT,
    "walk_right": PLAYER_WALK_RIGHT,
}
