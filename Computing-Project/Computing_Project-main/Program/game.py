# ============================================================================================================== #
#                                             GAME PROGRAM
# Written by: Louis Pattern     13/07/2022
# Known bugs:  none
# ============================================================================================================== #

import pygame
from sys import exit
import random


class Player(pygame.sprite.Sprite):  # Spaceship class
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("graphics/ship1.png").convert_alpha()
        self.rect = self.image.get_rect(center=(200, 200))

    def player_input(self):  # Ship movement from input
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


class Lasers(pygame.sprite.Sprite):  # Weapons and projectile class
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("graphics/laser.png").convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))

    def shoot(self):
        self.rect.x += 24

    def delete(self):  # Deletes sprite when it goes off screen
        if self.rect.x > 1000:
            self.kill()

    def update(self):
        self.shoot()
        self.delete()


class Enemies(pygame.sprite.Sprite):  # Enemies and obstacles class
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("graphics/ast.png").convert_alpha()
        self.image.set_colorkey("white")
        self.rect = self.image.get_rect(center=(1000, random.randint(10, 590)))

    def move(self):
        self.rect.x -= 4

    def die(self):
        if self.rect.right < 1:
            self.kill()

    def update(self):
        self.move()
        self.die()


def play():
    pygame.init()
    screen = pygame.display.set_mode((960, 600))  # Game window
    pygame.display.set_caption("Space Game")
    clock = pygame.time.Clock()

    test_font = pygame.font.Font(None, 50)
    score = 0
    div_rect = pygame.Rect(-300, 290, 2000, 10)
    text_surface = test_font.render("SPACE GAME", True, (180, 10, 10))
    game_over = test_font.render("GAME OVER", True, (255, 0, 0))
    score_surface = test_font.render(str(score), True, (60, 60, 200)).convert_alpha()
    bg_surface = pygame.image.load("graphics/spacebg.png").convert_alpha()
    player = pygame.sprite.GroupSingle()
    player.add(Player())
    laser = pygame.sprite.Group()
    ast = pygame.sprite.Group()
    cooldown = 0
    game_active = True
    play1 = True

    while play1:  # Game loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        if game_active:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE] and cooldown < 1:  # Shooting input + max fire rate
                laser.add(Lasers(player.sprite.rect.centerx, player.sprite.rect.centery))
                cooldown = 20

            # Collision Detection
            if pygame.sprite.groupcollide(laser, ast, True, True):
                score += 100
            if pygame.sprite.spritecollide(player.sprite, ast, False):
                game_active = False

            if random.randint(0, 30) == 0:
                ast.add(Enemies())

            cooldown -= 1

            # Drawing non - sprites
            pygame.draw.rect(screen, "#FFFFFF", div_rect)
            screen.blit(bg_surface, (0, 0))
            screen.blit(text_surface, (360, 100))
            pygame.draw.rect(screen, "White", div_rect)
            screen.blit(score_surface, (450, 280))
            score_surface = test_font.render(str(score), True, (60, 60, 200)).convert_alpha()
            cooldown -= 1
            # Sprites drawing and updating
            laser.draw(screen)
            laser.update()
            ast.draw(screen)
            ast.update()
            player.draw(screen)
            player.update()

        else:
            # Game Over screen
            screen.fill("Black")
            screen.blit(game_over, (360, 250))
            screen.blit(score_surface, (400, 150))
            keys = pygame.key.get_pressed()
            score = 0
            laser.empty()  # Deletes all sprites on screen
            ast.empty()
            if keys[pygame.K_RETURN]:
                score = 0
                game_active = True
                player.sprite.rect.centery = 200  # Reset ship pos
                player.sprite.rect.centerx = 100

        # Update everything
        pygame.display.update()
        clock.tick(60)  # Caps at 60 fps


if __name__ == "__main__":
    play()
