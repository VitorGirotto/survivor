import pygame
from pygame.display import update

from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from enemy import Enemy
import enemy
from player import Player


class Game:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.dt = 0.0

        # self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.map_bg_image = pygame.image.load(
            "../assets/GAME_BACKGROUND.png"
        ).convert_alpha()
        self.rect = self.map_bg_image.get_rect(left=0, top=0)

        self.drawable: pygame.sprite.Group = pygame.sprite.Group()
        self.updatable: pygame.sprite.Group = pygame.sprite.Group()
        self.enemies: pygame.sprite.Group = pygame.sprite.Group()

        Player.containers = (self.drawable, self.updatable)
        Enemy.containers = (self.drawable, self.updatable)

        player = Player("PLAYER_PLACEHOLDER", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        enemy = Enemy("ENEMY_PLACEHOLDER", 50, 100, player)

    def run(self):

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

            self.updatable.update(self.dt)

            self.screen.fill("purple")
            # self.screen.blit(source=self.map_bg_image, dest=self.rect)
            # print(pygame.sprite.Group.sprites(self.updatable))
            # print(pygame.sprite.Sprite.groups(player))

            for obj in self.drawable:
                obj.draw(self.screen)

            pygame.display.flip()
            self.dt = self.clock.tick(60) / 1000
