# ============================================================================================================== #
# SPRITES AND CLASSES FILE
# Written by: Louis Pattern     30/08/2022
# Known bugs: none
# ============================================================================================================== #

from pygame import mixer
import random
from colour_changer import *
from settings import *


class Background(pygame.sprite.Sprite):
    def __init__(self, width, height, level):
        super().__init__()
        if level == 1:
            surface = pygame.image.load("graphics/bg.png").convert_alpha()
        else:
            surface = pygame.image.load("graphics/bg2.jpg").convert_alpha()

        self.image = pygame.transform.scale(surface, (width*20, height))

        self.rect = self.image.get_rect(center=(width*10, height/2))

    def scroll(self, wd):
        self.rect.centerx -= wd*0.008
        if self.rect.right <= wd:
            self.rect.centerx = wd*10

    def update(self, width):
        self.scroll(width)


# Spaceship class controlled by the user
class Player(pygame.sprite.Sprite):
    def __init__(self, wd, ht):
        super().__init__()
        self.wd = wd
        self.ht = ht
        self.image_sprite = pygame.image.load("graphics/ship1.png")
        self.image_inv = pygame.image.load("graphics/shipInv.png")
        self.image = pygame.transform.scale(self.image_sprite, (wd/11, ht/11))
        self.rect = self.image.get_rect(center=(wd/10, ht/4))

    def player_input(self):  # Ship movement from input
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LSHIFT]:
            if keys[pygame.K_s] and self.rect.centery < self.ht and not keys[pygame.K_w]:
                if keys[pygame.K_a]:
                    self.rect.centery += ((self.ht / (100))/1.414)*0.5
                    self.rect.centerx -= ((self.wd / (178))/1.414)*0.5
                elif keys[pygame.K_d]:
                    self.rect.centery += ((self.ht / (100))/1.414)*0.5
                    self.rect.centerx += ((self.wd / (178))/1.414)*0.5
                else:
                    self.rect.centery += self.ht/100*0.5

            elif keys[pygame.K_w] and self.rect.centery > 0 and not keys[pygame.K_s]:
                if keys[pygame.K_a]:
                    self.rect.centery -= ((self.ht / (100))/1.414)*0.5
                    self.rect.centerx -= ((self.wd / (178))/1.414)*0.5
                elif keys[pygame.K_d]:
                    self.rect.centery -= ((self.ht / (100))/1.414)*0.5
                    self.rect.centerx += ((self.wd / (178))/1.414)*0.5
                else:
                    self.rect.centery -= self.ht/100*0.5

            elif keys[pygame.K_d] and not keys[pygame.K_a]:
                self.rect.centerx += self.wd/178

            elif keys[pygame.K_a] and not keys[pygame.K_d]:
                self.rect.centerx -= self.wd/178
        else:
            if keys[pygame.K_s] and self.rect.centery < self.ht and not keys[pygame.K_w]:
                if keys[pygame.K_a]:
                    self.rect.centery += (self.ht / (100))/1.414
                    self.rect.centerx -= (self.wd / (178))/1.414
                elif keys[pygame.K_d]:
                    self.rect.centery += (self.ht / (100))/1.414
                    self.rect.centerx += (self.wd / (178))/1.414
                else:
                    self.rect.centery += self.ht/100

            elif keys[pygame.K_w] and self.rect.centery > 0 and not keys[pygame.K_s]:
                if keys[pygame.K_a]:
                    self.rect.centery -= (self.ht / (100))/1.414
                    self.rect.centerx -= (self.wd / (178))/1.414
                elif keys[pygame.K_d]:
                    self.rect.centery -= (self.ht / (100))/1.414
                    self.rect.centerx += (self.wd / (178))/1.414
                else:
                    self.rect.centery -= self.ht/100

            elif keys[pygame.K_d] and not keys[pygame.K_a]:
                self.rect.centerx += self.wd/178

            elif keys[pygame.K_a] and not keys[pygame.K_d]:
                self.rect.centerx -= self.wd/178

        if self.rect.left > self.wd:
            self.rect.right = 0
        if self.rect.right < 0:
            self.rect.left = self.wd

    def take_dmg1(self):
        self.image = pygame.transform.scale(self.image_sprite, (self.wd/11, self.ht/11))

    def take_dmg2(self):
        self.image = pygame.transform.scale(self.image_inv, (self.wd/11, self.ht/11))

    def death_check(self, li):
        if li <= 0:
            self.take_dmg2()

    def update(self, lives):
        self.player_input()
        self.death_check(lives)


class PlayerA(Player):
    def player_input(self):  # Altered movement for versus
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LSHIFT]:
            if keys[pygame.K_s] and self.rect.centery < self.ht/2.25 and not keys[pygame.K_w]:
                if keys[pygame.K_a]:
                    self.rect.centery += ((self.ht / (100)) / 1.414) * 0.5
                    self.rect.centerx -= ((self.wd / (178)) / 1.414) * 0.5
                elif keys[pygame.K_d]:
                    self.rect.centery += ((self.ht / (100)) / 1.414) * 0.5
                    self.rect.centerx += ((self.wd / (178)) / 1.414) * 0.5
                else:
                    self.rect.centery += self.ht / 100 * 0.5

            elif keys[pygame.K_w] and self.rect.centery > 0 and not keys[pygame.K_s]:
                if keys[pygame.K_a]:
                    self.rect.centery -= ((self.ht / (100)) / 1.414) * 0.5
                    self.rect.centerx -= ((self.wd / (178)) / 1.414) * 0.5
                elif keys[pygame.K_d]:
                    self.rect.centery -= ((self.ht / (100)) / 1.414) * 0.5
                    self.rect.centerx += ((self.wd / (178)) / 1.414) * 0.5
                else:
                    self.rect.centery -= self.ht / 100 * 0.5

            elif keys[pygame.K_d] and not keys[pygame.K_a]:
                self.rect.centerx += self.wd / 178

            elif keys[pygame.K_a] and not keys[pygame.K_d]:
                self.rect.centerx -= self.wd / 178
        else:
            if keys[pygame.K_s] and self.rect.centery < self.ht/2.25 and not keys[pygame.K_w]:
                if keys[pygame.K_a]:
                    self.rect.centery += (self.ht / (100)) / 1.414
                    self.rect.centerx -= (self.wd / (178)) / 1.414
                elif keys[pygame.K_d]:
                    self.rect.centery += (self.ht / (100)) / 1.414
                    self.rect.centerx += (self.wd / (178)) / 1.414
                else:
                    self.rect.centery += self.ht / 100

            elif keys[pygame.K_w] and self.rect.centery > 0 and not keys[pygame.K_s]:
                if keys[pygame.K_a]:
                    self.rect.centery -= (self.ht / (100)) / 1.414
                    self.rect.centerx -= (self.wd / (178)) / 1.414
                elif keys[pygame.K_d]:
                    self.rect.centery -= (self.ht / (100)) / 1.414
                    self.rect.centerx += (self.wd / (178)) / 1.414
                else:
                    self.rect.centery -= self.ht / 100

            elif keys[pygame.K_d] and not keys[pygame.K_a]:
                self.rect.centerx += self.wd / 178

            elif keys[pygame.K_a] and not keys[pygame.K_d]:
                self.rect.centerx -= self.wd / 178

        if self.rect.left > self.wd:
            self.rect.right = 0
        if self.rect.right < 0:
            self.rect.left = self.wd


class PlayerB(pygame.sprite.Sprite):  # 2nd ship for versus
    def __init__(self, wd, ht):
        super().__init__()
        self.wd = wd
        self.ht = ht
        self.image_sprite = pygame.image.load("graphics/ship1b.png")
        self.image_inv = pygame.image.load("graphics/shipInv.png")
        self.image = pygame.transform.scale(self.image_sprite, (wd / 11, ht / 11))
        self.rect = self.image.get_rect(center=(wd / 10, ht / 1.25))

    def player_input(self):  # Player 2 input
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RCTRL]:
            if keys[pygame.K_DOWN] and self.rect.centery < 0 and not keys[pygame.K_UP]:
                if keys[pygame.K_LEFT]:
                    self.rect.centery += ((self.ht / (100)) / 1.414) * 0.5
                    self.rect.centerx -= ((self.wd / (178)) / 1.414) * 0.5
                elif keys[pygame.K_RIGHT]:
                    self.rect.centery += ((self.ht / (100)) / 1.414) * 0.5
                    self.rect.centerx += ((self.wd / (178)) / 1.414) * 0.5
                else:
                    self.rect.centery += self.ht / 100 * 0.5

            elif keys[pygame.K_UP] and self.rect.centery > self.ht/1.85 and not keys[pygame.K_DOWN]:
                if keys[pygame.K_LEFT]:
                    self.rect.centery -= ((self.ht / (100)) / 1.414) * 0.5
                    self.rect.centerx -= ((self.wd / (178)) / 1.414) * 0.5
                elif keys[pygame.K_RIGHT]:
                    self.rect.centery -= ((self.ht / (100)) / 1.414) * 0.5
                    self.rect.centerx += ((self.wd / (178)) / 1.414) * 0.5
                else:
                    self.rect.centery -= self.ht / 100 * 0.5

            elif keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT]:
                self.rect.centerx += self.wd / 178

            elif keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
                self.rect.centerx -= self.wd / 178
        else:
            if keys[pygame.K_DOWN] and self.rect.centery < self.ht and not keys[pygame.K_UP]:
                if keys[pygame.K_LEFT]:
                    self.rect.centery += (self.ht / (100)) / 1.414
                    self.rect.centerx -= (self.wd / (178)) / 1.414
                elif keys[pygame.K_RIGHT]:
                    self.rect.centery += (self.ht / (100)) / 1.414
                    self.rect.centerx += (self.wd / (178)) / 1.414
                else:
                    self.rect.centery += self.ht / 100

            elif keys[pygame.K_UP] and self.rect.centery > self.ht/1.85 and not keys[pygame.K_DOWN]:
                if keys[pygame.K_LEFT]:
                    self.rect.centery -= (self.ht / (100)) / 1.414
                    self.rect.centerx -= (self.wd / (178)) / 1.414
                elif keys[pygame.K_RIGHT]:
                    self.rect.centery -= (self.ht / (100)) / 1.414
                    self.rect.centerx += (self.wd / (178)) / 1.414
                else:
                    self.rect.centery -= self.ht / 100

            elif keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT]:
                self.rect.centerx += self.wd / 178

            elif keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
                self.rect.centerx -= self.wd / 178

        if self.rect.left > self.wd:
            self.rect.right = 0
        if self.rect.right < 0:
            self.rect.left = self.wd

    def take_dmg1(self):
        self.image = pygame.transform.scale(self.image_sprite, (self.wd/11, self.ht/11))

    def take_dmg2(self):
        self.image = pygame.transform.scale(self.image_inv, (self.wd/11, self.ht/11))

    def death_check(self, li):
        if li <= 0:
            self.take_dmg2()

    def update(self, lives):
        self.player_input()
        self.death_check(lives)


class Hearts(pygame.sprite.Sprite):  # Number of lives UI
    def __init__(self, wd, ht, plr):
        super().__init__()
        self.wd = wd
        self.ht = ht
        self.images = [pygame.image.load("graphics/hearts1.png"),
                       pygame.image.load("graphics/hearts2.png"),
                       pygame.image.load("graphics/hearts3.png"),
                       pygame.image.load("graphics/hearts4.png"),
                       pygame.image.load("graphics/hearts5.png"),
                       pygame.image.load("graphics/hearts1.5.png"),
                       pygame.image.load("graphics/hearts2.5.png"),
                       pygame.image.load("graphics/hearts3.5.png"),
                       pygame.image.load("graphics/hearts4.5.png")]

        self.image = pygame.transform.scale(self.images[2], (wd/3, ht/10))
        if plr:
            self.rect = self.image.get_rect(center=(wd/6, ht/30))
        else:
            self.rect = self.image.get_rect(center=(wd/6, ht/1.05))

    def animate(self, lvs, inv):  # Inv frames prevent multiple lives lost at once
        if inv <= 90:
            self.image = pygame.transform.scale(self.images[lvs-1], (self.wd/3, self.ht/10))
        elif lvs == 1:
            self.image = pygame.transform.scale(self.images[-4], (self.wd/3, self.ht/10))
        elif lvs == 2:
            self.image = pygame.transform.scale(self.images[-3], (self.wd/3, self.ht/10))
        elif lvs == 3:
            self.image = pygame.transform.scale(self.images[-2], (self.wd/3, self.ht/10))
        elif lvs == 4:
            self.image = pygame.transform.scale(self.images[-1], (self.wd/3, self.ht/10))

    def update(self, lives, frames):
        self.animate(lives, frames)


# Player weapon class
class Lasers(pygame.sprite.Sprite):
    def __init__(self, x, y, wd, ht, sound):
        super().__init__()
        self.wd = wd
        self.ht = ht
        self.surface = pygame.image.load("graphics/laser.png").convert_alpha()
        self.image = pygame.transform.scale(self.surface, (wd / 40, ht / 160))

        if sound:
            mixer.set_num_channels(10)
            mixer.Channel(1).set_volume(0.5)
            mixer.Channel(1).play(pygame.mixer.Sound('audio/sound_shoot.wav'))

        if get_setting("colour") == "True":
            self.image = change_hue(self.surface, 320)
            self.image = pygame.transform.scale(self.surface, (self.wd / 40, self.ht / 160))

        self.rect = self.image.get_rect(center=(x, y))

    def shoot(self):
        self.rect.x += self.wd/40

    def delete(self):  # Deletes sprite when it goes off-screen
        if self.rect.right > self.wd or self.rect.right < 0:
            self.kill()

    def update(self):
        self.shoot()
        self.delete()


# Enemy weapon class
class EnemyLasers(Lasers):
    def shoot(self):
        surface = pygame.image.load("graphics/laser2.png").convert_alpha()
        self.image = pygame.transform.scale(surface, (self.wd / 40, self.ht / 180))
        self.rect.x -= self.wd/80

    def delete(self):  # Deletes sprite when it goes off-screen
        if self.rect.right < 0:
            self.kill()


# Circular enemy bullets
class EnemyBullets(pygame.sprite.Sprite):
    def __init__(self, wd, ht, y):
        super().__init__()
        surface = pygame.image.load("graphics/circle_bullet.png")
        self.image = pygame.transform.scale(surface, (wd/70, ht/40))
        self.rect = self.image.get_rect(center=(wd, y))
        self.dir = random.uniform(-2, 2)

    def move(self):
        if self.rect.centerx < 0:
            self.kill()
        else:
            self.rect.centerx -= 10 - abs(self.dir*self.dir)
            self.rect.centery += self.dir

    def update(self):
        self.move()


# Enemy obstacles class
class Asteroids(pygame.sprite.Sprite):
    def __init__(self, wd, ht, x, y):
        super().__init__()
        self.wd = wd
        self.ht = ht
        self.surface = pygame.image.load("graphics/ast.png").convert_alpha()
        self.image = pygame.transform.scale(self.surface, (wd/12, ht/9))
        self.image.set_colorkey("white")
        self.rect = self.image.get_rect(center=(x, y))

    def move(self):
        self.rect.x -= self.wd/250

    def die(self):
        self.kill()

    def update(self):
        self.move()
        if self.rect.right < 1:
            self.die()


# Alien and boss class
class Alien(pygame.sprite.Sprite):
    def __init__(self, wd, ht, alien_type):
        super().__init__()
        self.type = alien_type
        self.wd = wd
        self.ht = ht

        if alien_type == "normal":
            self.lives = 3
            self.hit = False

            self.surface = pygame.image.load("graphics/alien1.png").convert_alpha()
            self.image = pygame.transform.scale(self.surface, (wd / 12, ht / 9))
            self.image.set_colorkey("white")
            self.rect = self.image.get_rect(center=(wd*1.1, random.uniform(ht*0.1, ht*0.9)))
        else:
            self.lives = 50
            self.hit = False
            self.surface_list = [pygame.image.load("graphics/boss_frame_0.gif"),
                                 pygame.image.load("graphics/boss_frame_2.gif"),
                                 pygame.image.load("graphics/boss_frame_3.gif"),
                                 pygame.image.load("graphics/boss_frame_4.gif"),
                                 pygame.image.load("graphics/boss_frame_5.gif"),
                                 pygame.image.load("graphics/boss_frame_6.gif"),
                                 pygame.image.load("graphics/boss_frame_7.gif"),
                                 pygame.image.load("graphics/boss_frame_8.gif")]

            self.image = pygame.transform.scale(self.surface_list[0], (wd / 4, ht / 4))
            self.rect = self.image.get_rect(center=(wd * 1.1, ht * 0.5))

    def move(self, px, py, p2x, p2y):
        self.hit = False
        if self.type == "normal":
            if self.rect.centery < self.ht/2:
                # player 1 side movement
                if self.rect.centery < py:
                    self.rect.centery += self.ht / 300
                elif self.rect.centery > py:
                    self.rect.centery -= self.ht / 300

                if px > self.wd / 2:
                    self.rect.centerx -= self.wd / 500
                elif px > self.wd / 10:
                    self.rect.centerx -= self.wd / px
                else:
                    self.rect.centerx -= self.wd / 100

            else:
                # player 2 side movement
                if self.rect.centery < p2y:
                    self.rect.centery += self.ht / 300
                elif self.rect.centery > p2y:
                    self.rect.centery -= self.ht / 300

                if p2x > self.wd / 2:
                    self.rect.centerx -= self.wd / 500
                elif p2x > self.wd / 10:
                    self.rect.centerx -= self.wd / p2x
                else:
                    self.rect.centerx -= self.wd / 100

        elif self.type == "boss":
            self.rect.centerx -= self.wd/2000

    def take_dmg(self, shot):
        if shot and not self.hit:
            self.lives -= 1
            self.hit = True

    def animate(self, timer):
        n = (timer % 16)//2
        self.image = pygame.transform.scale(self.surface_list[n], (self.wd / 4, self.ht / 4))
        self.image.set_colorkey("black")

    def update(self, playerx, playery, player2x, player2y, is_shot, timer):
        self.take_dmg(is_shot)
        self.move(playerx, playery, player2x, player2y)

        if self.type == "boss":
            self.animate(timer)

        if self.rect.centerx < 1 or self.lives == 0:
            self.kill()


class Pickup(pygame.sprite.Sprite):
    def __init__(self, wd, ht):
        super().__init__()
        self.type = "star"
        self.surface = pygame.image.load("graphics/star.png")
        self.image = pygame.transform.scale(self.surface, (wd/32, ht/20))
        self.rect = self.image.get_rect(center=(wd*1.1, random.uniform(ht*0.1, ht*0.9)))

    def move(self, width):
        self.rect.centerx -= width/150

    def change(self, wd, ht, pickup_type):
        # changes type of pickup, heart will give the player a life rather
        # than points
        if pickup_type == "heart":
            self.type = "heart"
            self.surface = pygame.image.load("graphics/smallheart.png")
            self.image = pygame.transform.scale(self.surface, (wd/32, ht/20))
        else:
            self.type = "star"
            self.surface = pygame.image.load("graphics/star.png")
            self.image = pygame.transform.scale(self.surface, (wd / 32, ht / 20))

    def reset(self, width, height, hide):
        if random.randint(0, 4) == 0:
            self.change(width, height, "heart")
        else:
            self.change(width, height, "star")

        if hide:
            self.rect.centerx = -100
        else:
            self.rect.centerx = width*1.1
            self.rect.centery = random.uniform(height*0.1, height*0.9)
        self.update_colour(width, height)

    def update_colour(self, width, height):
        if get_setting("colour") == "True" and self.type == "heart":
            self.image = change_hue(self.surface, 280)
        self.image = pygame.transform.scale(self.surface, (width/32, height/20))

    def update(self, wd, ht, timer, hide):
        self.move(wd)
        if timer % 600 == 0 or hide:
            self.reset(wd, ht, hide)


# Buttons on the main menu
class Option(pygame.sprite.Sprite):
    def __init__(self, variant, wd, ht):
        super().__init__()
        self.cycle = 0
        self.timer = 0
        self.toggle = True
        self.wd = wd
        self.ht = ht
        if variant == "play":
            self.type = "play"
            self.image_sprites = [pygame.image.load("graphics/menu/option_play.png"),
                                  pygame.image.load("graphics/menu/option_play1.png"),
                                  pygame.image.load("graphics/menu/option_play2.png"),
                                  pygame.image.load("graphics/menu/option_play3.png"),
                                  pygame.image.load("graphics/menu/option_play4.png")]

            self.image = pygame.transform.scale(self.image_sprites[0], (wd / 3, ht / 15))
            self.rect = self.image.get_rect(center=(wd/2, ht/2.5))

        elif variant == "settings":
            self.type = "settings"
            self.image_sprites = [pygame.image.load("graphics/menu/option_settings.png"),
                                  pygame.image.load("graphics/menu/option_settings1.png"),
                                  pygame.image.load("graphics/menu/option_settings2.png"),
                                  pygame.image.load("graphics/menu/option_settings3.png"),
                                  pygame.image.load("graphics/menu/option_settings4.png")]

            self.image = pygame.transform.scale(self.image_sprites[0], (self.wd / 2.3, self.ht / 15))
            self.rect = self.image.get_rect(center=(wd/2, ht/2.5 * 1.3))
        elif variant == "versus":
            self.type = "versus"
            self.image_sprites = [pygame.image.load("graphics/menu/option_versus.png"),
                                  pygame.image.load("graphics/menu/option_versus1.png"),
                                  pygame.image.load("graphics/menu/option_versus2.png"),
                                  pygame.image.load("graphics/menu/option_versus3.png"),
                                  pygame.image.load("graphics/menu/option_versus4.png")]

            self.image = pygame.transform.scale(self.image_sprites[0], (self.wd / 1.65, self.ht / 14.8))
            self.rect = self.image.get_rect(center=(wd/2, ht/2.5 * 1.6))
        elif variant == "highscores":
            self.type = "highscores"
            self.image_sprites = [pygame.image.load("graphics/menu/option_highscores.png"),
                                  pygame.image.load("graphics/menu/option_highscores1.png"),
                                  pygame.image.load("graphics/menu/option_highscores2.png"),
                                  pygame.image.load("graphics/menu/option_highscores3.png"),
                                  pygame.image.load("graphics/menu/option_highscores4.png")]

            self.image = pygame.transform.scale(self.image_sprites[0], (self.wd / 1.9, self.ht / 17))
            self.rect = self.image.get_rect(center=(wd/2, ht/2.5 * 1.9))
        else:
            self.type = "exit"
            self.image_sprites = [pygame.image.load("graphics/menu/option_exit.png"),
                                  pygame.image.load("graphics/menu/option_exit1.png")]
            self.image = pygame.transform.scale(self.image_sprites[0], (self.wd / 4, self.ht / 20))
            self.rect = self.image.get_rect(center=(wd/2, ht/2.5 * 2.3))

    def animate(self, select):
        if self.type == "play":
            if select == 0:
                self.image = pygame.transform.scale(self.image_sprites[self.cycle], (self.wd / 3, self.ht / 15))
            else:
                self.image = pygame.transform.scale(self.image_sprites[0], (self.wd / 3, self.ht / 15))
        if self.type == "settings":
            if select == 1:
                self.image = pygame.transform.scale(self.image_sprites[self.cycle], (self.wd / 2.3, self.ht / 15))
            else:
                self.image = pygame.transform.scale(self.image_sprites[0], (self.wd / 2.3, self.ht / 15))
        if self.type == "versus":
            if select == 2:
                self.image = pygame.transform.scale(self.image_sprites[self.cycle], (self.wd / 1.65, self.ht / 14.8))
            else:
                self.image = pygame.transform.scale(self.image_sprites[0], (self.wd / 1.65, self.ht / 14.8))
        if self.type == "highscores":
            if select == 3:
                self.image = pygame.transform.scale(self.image_sprites[self.cycle], (self.wd / 1.9, self.ht / 16))
            else:
                self.image = pygame.transform.scale(self.image_sprites[0], (self.wd / 1.9, self.ht / 17))
        elif self.type == "exit":
            if select == 4:
                self.image = pygame.transform.scale(self.image_sprites[1], (self.wd / 4, self.ht / 20))
            else:
                self.image = pygame.transform.scale(self.image_sprites[0], (self.wd / 4, self.ht / 20))

    def animate_cycle(self):
        if self.toggle:
            self.cycle += 1
        else:
            self.cycle -= 1
        if self.cycle >= 4:
            self.toggle = False
        if self.cycle <= 1:
            self.toggle = True

    def update(self, select):
        self.animate(select)
        self.timer -= 1
        if self.timer <= 0:
            self.timer = 8
            self.animate_cycle()


# Buttons and animations for the settings file
class Settings(pygame.sprite.Sprite):
    def __init__(self, variant, wd, ht):
        super().__init__()
        self.wd = wd
        self.ht = ht
        self.delay = 100
        if variant == "difficulty":
            self.type = "dif"
            self.image_list = [pygame.image.load("graphics/menu/setting_diff.png"),
                               pygame.image.load("graphics/menu/setting_diff1.png"),
                               pygame.image.load("graphics/menu/setting_diff2.png"),
                               pygame.image.load("graphics/menu/setting_diff3.png")]

            self.image = pygame.transform.scale(self.image_list[0], (wd / 1.6, ht / 17))
            self.rect = self.image.get_rect(midleft=(wd / 12, ht / 2.5 * 0.8))
        elif variant == "resolution":
            self.type = "res"
            self.image_list = [pygame.image.load("graphics/menu/setting_res.png"),
                               pygame.image.load("graphics/menu/setting_res1.png"),
                               pygame.image.load("graphics/menu/setting_res2.png"),
                               pygame.image.load("graphics/menu/setting_res3.png"),
                               pygame.image.load("graphics/menu/setting_res4.png")]

            self.image = pygame.transform.scale(self.image_list[0], (wd / 1.2, ht / 17))
            self.rect = self.image.get_rect(midleft=(wd / 12, ht / 2.5 * 1.2))
        elif variant == "colourblind":
            self.type = "colour"
            self.image_list = [pygame.image.load("graphics/menu/setting_colour.png"),
                               pygame.image.load("graphics/menu/setting_colour_b.png"),
                               pygame.image.load("graphics/menu/setting_colour1.png"),
                               pygame.image.load("graphics/menu/setting_colour1b.png")]
            self.image = pygame.transform.scale(self.image_list[0], (wd / 1.6, ht / 17))
            self.rect = self.image.get_rect(midleft=(wd / 12, ht / 2.5 * 1.6))
            get = get_setting("colour")
            if get == "True":
                self.toggle = True
            else:
                self.toggle = False
            self.ignore = False
        elif variant == "controls":
            self.type = "controls"
            self.image1 = pygame.image.load("graphics/menu/controls.png")
            self.image = pygame.transform.scale(self.image1, (wd/2, ht/6))
            self.rect = self.image.get_rect(midleft=(wd/12, ht/1.2))

    def action(self, r, c, d):
        keys = pygame.key.get_pressed()
        if self.type == "dif":
            if r == 0:
                temp_list = ["Easy", "Normal", "Hard"]
                c = c % 3
                self.image = pygame.transform.scale(self.image_list[c+1], (self.wd / 1.6, self.ht / 17))
                if (keys[pygame.K_SPACE] or keys[pygame.K_RETURN]) and d < 1:
                    save_setting("difficulty", temp_list[c])
            else:
                self.image = pygame.transform.scale(self.image_list[0], (self.wd / 1.6, self.ht / 17))
        elif self.type == "res":
            if r == 1:
                temp_list = ["800", "960", "1440", "1920"]
                temp_ht = ["600", "540", "810", "1080"]
                c = c % 4
                self.image = pygame.transform.scale(self.image_list[c+1], (self.wd / 1.2, self.ht / 17))
                if keys[pygame.K_SPACE] or keys[pygame.K_RETURN]:
                    save_setting("width", temp_list[c])
                    save_setting("height", temp_ht[c])
            else:
                self.image = pygame.transform.scale(self.image_list[0], (self.wd / 1.2, self.ht / 17))
        elif self.type == "colour":
            if r == 2:
                if self.toggle:
                    self.image = pygame.transform.scale(self.image_list[3], (self.wd / 1.6, self.ht / 17))
                    if (keys[pygame.K_SPACE] or keys[pygame.K_RETURN]) and not self.ignore:
                        save_setting("colour", "False")
                        self.toggle = not self.toggle
                        self.ignore = True
                else:
                    self.image = pygame.transform.scale(self.image_list[1], (self.wd / 1.6, self.ht / 17))
                    if (keys[pygame.K_SPACE] or keys[pygame.K_RETURN]) and not self.ignore:
                        save_setting("colour", "True")
                        self.toggle = not self.toggle
                        self.ignore = True
                if not keys[pygame.K_SPACE] and not keys[pygame.K_RETURN]:
                    self.ignore = False
            else:
                if self.toggle:
                    self.image = pygame.transform.scale(self.image_list[2], (self.wd / 1.6, self.ht / 17))
                else:
                    self.image = pygame.transform.scale(self.image_list[0], (self.wd / 1.6, self.ht / 17))

    def update(self, row, col, delay):
        self.action(row, col, delay)


# Marker to show the currently active setting
class SettingMarker(pygame.sprite.Sprite):
    def __init__(self, row, wd, ht):
        super().__init__()
        self.row = row
        self.wd = wd
        self.ht = ht
        self.image1 = pygame.image.load("graphics/menu/marker.png")
        self.image = pygame.transform.scale(self.image1, (self.wd / 26, self.ht / 20))
        self.rect = self.image.get_rect(center=(self.wd / 2, (self.ht / 6) * self.row + self.ht / 4))

    def move(self):
        if self.row == 0:
            col_dict = {"EASY": 0.4, "NORMAL": 0.52, "HARD": 0.65}
            self.rect.centerx = self.wd*col_dict[get_setting("difficulty").upper()]
        else:
            col_dict = {"800": 0.39, "960": 0.53, "1440": 0.68, "1920": 0.83}
            self.rect.centerx = self.wd*col_dict[get_setting("width")]

    def update_colour(self):
        self.image1 = pygame.image.load("graphics/menu/marker.png")
        if get_setting("colour") == "True":
            self.image = change_hue(self.image1, 320)
        self.image = pygame.transform.scale(self.image1, (self.wd / 26, self.ht / 20))

    def update(self, change):
        self.move()
        if change:
            self.update_colour()


# Text that displays the top 5 player's names with corresponding score
class HighscoreRow(pygame.sprite.Sprite):
    def __init__(self, num, wd, ht, name, score):
        super().__init__()
        self.num = num
        self.name = name
        self.score = score
        y = (ht/3 + num*ht/10)
        self.font = pygame.font.Font("graphics/fonts/ARCADE_R.ttf", round(wd / 24))
        self.image = self.font.render(f"{num+1} {name} {score}", False, (200, 200, 200))
        self.rect = self.image.get_rect(midleft=(wd/8, y))

    def update(self):
        if self.num == 0:
            self.image = self.font.render(f"{self.num+1} {self.name} {self.score}!", False, (250, 200, 10))
        else:
            self.image = self.font.render(f"{self.num+1} {self.name} {self.score}", False, (200, 200, 200))


# A message on screen that can be hidden or shown
class Texts(pygame.sprite.Sprite):
    def __init__(self, wd, ht, word, font, size):
        super().__init__()
        self.wd = wd
        self.ht = ht
        self.surface = font.render(str(word), False, (200, 200, 200))
        self.image = pygame.transform.scale(self.surface, (ht*size, wd*size))
        self.rect = self.image.get_rect(center=(wd/2, ht/2))

    def change(self, word, font, size):
        self.surface = font.render(word, False, (200, 200, 200))
        self.image = pygame.transform.scale(self.surface, (self.wd * size * 2, self.ht * size))
        self.rect = self.image.get_rect(center=(self.wd / 2, self.ht / 2))

    def update(self, word, font, size, is_shown):
        if is_shown:
            self.change(word, font, size)
        else:
            self.image = font.render("", False, (0, 0, 0))
