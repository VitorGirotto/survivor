import pygame
from enum import Enum

from sprite_sheet import SpriteSheet


class Animation:
    class PlayMode(Enum):
        NORMAL = (1,)
        LOOP = 2

    def __init__(self, frames, frame_duration, mode) -> None:
        self.frames = frames
        self.frame_duration = frame_duration
        self.animation_duration = len(self.frames) * self.frame_duration
        self.mode = mode

    def parse_sprite(self, entity_sprite, action):
        for frame in entity_sprite[action]:
            sprite = entity_sprite[action][frame]
            x, y, w, h = sprite["x"], sprite["y"], sprite["w"], sprite["h"]
            image = self.sprite_sheet.get_sprite(x, y, w, h)
            return image
