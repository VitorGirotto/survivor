from enum import Enum

import pygame

from sprite_sheet import SpriteSheet
from sprite_sheet import Frame


class Animation:
    class PlayMode(Enum):
        NORMAL = 1
        LOOP = 2

    def __init__(
        self,
        frames: list[pygame.Surface],
        frame_duration: float,
        mode: PlayMode = PlayMode.LOOP,
    ) -> None:
        if not frames:
            raise ValueError("Animation needs at least one frame")
        if frame_duration <= 0:
            raise ValueError("frame_duration must be greater than zero")

        self.frames = frames
        self.frame_duration = frame_duration
        self.animation_duration = len(self.frames) * self.frame_duration
        self.mode = mode
        self.elapsed_time = 0.0

    @classmethod
    def from_sprite_sheet(
        cls,
        sprite_sheet: SpriteSheet,
        frames: list[Frame] | tuple[Frame, ...],
        frame_duration: float,
        mode: PlayMode = PlayMode.LOOP,
        *,
        scale: float = 1,
        colorkey: pygame.Color | str | tuple[int, int, int] | None = None,
    ) -> "Animation":
        return cls(
            sprite_sheet.get_sprites(frames, scale=scale, colorkey=colorkey),
            frame_duration,
            mode,
        )

    def reset(self) -> None:
        self.elapsed_time = 0.0

    def update(self, dt: float) -> None:
        self.elapsed_time += dt

        if self.mode == self.PlayMode.LOOP:
            self.elapsed_time %= self.animation_duration
        else:
            self.elapsed_time = min(self.elapsed_time, self.animation_duration)

    def get_current_frame(self) -> pygame.Surface:
        frame_index = int(self.elapsed_time / self.frame_duration)
        frame_index = min(frame_index, len(self.frames) - 1)
        return self.frames[frame_index]

    @property
    def image(self) -> pygame.Surface:
        return self.get_current_frame()

    @property
    def is_finished(self) -> bool:
        return (
            self.mode == self.PlayMode.NORMAL
            and self.elapsed_time >= self.animation_duration
        )
