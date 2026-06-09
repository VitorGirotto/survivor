import pygame

from constants import SCREEN_WIDTH, SCREEN_HEIGHT


class Menu:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.bg_image = pygame.image.load(
            "../assets/adriano-bugnotto-background.jpg"
        ).convert_alpha()
        self.rect = self.bg_image.get_rect(left=0, top=0)

    def run(self):
        while True:
            self.screen.fill("black")
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            self.screen.blit(source=self.bg_image, dest=self.rect)

            pygame.display.flip()
