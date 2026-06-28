import pygame

from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from enemy import Enemy
from enemySpawn import MapField
from entity import ASSETS_DIR
from player import Player
from shot import Shot


def format_elapsed_time(elapsed_time: float) -> str:
    total_seconds = int(elapsed_time)
    minutes = total_seconds // 60
    seconds = total_seconds % 60
    return f"{minutes:02}:{seconds:02}"


class Game:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.dt = 0.0
        self.elapsed_time = 0.0
        self.counter = 0
        self.score = 0
        self.timer_font = pygame.font.Font(None, 36)

        # self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.map_bg_image = pygame.image.load(
            ASSETS_DIR / "bg_game.png"
        ).convert_alpha()
        self.rect = self.map_bg_image.get_rect(left=0, top=0)

        self.drawable: pygame.sprite.Group = pygame.sprite.Group()
        self.updatable: pygame.sprite.Group = pygame.sprite.Group()
        self.enemies: pygame.sprite.Group = pygame.sprite.Group()

        Player.containers = (self.drawable, self.updatable)
        Enemy.containers = (self.drawable, self.updatable, self.enemies)
        MapField.containers = self.updatable
        Shot.containers = (self.drawable, self.updatable)

        self.player = Player(
            "PLAYER_PLACEHOLDER",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2,
            self.enemies,
            self.increase_score,
        )
        self.map_field = MapField(self.player, self.enemies)

    def increase_score(self, _enemy: pygame.sprite.Sprite) -> None:
        self.score += 1

    def draw_score(self) -> None:
        score_surf = self.timer_font.render(f"Score: {self.score}", True, "white")
        score_rect = score_surf.get_rect(topleft=(20, 20))
        self.screen.blit(score_surf, score_rect)

    def draw_background(self) -> None:
        self.screen.blit(self.map_bg_image, self.rect)

    def draw_timer(self) -> None:
        timer_text = format_elapsed_time(self.elapsed_time)
        timer_surf = self.timer_font.render(timer_text, True, "white")
        timer_rect = timer_surf.get_rect(topright=(SCREEN_WIDTH - 20, 20))
        self.screen.blit(timer_surf, timer_rect)

    def is_game_over(self) -> bool:
        return self.player.health <= 0

    def run(self):

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
            # for frame in PLAYER_SPRITES["walk_right"]:
            #     print(frame)
            # print(player_frames["walk_right"]["walk_right1"])
            self.elapsed_time += self.dt
            self.updatable.update(self.dt)
            if self.is_game_over():
                return

            self.draw_background()

            for obj in self.drawable:
                obj.draw(self.screen)
            self.draw_score()
            self.draw_timer()

            pygame.display.flip()
            self.dt = self.clock.tick(60) / 1000
