import pygame

from constants import SCREEN_HEIGHT, SCREEN_WIDTH


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    def run(self):
        pygame.time.Clock()
        clock = pygame.time.Clock()
        dt = 0

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

        self.screen.fill("purple")

        pygame.display.flip()
        clock.tick(60)

    # if __name__ == "__main__":
    #     main()
