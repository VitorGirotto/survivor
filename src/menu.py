import pygame

from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from button import Button
from entity import ASSETS_DIR
from game import Game


class Menu:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.bg_image = pygame.image.load(
            ASSETS_DIR / "adriano-bugnotto-background.jpg"
        ).convert_alpha()
        self.play_button_img = pygame.image.load(
            ASSETS_DIR / "play_button.png"
        ).convert_alpha()
        self.exit_button_img = pygame.image.load(
            ASSETS_DIR / "exit_button.png"
        ).convert_alpha()
        self.logo_img = pygame.image.load(ASSETS_DIR / "logo.png").convert_alpha()

        self.logo = Button(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 160, self.logo_img, 1)
        self.play_button = Button(
            SCREEN_WIDTH / 2 - 120, SCREEN_HEIGHT / 2 + 124, self.play_button_img, 1
        )
        # self.leaderboard_button = Button(
        #     SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 124, self.play_button_img, 1
        # )
        self.exit_button = Button(
            SCREEN_WIDTH / 2 + 120, SCREEN_HEIGHT / 2 + 124, self.exit_button_img, 1
        )
        self.rect = self.bg_image.get_rect(left=0, top=0)

    def run(self):
        while True:
            self.screen.fill("black")
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            self.screen.blit(source=self.bg_image, dest=self.rect)
            self.logo.draw(self.screen)
            if self.play_button.draw(self.screen):
                game = Game()
                game.run()
            # self.leaderboard_button.draw(self.screen)
            if self.exit_button.draw(self.screen):
                pygame.quit()
                quit()

            pygame.display.flip()
