# pygame test

import pygame
from random import *
from sys import exit

pygame.init()
w = 1200
h = 700
screen = pygame.display.set_mode((w, h))
pygame.display.set_caption("Totally awesome cool computer science project that will get A*")
clock = pygame.time.Clock()
dvd = pygame.image.load("graphics/dvd4.jpg")

trail = pygame.Surface((5, 5))
trail.fill("Red")
trail2 = pygame.Surface((5, 5))
trail2.fill("Blue")
trail3 = pygame.Surface((5, 5))
trail3.fill("Green")
trail4 = pygame.Surface((5, 5))
trail4.fill("Yellow")

x = randint(100, w)
y = randint(100, h)

right = True
up = True


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    screen.blit(dvd, (x, y))

    # if up and right:
    #     screen.blit(trail, (x-20, y+100))
    #
    # if up and not right:
    #     screen.blit(trail2, (x+150, y+120))
    #
    # if not up and right:
    #     screen.blit(trail3, (x-20, y-20))
    #
    # if not up and not right:
    #     screen.blit(trail4, (x+150, y-20))

    if x > w-130:
        right = False
    if x < 0:
        right = True

    if y > h-100:
        up = True
    if y < 0:
        up = False

    if up:
        y -= 1
    else:
        y += 1
    if right:
        x += 1
    else:
        x -= 1

    pygame.display.update()
    clock.tick(120)
