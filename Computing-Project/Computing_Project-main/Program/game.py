# ============================================================================================================== #
#                                             GAME PROGRAM
# Written by: Louis Pattern     11/07/2022
# Known bugs:     laser cannot be fired again until it reaches end of screen.
# ============================================================================================================== #

import pygame
from sys import exit
import random


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("graphics/ship1.png").convert_alpha()
        self.rect = self.image.get_rect(center=(200, 200))

    def player_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LSHIFT]:
            if keys[pygame.K_s] and self.rect.centery < 600:
                self.rect.centery += 3

            if keys[pygame.K_w] and self.rect.centery > 0:
                self.rect.centery -= 3

            if keys[pygame.K_d]:
                self.rect.centerx += 3

            if keys[pygame.K_a]:
                self.rect.centerx -= 3
        else:
            if keys[pygame.K_s] and self.rect.centery < 600:
                self.rect.centery += 6

            if keys[pygame.K_w] and self.rect.centery > 0:
                self.rect.centery -= 6

            if keys[pygame.K_d]:
                self.rect.centerx += 6

            if keys[pygame.K_a]:
                self.rect.centerx -= 6

        if self.rect.left > 960:
            self.rect.right = 0
        if self.rect.right < 0:
            self.rect.left = 960

    def update(self):
        self.player_input()


class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("graphics/laser.png").convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))

    def shoot(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.rect.centerx += 2

    def update(self):
        self.shoot()


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((960, 600))
        pygame.display.set_caption("Space Game")
        self.clock = pygame.time.Clock()
        self.test_font = pygame.font.Font(None, 50)
        self.play1 = True
        self.score = 0
        self.div_rect = pygame.Rect(-300, 290, 2000, 10)
        self.text_surface = self.test_font.render("SPACE GAME", True, (180, 10, 10))
        self.game_over = self.test_font.render("GAME OVER", True, (255, 0, 0))
        self.score_surface = self.test_font.render(str(self.score), True, (60, 60, 200))
        self.ast_surface = pygame.image.load("graphics/ast.png")
        self.ast_surface.set_colorkey("white")
        self.ast_surface = self.ast_surface.convert_alpha()
        self.ast_rect = self.ast_surface.get_rect(center=(1000, 200))
        self.laser_surface = pygame.image.load("graphics/laser.png").convert_alpha()
        self.laser_rect = self.laser_surface.get_rect(center=(0, 0))
        self.bg_surface = pygame.image.load("graphics/spacebg.png").convert_alpha()
        # inv_frames = 0
        self.shoot = False
        self.game_active = True

        self.player = pygame.sprite.GroupSingle()
        self.player.add(Player())

        # self.lasers = pygame.sprite.Group()
        # self.lasers.add(Lasers())

        # Timer
        self.timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.timer, 1000)

    def play(self):
        while self.play1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                # if event.type == timer and game_active:
                #     obstacle_rect_list.append(ast_surface.get_rect(center=(random.randint(0, 1000),
                #                                                            random.randint(0, 1000))))

                # if event.type == pygame.KEYDOWN:
                #     if event.key == pygame.K_s:
                #         print("move")
                # if event.type == pygame.KEYUP:
                #      print("No")

            # screen.blit(ship_surface, (ship_x_pos, ship_y_pos))

            if self.game_active:

                self.ast_rect.left += -3
                if self.ast_rect.left < -200:
                    self.ast_rect.left = 1100

                # Enemies movement

                # if self.player.rect.colliderect(self.ast_rect):
                #     self.game_active = False
                #
                # if self.laser_rect.colliderect(self.ast_rect):
                #     self.score += 100
                #     self.ast_rect.left = 1200
                #     self.ast_rect.centery = random.randint(0, 500)
                #
                # if not self.shoot:
                #     self.laser_rect.centerx = self.ship_rect.centerx
                #     self.laser_rect.centery = self.ship_rect.centery

                keys = pygame.key.get_pressed()

                #
                # if self.shoot:
                #     self.laser_rect.centerx += 10
                #
                # if self.laser_rect.left > 960:
                #     self.shoot = False

                pygame.draw.rect(self.screen, "#FFFFFF", self.div_rect)
                self.screen.blit(self.bg_surface, (0, 0))
                self.screen.blit(self.text_surface, (360, 100))
                pygame.draw.rect(self.screen, "White", self.div_rect)
                self.screen.blit(self.score_surface, (450, 280))
                self.screen.blit(self.laser_surface, self.laser_rect)
                # self.screen.blit(self.ship_surface, self.ship_rect)
                self.player.draw(self.screen)
                self.player.update()

                # self.lasers.draw(self.screen)
                # self.lasers.update()

                self.screen.blit(self.ast_surface, self.ast_rect)
                self.score_surface = self.test_font.render(str(self.score), True, (60, 60, 200))

            else:
                self.screen.fill("Black")
                self.screen.blit(self.game_over, (360, 250))
                self.screen.blit(self.score_surface, (440, 150))
                keys = pygame.key.get_pressed()
                self.score = 0
                if keys[pygame.K_SPACE]:
                    self.player.centerx = 100
                    self.player.centery = 300
                    self.ast_rect.centerx = 1000
                    self.ast_rect.centery = random.randint(200, 700)
                    self.score = 0
                    self.game_active = True

            # Update everything
            pygame.display.update()
            self.clock.tick(60)  # Caps at 60 fps


if __name__ == "__main__":
    SpaceGame = Game()
    while True:
        SpaceGame.play()
