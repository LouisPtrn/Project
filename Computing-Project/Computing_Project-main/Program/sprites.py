# ============================================================================================================== #
# SPRITES AND CLASSES FILE
# Written by: Louis Pattern     10/08/2022
# Known bugs: none
# ============================================================================================================== #

import pygame
import random
from settings import *


class Player(pygame.sprite.Sprite):  # Spaceship class
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
                self.rect.centery += self.ht/200

            if keys[pygame.K_w] and self.rect.centery > 0 and not keys[pygame.K_s]:
                self.rect.centery -= self.ht/200

            if keys[pygame.K_d] and not keys[pygame.K_a]:
                self.rect.centerx += self.wd/356

            if keys[pygame.K_a] and not keys[pygame.K_d]:
                self.rect.centerx -= self.wd/356
        else:
            if keys[pygame.K_s] and self.rect.centery < self.ht and not keys[pygame.K_w]:
                self.rect.centery += self.ht/100

            if keys[pygame.K_w] and self.rect.centery > 0 and not keys[pygame.K_s]:
                self.rect.centery -= self.ht/100

            if keys[pygame.K_d] and not keys[pygame.K_a]:
                self.rect.centerx += self.wd/178

            if keys[pygame.K_a] and not keys[pygame.K_d]:
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
            self.kill()

    def update(self, lives):
        self.player_input()
        self.death_check(lives)


class PlayerA(Player):
    def player_input(self):  # Altered movement for versus
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LSHIFT]:
            if keys[pygame.K_s] and self.rect.centery < self.ht/2.25 and not keys[pygame.K_w]:
                self.rect.centery += self.ht/200

            if keys[pygame.K_w] and self.rect.centery > 0 and not keys[pygame.K_s]:
                self.rect.centery -= self.ht/200

            if keys[pygame.K_d] and not keys[pygame.K_a]:
                self.rect.centerx += self.wd/356

            if keys[pygame.K_a] and not keys[pygame.K_d]:
                self.rect.centerx -= self.wd/356
        else:
            if keys[pygame.K_s] and self.rect.centery < self.ht/2.25 and not keys[pygame.K_w]:
                self.rect.centery += self.ht/100

            if keys[pygame.K_w] and self.rect.centery > 0 and not keys[pygame.K_s]:
                self.rect.centery -= self.ht/100

            if keys[pygame.K_d] and not keys[pygame.K_a]:
                self.rect.centerx += self.wd/178

            if keys[pygame.K_a] and not keys[pygame.K_d]:
                self.rect.centerx -= self.wd/178

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
            if keys[pygame.K_DOWN] and self.rect.centery < self.ht and not keys[pygame.K_UP]:
                self.rect.centery += self.ht/200

            if keys[pygame.K_UP] and self.rect.centery > self.ht/1.85 and not keys[pygame.K_DOWN]:
                self.rect.centery -= self.ht/200

            if keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT]:
                self.rect.centerx += self.wd/356

            if keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
                self.rect.centerx -= self.wd/356
        else:
            if keys[pygame.K_DOWN] and self.rect.centery < self.ht and not keys[pygame.K_UP]:
                self.rect.centery += self.ht/100

            if keys[pygame.K_UP] and self.rect.centery > self.ht/1.85 and not keys[pygame.K_DOWN]:
                self.rect.centery -= self.ht/100

            if keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT]:
                self.rect.centerx += self.wd/178

            if keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
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
            self.kill()

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
                       pygame.image.load("graphics/hearts1.5.png"),
                       pygame.image.load("graphics/hearts2.5.png")]

        self.image = pygame.transform.scale(self.images[2], (wd/3, ht/10))
        if plr:
            self.rect = self.image.get_rect(center=(wd/6, ht/30))
        else:
            self.rect = self.image.get_rect(center=(wd/6, ht/1.05))

    def animate(self, lvs, inv):  # Inv frames prevent multiple lives lost at once
        if inv <= 90:
            self.image = pygame.transform.scale(self.images[lvs-1], (self.wd/3, self.ht/10))
        elif lvs == 2:
            self.image = pygame.transform.scale(self.images[-1], (self.wd/3, self.ht/10))
        else:
            self.image = pygame.transform.scale(self.images[-2], (self.wd/3, self.ht/10))

    def update(self, lives, frames):
        self.animate(lives, frames)


class Lasers(pygame.sprite.Sprite):  # Playser weapon class
    def __init__(self, x, y, wd, ht):
        super().__init__()
        self.wd = wd
        self.ht = ht
        self.surface = pygame.image.load("graphics/laser.png").convert_alpha()
        self.image = pygame.transform.scale(self.surface, (self.wd / 40, self.ht / 160))
        self.rect = self.image.get_rect(center=(x, y))

    def shoot(self):
        self.rect.x += self.wd/40

    def delete(self):  # Deletes sprite when it goes off screen
        if self.rect.left > self.wd or self.rect.right < 0:
            self.kill()

    def update(self):
        self.shoot()
        self.delete()


class EnemyLasers(Lasers):  # Enemy weapon class
    def shoot(self):
        surface = pygame.image.load("graphics/laser2.png").convert_alpha()
        self.image = pygame.transform.scale(surface, (self.wd / 40, self.ht / 180))
        self.rect.x -= self.wd/80

    def delete(self):  # Deletes sprite when it goes off screen
        if self.rect.right < 0:
            self.kill()


class Enemies(pygame.sprite.Sprite):  # Enemies and obstacles class
    def __init__(self, wd, ht, y1, y2):
        super().__init__()
        self.wd = wd
        self.ht = ht
        self.surface = pygame.image.load("graphics/ast.png").convert_alpha()
        self.image = pygame.transform.scale(self.surface, (wd/12, ht/9))
        self.image.set_colorkey("white")
        self.rect = self.image.get_rect(center=(wd*1.1, random.uniform(y1+ht*0.07, y2-ht*0.07)))

    def move(self):
        self.rect.x -= self.wd/250

    def die(self):
        if self.rect.right < 0:
            self.kill()

    def update(self):
        self.move()
        self.die()


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


class SettingMarker(pygame.sprite.Sprite):
    def __init__(self, row, wd, ht):
        super().__init__()
        self.row = row
        self.wd = wd
        self.image1 = pygame.image.load("graphics/menu/marker.png")
        self.image = pygame.transform.scale(self.image1, (wd/26, ht/20))
        self.rect = self.image.get_rect(center=(wd/2, (ht/6)*row + ht/4))

    def move(self):
        if self.row == 0:
            col_dict = {"EASY": 0.4, "NORMAL": 0.52, "HARD": 0.65}
            self.rect.centerx = self.wd*col_dict[get_setting("difficulty").upper()]
        else:
            col_dict = {"800": 0.39, "960": 0.53, "1440": 0.68, "1920": 0.83}
            self.rect.centerx = self.wd*col_dict[get_setting("width")]

    def update(self):
        self.move()
