# ============================================================================================================== #
#                                             MAIN PROGRAM
# Written by: Louis Pattern     01/07/2022
# Known bugs: none
# ============================================================================================================== #

import pygame
from sys import exit

pygame.init()
screen = pygame.display.set_mode((960, 600))
pygame.display.set_caption("Space Game")
clock = pygame.time.Clock()
test_font = pygame.font.Font(None, 50)


star_surface = pygame.Surface((2, 2))
star_surface.fill("White")
test_surface = pygame.image.load("graphics/marisa.png").convert_alpha()
play = True
gen = 1
screen.blit(test_surface, (350, 425))
div_rect = pygame.Rect(-300, 290, 2000, 10)
text_surface = test_font.render("SPACE GAME", True, (180, 10, 10))
ship_surface = pygame.image.load("graphics/ship1.png").convert_alpha()
ship_rect = ship_surface.get_rect(center=(200, 200))
ast_surface = pygame.image.load("graphics/ast.png")
ast_surface.set_colorkey("white")
ast_surface = ast_surface.convert_alpha()
ast_rect = ast_surface.get_rect(center=(1000, 200))
bg_surface = pygame.image.load("graphics/spacebg.png").convert_alpha()
# inv_frames = 0


while play:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        # if event.type == pygame.KEYDOWN:
        #     if event.key == pygame.K_s:
        #         print("move")
        # if event.type == pygame.KEYUP:
        #      print("No")

    screen.blit(bg_surface, (0, 0))
    screen.blit(text_surface, (360, 100))
    pygame.draw.rect(screen, "White", div_rect)
    # screen.blit(ship_surface, (ship_x_pos, ship_y_pos))
    ship_rect.right += 8
    if ship_rect.right > 1100:
        ship_rect.right = 100
    screen.blit(ship_surface, ship_rect)

    ast_rect.left += -3
    if ast_rect.left < -200:
        ast_rect.left = 1100
    screen.blit(ast_surface, ast_rect)

    pygame.draw.rect(screen, "#FFFFFF", div_rect)

    if ship_rect.colliderect(ast_rect):  # and inv_frames == 0:
        ship_rect.right = -600
        # inv_frames = 100
    # if inv_frames > 0:
    #     inv_frames -= 1

    keys = pygame.key.get_pressed()
    if keys[pygame.K_s]:
        ship_rect.centery += 5
    if keys[pygame.K_w]:
        ship_rect.centery -= 5

    # Update everything
    pygame.display.update()
    clock.tick(60)  # Caps at 60 fps
