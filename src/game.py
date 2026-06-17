import pygame

from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from player import Player


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.map_bg_image = pygame.image.load(
            "../assets/GAME_BACKGROUND.png"
        ).convert_alpha()
        self.rect = self.map_bg_image.get_rect(left=0, top=0)

        self.drawable: pygame.sprite.Group = pygame.sprite.Group()
        self.updatable: pygame.sprite.Group = pygame.sprite.Group()

        Player.containers = (self.drawable, self.updatable)

        player = Player("PLAYER_PLACEHOLDER", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    def run(self):
        pygame.time.Clock()
        clock = pygame.time.Clock()
        dt = 0.0

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

            self.screen.fill("purple")
            # self.screen.blit(source=self.map_bg_image, dest=self.rect)

            for obj in self.drawable:
                obj.draw(self.screen)

            pygame.display.flip()
            dt = clock.tick(60) / 1000
