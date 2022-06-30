# ============================================================================================================== #
#                                             MAIN PROGRAM
# Written by: Louis Pattern     11/05/2022
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
# text_surface = test_font.render("Sample text", False, "Red")
ship_surface = pygame.image.load("graphics/ship1.png").convert_alpha()

bg_surface = pygame.image.load("graphics/spacebg.png").convert_alpha()
ship_x_pos = 200
ship_y_pos = 250

while play:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    screen.blit(bg_surface, (0, 0))

    ship_x_pos += 4
    if ship_x_pos > 1200:
        ship_x_pos = -200
    screen.blit(ship_surface, (ship_x_pos, ship_y_pos))

    # Update everything
    pygame.display.update()
    clock.tick(60)  # Caps at 60 fps