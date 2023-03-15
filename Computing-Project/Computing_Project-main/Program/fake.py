from sys import exit
from validation import *
import pygame
import random
import os

def is_inrange(data, lo, hi):
    try:
        if (len(data) >= lo) and (len(data) <= hi):
            return True
        return False
    except TypeError:
        return "Error"

def is_length(data, length, opt):
    try:
        if opt == 1:
            if len(data) == length:
                return True
            return False
        elif opt == 2:
            if len(data) >= length:
                return True
            return False
        elif opt == 3:
            if len(data) <= length:
                return True
            return False
    except Exception as ex:
        return ex

def is_valid_user(u, opt):
    if opt == "username":
        if isinstance(u, str):
            if is_inrange(u, 3, 20):
                u = u.upper()
                characters = []
                for i in range(65, 91):
                    characters.append(chr(i))
                for i in range(48, 58):
                    characters.append(chr(i))
                characters.append("_")
                valid = True
                for n in range(len(u)):
                    if not u[n] in characters:
                        valid = False
            else:
                valid = False
        else:
            valid = False
    else:
        valid = False
        if isinstance(u, str) and is_inrange(u, 8, 255):
            valid = True
    return valid




# Spaceship class controlled by the user
class Player(pygame.sprite.Sprite):
    def __init__(self, wd, ht):
        super().__init__()
        self.wd = wd
        self.ht = ht
        self.image_sprite = pygame.image.load("graphics/ship1.png")
        self.image = pygame.transform.scale(self.image_sprite, (wd/11, ht/11))
        self.position = pygame.math.Vector2(0, 0)
        self.rect = self.image.get_rect()

    def player_input(self):  # Ship movement from input
        keys = pygame.key.get_pressed()
        dx = keys[pygame.K_d] - keys[pygame.K_a]
        dy = keys[pygame.K_s] - keys[pygame.K_w]
        self.direction = pygame.math.Vector2(dx, dy)
        # Accounting for diagonal speed by dividing by root 2
        if dx != 0 and dy != 0:
            self.direction /= 1.41421

        # Focus active when shift is held
        if keys[pygame.K_LSHIFT]:
            self.position += self.direction * 4
        else:
            self.position += self.direction * 8

        # Set rect position to position vector
        self.rect.x = round(self.position.x)
        self.rect.y = round(self.position.y)

        if self.rect.left > self.wd:
            self.rect.right = 0
        if self.rect.right < 0:
            self.rect.left = self.wd

        if self.rect.left > self.wd:
            self.rect.right = 0
        if self.rect.right < 0:
            self.rect.left = self.wd

    # def take_dmg1(self):
    #     self.image = pygame.transform.scale(self.image_sprite, (self.wd/11, self.ht/11))
    #
    # def take_dmg2(self):
    #     self.image = pygame.transform.scale(self.image_inv, (self.wd/11, self.ht/11))

    # def death_check(self, li):
    #     if li <= 0:
    #         self.take_dmg2()

    def update(self):
        self.player_input()


class Lasers(pygame.sprite.Sprite):
    def __init__(self, x, y, wd, ht):
        super().__init__()
        self.wd = wd
        self.ht = ht
        self.surface = pygame.image.load("graphics/laser.png").convert_alpha()
        self.image = pygame.transform.scale(self.surface, (wd / 40, ht / 160))
        self.rect = self.image.get_rect(center=(x, y))

    def shoot(self):
        self.rect.x += self.wd/40

    def delete(self):  # Deletes sprite when it goes off-screen
        if self.rect.right > self.wd or self.rect.right < 0:
            self.kill()

    def update(self):
        self.shoot()
        self.delete()


class Alien(pygame.sprite.Sprite):
    def __init__(self, wd, ht, alien_type):
        super().__init__()
        self.type = alien_type
        self.wd = wd
        self.ht = ht

        if alien_type == "normal":
            self.lives = 3
            self.surface = pygame.image.load("graphics/alien1.png") #.convert_alpha()
            self.image = pygame.transform.scale(self.surface, (wd / 12, ht / 9))
            self.rect = self.image.get_rect(center=(wd*1.1, random.uniform(ht*0.1, ht*0.9)))

    def move(self):
        if self.type == "normal":
            self.rect.centerx -= self.wd / 500

    def update(self, timer):
        self.move()

        # Alien death when it goes off-screen or when it's health is 0
        if self.rect.centerx < 1 or self.lives <= 0:
            self.kill()


def play():
    width = 960
    height = 540
    play_game = True
    game_timer = 3600
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Space Game")
    clock = pygame.time.Clock()
    player = pygame.sprite.GroupSingle()
    player.add(Player(width, height))
    laser = pygame.sprite.Group()
    aliens = pygame.sprite.Group()
    cooldown = 0

    while play_game:  # Game loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE] and cooldown < 1:  # Shooting input + max fire rate
            laser.add(Lasers(player.sprite.rect.centerx, player.sprite.rect.centery, width, height))
            cooldown = 10
        cooldown -= 1

        if game_timer % 200 == 0:  # Adding aliens
            aliens.add(Alien(width, height, "normal"))

        # Alien hit detection
        for n in laser:
            for alien in aliens:
                if pygame.sprite.collide_rect(n, alien):
                    n.kill()
                    alien.__setattr__("lives", alien.__getattribute__("lives") - 1)

        game_timer -= 1
        # Update everything
        screen.fill("black")
        player.draw(screen)
        laser.draw(screen)
        aliens.update(game_timer)

        aliens.draw(screen)
        player.update()
        laser.update()
        pygame.display.update()
        clock.tick(60)  # Caps at 60 fps


if __name__ == "__main__":
    play()


#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------