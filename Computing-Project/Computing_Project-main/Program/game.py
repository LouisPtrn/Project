# ============================================================================================================== #
#                                             GAME PROGRAM
# Written by: Louis Pattern     11/07/2022
# Known bugs:  none
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


class Lasers(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("graphics/laser.png").convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))

    def shoot(self):
        self.rect.x += 24

    def delete(self):
        if self.rect.x > 1000 or not game_active:
            self.kill()

    def update(self):
        global lrect
        self.shoot()
        self.delete()
        lrect = self.rect


class Enemies(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("graphics/ast.png").convert_alpha()
        self.image.set_colorkey("white")
        self.rect = self.image.get_rect(center=(1000, random.randint(10, 590)))

    def move(self):
        self.rect.x -= 4

    def die(self):
        if self.rect.right < 1 or not game_active:
            self.kill()

    def hit_player(self):
        global game_active
        if self.rect.colliderect(player.sprite.rect):
            game_active = False

    def update(self):
        self.move()
        self.hit_player()
        self.die()


def play():
    global game_active
    global player
    global laser
    pygame.init()
    screen = pygame.display.set_mode((960, 600))
    pygame.display.set_caption("Space Game")
    clock = pygame.time.Clock()
    test_font = pygame.font.Font(None, 50)
    play1 = True
    score = 0
    div_rect = pygame.Rect(-300, 290, 2000, 10)
    text_surface = test_font.render("SPACE GAME", True, (180, 10, 10))
    game_over = test_font.render("GAME OVER", True, (255, 0, 0))
    score_surface = test_font.render(str(score), True, (60, 60, 200))
    bg_surface = pygame.image.load("graphics/spacebg.png").convert_alpha()
    game_active = True
    player = pygame.sprite.GroupSingle()
    player.add(Player())
    laser = pygame.sprite.Group()
    ast = pygame.sprite.Group()
    cooldown = 0

    while play1:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        if pygame.sprite.groupcollide(laser, ast, True, True):
            score += 100

        if game_active:
            if random.randint(0, 30) == 0:
                ast.add(Enemies())


            keys = pygame.key.get_pressed()

            if keys[pygame.K_SPACE] and cooldown < 1:
                laser.add(Lasers(player.sprite.rect.centerx, player.sprite.rect.centery))
                cooldown = 16

            pygame.draw.rect(screen, "#FFFFFF", div_rect)
            screen.blit(bg_surface, (0, 0))
            screen.blit(text_surface, (360, 100))
            pygame.draw.rect(screen, "White", div_rect)
            screen.blit(score_surface, (450, 280))
            score_surface = test_font.render(str(score), True, (60, 60, 200))

            laser.draw(screen)
            laser.update()
            ast.draw(screen)
            ast.update()
            player.draw(screen)
            player.update()
            cooldown -= 1
        else:
            screen.fill("Black")
            screen.blit(game_over, (360, 250))
            screen.blit(score_surface, (400, 150))
            keys = pygame.key.get_pressed()
            score = 0
            if keys[pygame.K_RETURN]:
                score = 0
                game_active = True
                player.sprite.rect.centery = 200
                player.sprite.rect.centerx = 100


        # Update everything
        pygame.display.update()
        clock.tick(60)  # Caps at 60 fps


if __name__ == "__main__":
    play()
