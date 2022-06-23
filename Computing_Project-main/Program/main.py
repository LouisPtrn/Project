# ============================================================================================================== #
#                                             MAIN PROGRAM
# Written by: Louis Pattern     11/05/2022
# Known bugs: none
# ============================================================================================================== #

import pygame
from random import *
from sys import exit

pygame.init()
screen = pygame.display.set_mode((960, 600))
pygame.display.set_caption("Space shooter")
clock = pygame.time.Clock()
test_font = pygame.font.Font(None, 50)


star_surface = pygame.Surface((2, 2))
star_surface.fill("White")
test_surface = pygame.image.load("graphics/marisa.png")
play = True
gen = 1
screen.blit(test_surface, (350, 425))
text_surface = test_font.render("Sample text", False, "Red")

while play:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    if gen > 0:
        for k in range(50):
            i = randint(0, 960)
            j = randint(0, 600)
            screen.blit(star_surface, (i, j))
        gen -= 1
    else:
        screen.blit(text_surface, (350, 150))

    # Update everything
    pygame.display.update()
    clock.tick()  # Caps at 60 fps
