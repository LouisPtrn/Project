# ============================================================================================================== #
# File used for editing colours on images
# Written by: Louis Pattern     15/09/2022
# Known bugs:  none
# ============================================================================================================== #

import pygame


def change_hue(image, n):
    pixels = pygame.PixelArray(image)
    for x in range(image.get_width()):
        for y in range(image.get_height()):
            rgb = image.unmap_rgb(pixels[x][y])
            color = pygame.Color(*rgb)
            h, s, l, a = color.hsla
            color.hsla = (int(h) + n) % 360, int(s), int(l), int(a)
            pixels[x][y] = color
    del pixels
