# ============================================================================================================== #
#                                             MAIN PROGRAM
# Written by: Louis Pattern     01/07/2022
# Known bugs:     laser cannot be fired again until it reaches end of screen.
# ============================================================================================================== #

import pygame
from sys import exit
import random


def play():
    pygame.init()
    screen = pygame.display.set_mode((960, 600))
    pygame.display.set_caption("Space Game")
    clock = pygame.time.Clock()
    test_font = pygame.font.Font(None, 50)

    star_surface = pygame.Surface((2, 2))
    star_surface.fill("White")
    test_surface = pygame.image.load("graphics/marisa.png").convert_alpha()
    play1 = True
    gen = 1
    score = 0
    screen.blit(test_surface, (350, 425))
    div_rect = pygame.Rect(-300, 290, 2000, 10)
    text_surface = test_font.render("SPACE GAME", True, (180, 10, 10))
    game_over = test_font.render("GAME OVER", True, (255, 0, 0))
    score_surface = test_font.render(str(score), True, (60, 60, 200))
    ship_surface = pygame.image.load("graphics/ship1.png").convert_alpha()
    ship_rect = ship_surface.get_rect(center=(200, 200))
    ast_surface = pygame.image.load("graphics/ast.png")
    ast_surface.set_colorkey("white")
    ast_surface = ast_surface.convert_alpha()
    ast_rect = ast_surface.get_rect(center=(1000, 200))
    laser_surface = pygame.image.load("graphics/laser.png").convert_alpha()
    laser_rect = laser_surface.get_rect(center=(0, 0))
    bg_surface = pygame.image.load("graphics/spacebg.png").convert_alpha()
    # inv_frames = 0
    shoot = False
    game_active = True

    while play1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            # if event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_s:
            #         print("move")
            # if event.type == pygame.KEYUP:
            #      print("No")

        # screen.blit(ship_surface, (ship_x_pos, ship_y_pos))

        if game_active:
            if ship_rect.left > 960:
                ship_rect.left = 0
            if ship_rect.right < 0:
                ship_rect.right = 960

            ast_rect.left += -3
            if ast_rect.left < -200:
                ast_rect.left = 1100

            if ship_rect.colliderect(ast_rect):
                game_active = False

            if laser_rect.colliderect(ast_rect):
                score += 100
                ast_rect.left = 1200
                ast_rect.centery = random.randint(0, 500)

            if not shoot:
                laser_rect.centerx = ship_rect.centerx
                laser_rect.centery = ship_rect.centery

            keys = pygame.key.get_pressed()

            if keys[pygame.K_s]:
                if keys[pygame.K_LSHIFT]:
                    ship_rect.centery += 3
                else:
                    ship_rect.centery += 6
            if keys[pygame.K_w]:
                if keys[pygame.K_LSHIFT]:
                    ship_rect.centery -= 3
                else:
                    ship_rect.centery -= 6
            if keys[pygame.K_d]:
                if keys[pygame.K_LSHIFT]:
                    ship_rect.centerx += 3
                else:
                    ship_rect.centerx += 6
            if keys[pygame.K_a]:
                if keys[pygame.K_LSHIFT]:
                    ship_rect.centerx -= 3
                else:
                    ship_rect.centerx -= 6
            if keys[pygame.K_SPACE]:
                shoot = True

            if shoot:
                laser_rect.centerx += 10

            if laser_rect.left > 960:
                shoot = False

            if ship_rect.top <= 0:
                ship_rect.top = 0

            if ship_rect.bottom >= 600:
                ship_rect.bottom = 600

            pygame.draw.rect(screen, "#FFFFFF", div_rect)
            screen.blit(bg_surface, (0, 0))
            screen.blit(text_surface, (360, 100))
            pygame.draw.rect(screen, "White", div_rect)
            screen.blit(score_surface, (450, 280))
            screen.blit(laser_surface, laser_rect)
            screen.blit(ship_surface, ship_rect)
            screen.blit(ast_surface, ast_rect)
            score_surface = test_font.render(str(score), True, (60, 60, 200))
        else:
            screen.fill("Black")
            screen.blit(game_over, (360, 250))
            screen.blit(score_surface, (400, 150))
            keys = pygame.key.get_pressed()
            score = 0
            if keys[pygame.K_SPACE]:
                ship_rect.centerx = 100
                ship_rect.centery = 300
                ast_rect.centerx = 1000
                score = 0
                game_active = True

        # Update everything
        pygame.display.update()
        clock.tick(60)  # Caps at 60 fps


if __name__ == "__main__":
    play()
