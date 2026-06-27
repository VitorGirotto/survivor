import pygame


class SpriteSheet:
    def __init__(self, filename: str) -> None:
        self.sprite_image = pygame.image.load(filename).convert_alpha()

    def get_sprite(self, frame):
        image = self.sprite_image.subsurface(pygame.Rect(frame))
        # sprite = pygame.Surface((frame[2], frame[3]))
        image.set_colorkey((0, 255, 0))
        image.blit(self.sprite_image, (0, 0), (x, y, w, h))
        return image

    # def parse_sprite(self, entity_sprite, action):
    #     sprite = entity_sprite[action]
    #     x, y, w, h = sprite["x"], sprite["y"], sprite["w"], sprite["h"]
    #     image = self.get_sprite(x, y, w, h)
    #     return image
