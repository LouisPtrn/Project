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

        if self.rect.centery < 0 and keys[pygame.K_w]:
            self.direction = pygame.math.Vector2(self.direction.x, 0)

        if self.rect.centery > self.ht and keys[pygame.K_s]:
            self.direction = pygame.math.Vector2(self.direction.x, 0)

        # Focus active when shift is held
        if keys[pygame.K_LSHIFT]:
            self.position += self.direction * 4
        else:
            self.position += self.direction * 8

        if self.rect.left > self.wd:
            self.rect.right = 0
            self.position.x = self.rect.x
        elif self.rect.right < 0:
            self.rect.left = self.wd
            self.position.x = self.rect.x

        # Set rect position to position vector
        self.rect.x = round(self.position.x)
        self.rect.y = round(self.position.y)

    def take_dmg1(self):
        self.image = pygame.transform.scale(self.image_sprite, (self.wd / 11, self.ht / 11))

    def take_dmg2(self):
        self.image = pygame.transform.scale(self.image_inv, (self.wd / 11, self.ht / 11))

    def death_check(self, li):
        if li <= 0:
            self.take_dmg2()

    def update(self, lives):
        self.player_input()
        self.death_check(lives)


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
            self.surface = pygame.image.load("graphics/alien1.png").convert_alpha()
            self.image = pygame.transform.scale(self.surface, (wd / 12, ht / 9))
            self.image.set_colorkey("white")
            self.rect = self.image.get_rect(center=(wd*1.1, random.uniform(ht*0.1, ht*0.9)))
        else:
            # Boss type alien
            self.lives = 50
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

    def move(self, px, py):
        if self.type == "normal":
            self.rect.centerx -= self.wd / 500
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
        elif self.type == "boss":
            self.rect.centerx -= self.wd/2000


    def animate(self, timer):
        n = (timer % 16)//2
        self.image = pygame.transform.scale(self.surface_list[n], (self.wd / 4, self.ht / 4))
        self.image.set_colorkey("black")

    def update(self, playerx, playery, timer):
        self.move(playerx, playery)

        if self.type == "boss":
            self.animate(timer)

        # Alien death when it goes off-screen or when it's health is 0
        if self.rect.centerx < 1 or self.lives <= 0:
            self.kill()


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


# Number of lives UI
class Hearts(pygame.sprite.Sprite):
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


def play1():
    width = 960
    height = 540
    play_game = True
    game_timer = 3600
    score = 0
    lives = 3
    level = 1
    inv_frames = 0
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Space Game")


    font1 = pygame.font.Font("graphics/fonts/ARCADE_I.ttf", round(width / 19))
    font2 = pygame.font.Font("graphics/fonts/ARCADE_N.ttf", round(width / 19))

    clock = pygame.time.Clock()

    bg = pygame.sprite.GroupSingle()
    bg.add(Background(width, height, level))

    player = pygame.sprite.GroupSingle()
    player.add(Player(width, height))
    laser = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    aliens = pygame.sprite.Group()
    badlaser = pygame.sprite.Group()
    player1_lives = pygame.sprite.GroupSingle()
    player1_lives.add(Hearts(width, height, True))

    score_surface = font2.render(str(score), True, (60, 60, 200)).convert_alpha()
    score_rect = score_surface.get_rect(center=(width / 2, height / 10))

    cooldown = 0
    alien_cooldown = 10
    game_state = 1

    while play_game:  # Game loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and (game_state == 1):
                if event.key == pygame.K_ESCAPE:
                    game_state = 10
            if event.type == pygame.KEYDOWN and (game_state == 10):
                if event.key == pygame.K_RETURN:
                    game_state = 1

        keys = pygame.key.get_pressed()
        # Play game
        if game_state == 1:
            if keys[pygame.K_SPACE] and cooldown < 1:  # Shooting input + max fire rate
                laser.add(Lasers(player.sprite.rect.centerx, player.sprite.rect.centery, width, height))
                cooldown = 10
            cooldown -= 1

            # Adding enemies
            if game_timer % 352 == 0 and game_timer > 500:
                attack_pattern1(enemies, width, height, random.randint(0, height))

            if game_timer % 401 == 0 and game_timer > 500:
                attack_pattern2(enemies, width, height, random.randint(0, height))

            if game_timer % 547 == 0 and game_timer > 500:
                attack_pattern3(enemies, width, height, random.randint(0, height))

            if random.randint(0, game_timer + 1000) <= 50 and game_timer > 250:
                badlaser.add(EnemyBullets(width, height, random.uniform(height * 0.1, height * 0.9)))


            # Collision Detection
            if pygame.sprite.groupcollide(laser, enemies, True, True):
                score += 100

            if game_timer % 270 == 0:  # Adding aliens
                aliens.add(Alien(width, height, "normal"))
            else:
                for alien in aliens:
                    if alien_cooldown <= 0 and alien.__getattribute__("type") == "normal":
                        badlaser.add(EnemyLasers(alien.rect.centerx, alien.rect.centery, width, height))
                        alien_cooldown = 20
            alien_cooldown -= 1

            # Alien hit detection
            for n in laser:
                for alien in aliens:
                    if pygame.sprite.collide_rect(n, alien):
                        n.kill()
                        alien.__setattr__("lives", alien.__getattribute__("lives") - 1)
                        if alien.__getattribute__("lives") <= 0:
                            score += 500

            # Player hit detection
            if (pygame.sprite.spritecollide(player.sprite, enemies, False) or
                pygame.sprite.spritecollide(player.sprite, badlaser, False) or
                pygame.sprite.spritecollide(player.sprite, aliens, False)) and inv_frames <= 0:
                lives -= 1
                inv_frames = 120

            invincibility(inv_frames, player.sprite)

            game_timer -= 1
            inv_frames -= 1

            # Update everything
            bg.draw(screen)
            bg.update(width)
            badlaser.draw(screen)
            badlaser.update()

            if lives > 0:
                player.draw(screen)
                player.update(lives)
            else:
                game_state = 2
            laser.draw(screen)
            aliens.update(player.sprite.rect.centerx, player.sprite.rect.centery, game_timer)
            aliens.draw(screen)
            enemies.draw(screen)
            enemies.update()
            laser.update()
            screen.blit(score_surface, score_rect)
            score_surface = font2.render(str(score), True, (60, 60, 200), (10, 10, 10)).convert_alpha()
            player1_lives.update(lives, inv_frames)
            player1_lives.draw(screen)

        elif game_state == 2:
            # Game over screen
            screen.fill("red")
            screen.blit(score_surface, score_rect)
        # Pause screen
        else:
            pass
        pygame.display.update()
        clock.tick(60)  # Caps at 60 fps


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
        if random.randint(0, 1) == 0:
            self.change(width, height, "heart")
        else:
            self.change(width, height, "star")

        if hide:
            self.rect.centerx = -100
        else:
            self.rect.centerx = width*1.1
            self.rect.centery = random.uniform(height*0.1, height*0.9)
        # self.update_colour(width, height)

    # def update_colour(self, width, height):
    #     if get_setting("colour") == "True" and self.type == "heart":
    #         self.image = change_hue(self.surface, 280)
    #     self.image = pygame.transform.scale(self.surface, (width/32, height/20))

    def update(self, wd, ht, timer, hide):
        self.move(wd)
        if timer % 600 == 0 or hide:
            self.reset(wd, ht, hide)


def play():
    width = 960
    height = 540
    play_game = True
    boss_active = False
    game_timer = 3600
    text_delay = 0
    score = 0
    lives = 3
    level = 1
    dif = "NORMAL"
    inv_frames = 0
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Space Game")

    font1 = pygame.font.Font("graphics/fonts/ARCADE_I.ttf", round(width / 19))
    font2 = pygame.font.Font("graphics/fonts/ARCADE_N.ttf", round(width / 19))
    level_text = font2.render("", False, (255, 255, 255), (0, 0, 0))
    level_rect = level_text.get_rect(center=(width / 3, height / 2))
    message = pygame.sprite.GroupSingle()
    message.add(Texts(width, height, "word", font2, 0.1))

    clock = pygame.time.Clock()

    bg = pygame.sprite.GroupSingle()
    bg.add(Background(width, height, level))

    player = pygame.sprite.GroupSingle()
    player.add(Player(width, height))
    laser = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    aliens = pygame.sprite.Group()
    badlaser = pygame.sprite.Group()
    player1_lives = pygame.sprite.GroupSingle()
    player1_lives.add(Hearts(width, height, True))
    star = pygame.sprite.GroupSingle()
    star.add(Pickup(width, height))

    score_surface = font2.render(str(score), True, (60, 60, 200)).convert_alpha()
    score_rect = score_surface.get_rect(center=(width / 2, height / 10))

    cooldown = 0
    alien_cooldown = 10
    game_state = 1
    hide_star = False

    while play_game:  # Game loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and (game_state == 1):
                if event.key == pygame.K_ESCAPE:
                    text_delay = 40
                    game_state = 10
            if event.type == pygame.KEYDOWN and (game_state == 10):
                if event.key == pygame.K_ESCAPE and text_delay <= 0:
                    game_state = 1

        keys = pygame.key.get_pressed()
        # Play game
        if game_state == 1:
            # Gameplay
            bg_changed = False
            hide_star = False
            game_timer -= 1
            keys = pygame.key.get_pressed()

            if game_timer <= 1:
                game_timer = 3600
                text_delay = 0
                level_text = font2.render("", False, (255, 255, 255), (0, 0, 0))
                i = 0
                if level == 3: # Final level
                    game_state = 9
                else:
                    game_state = 4
                level += 1

            if keys[pygame.K_SPACE] and cooldown < 1:  # Shooting input + max fire rate
                laser.add(Lasers(player.sprite.rect.centerx, player.sprite.rect.centery, width, height))
                if dif == "NORMAL":
                    cooldown = 10

            cooldown -= 1

            # Collision Detection
            if pygame.sprite.groupcollide(laser, enemies, True, True):
                score += 100

            if pygame.sprite.groupcollide(player, star, False, False):
                if star.sprite.__getattribute__("type") == "star":
                    score += 1000
                    hide_star = True
                else:
                    hide_star = True
                    if lives < 5:
                        lives += 1

            if (pygame.sprite.spritecollide(player.sprite, enemies, False) or
                pygame.sprite.spritecollide(player.sprite, badlaser, False) or
                pygame.sprite.spritecollide(player.sprite, aliens, False)) and inv_frames <= 0:
                lives -= 1
                inv_frames = 120

            # Adding enemies
            if game_timer % 352 == 0 and game_timer > 250:
                attack_pattern1(enemies, width, height, random.randint(0, height))

            if game_timer % 401 == 0 and game_timer > 250:
                attack_pattern2(enemies, width, height, random.randint(0, height))

            if game_timer % 547 == 0 and game_timer > 250:
                attack_pattern3(enemies, width, height, random.randint(0, height))

            if random.randint(0, game_timer + 1000) <= 50 and game_timer > 250:
                badlaser.add(EnemyBullets(width, height, random.uniform(height * 0.1, height * 0.9)))

            # Alien hit detection
            for n in laser:
                for alien in aliens:
                    if pygame.sprite.collide_rect(n, alien):
                        n.kill()
                        alien.__setattr__("lives", alien.__getattribute__("lives") - 1)
                        if alien.__getattribute__("lives") <= 0:
                            score += 500

            if game_timer % 200 == 0:
                aliens.add(Alien(width, height, "normal"))

            else:
                for alien in aliens:
                    if alien_cooldown <= 0 and alien.__getattribute__("type") == "normal":
                        badlaser.add(EnemyLasers(alien.rect.centerx, alien.rect.centery, width, height))
                        alien_cooldown = 30
                    if (alien.__getattribute__("type") == "boss") and ((0 >= boss_timer >= -150) or
                                                                       (-250 >= boss_timer >= -2000)) and \
                            boss_timer % 3 == 0:
                        badlaser.add(EnemyLasers(alien.rect.centerx,
                                                 alien.rect.centery + (height / random.randint(7, 9)), width, height))
                        badlaser.add(EnemyLasers(alien.rect.centerx,
                                                 alien.rect.centery - (height / random.randint(7, 9)), width, height))


            if game_timer == 1800 and level == 3:
                aliens.add(Alien(width, height, "boss"))
                boss_active = True
                boss_timer = 300

            alien_cooldown -= 1
            invincibility(inv_frames, player.sprite)

            if boss_active:
                boss_timer -= 1
                if len(aliens) == 0:
                    boss_active = False
                    score += 5000
                    boss_timer = 200
            elif level == 3 and game_timer < 1800:
                boss_timer += 1
                if boss_timer > 400:
                    game_state = 9

            # Draw background first
            bg.draw(screen)
            bg.update(width)

            inv_frames -= 1
            # Sprites drawing and updating
            laser.draw(screen)
            laser.update()
            aliens.update(player.sprite.rect.centerx, player.sprite.rect.centery, game_timer)
            aliens.draw(screen)
            enemies.draw(screen)
            enemies.update()
            star.draw(screen)
            star.update(width, height, game_timer, hide_star)
            badlaser.draw(screen)
            badlaser.update()

            if lives > 0:
                player.draw(screen)
                player.update(lives)
            else:
                game_state = 2
            screen.blit(score_surface, score_rect)
            score_surface = font2.render(str(score), True, (60, 60, 200), (10, 10, 10)).convert_alpha()
            player1_lives.update(lives, inv_frames)
            player1_lives.draw(screen)

        elif game_state == 2:
            # Game over screen
            screen.fill("black")
            screen.blit(score_surface, score_rect)
            message.update("GAME OVER", font1, 0.2, True)
            message.draw(screen)

        # Level transition screen
        elif game_state == 4:
            screen.fill((0, 0, 0))
            if not bg_changed:
                # mixer.music.load("audio/music_1.mp3")
                # mixer.music.set_volume(0)
                # mixer.music.play()
                bg.empty()
                bg.add(Background(width, height, level))
                bg_changed = True
            if level == 1:
                # mixer.music.load("audio/music_2.mp3")
                # mixer.music.set_volume(0)
                # mixer.music.play()
                pass

            text = "LEVEL " + str(level)
            if text_delay >= 10:
                if i <= len(text):

                    level_text = font2.render(text[:i], False, (255, 255, 255), (0, 0, 0))
                    i += 1
                    text_delay = 0
                elif text_delay >= 50:
                    game_state = 1
            text_delay += 1
            screen.blit(level_text, level_rect)

        elif game_state == 9:
            # Win screen
            keys = pygame.key.get_pressed()
            game_timer += 1

            screen.fill("black")
            # score_rect = score_surface.get_rect(center=(width / 2, height / 1.5))

            if game_timer % 40 >= 20:
                message.update("You win!", font2, 0.2, False)
            else:
                message.update("You win!", font2, 0.2, True)

            message.draw(screen)
            screen.blit(score_surface, score_rect)

            laser.empty()
            aliens.empty()
            badlaser.empty()
            enemies.empty()
            # if not saved:
            #     enter_score(name, score, get_date())
            #     saved = True
            # if keys[pygame.K_RETURN]:
            #     game_state = 1
            #     start_delay = 30

        # Pause screen
        else:
            text_delay -= 1
            message.update("PAUSED", font1, 0.15, True)
            message.draw(screen)
        pygame.display.update()
        clock.tick(60)  # Caps at 60 fps


# Three enemies in horizontal line
def attack_pattern1(sprite_group, width, height, y):
    sprite_group.add(Asteroids(width, height, width * 1.1, y))
    sprite_group.add(Asteroids(width, height, width * 1.25, y))
    sprite_group.add(Asteroids(width, height, width * 1.4, y))


# Three enemies in vertical line
def attack_pattern2(sprite_group, width, height, y):
    sprite_group.add(Asteroids(width, height, width * 1.1, y - (0.2 * height)))
    sprite_group.add(Asteroids(width, height, width * 1.1, y))
    sprite_group.add(Asteroids(width, height, width * 1.1, y + (0.2 * height)))


# Three enemies in diagonal line
def attack_pattern3(sprite_group, width, height, y):
    sprite_group.add(Asteroids(width, height, width * 1.1, y))
    sprite_group.add(Asteroids(width, height, width * 1.2, y + (0.2 * height)))
    sprite_group.add(Asteroids(width, height, width * 1.3, y + (0.4 * height)))

def invincibility(inv_frames, sprite):
    # Invincibility frames flashing animation
    # Pycharm marks the passing of a sprite as a warning: "Expected type 'Player', got 'Sprite' instead"
    # but this still functions normally with no bugs.
    if inv_frames >= 0:
        if inv_frames >= 100:
            Player.take_dmg2(sprite)
        elif inv_frames >= 80:
            Player.take_dmg1(sprite)
        elif inv_frames >= 60:
            Player.take_dmg2(sprite)
        elif inv_frames >= 40:
            Player.take_dmg1(sprite)
        elif inv_frames >= 20:
            Player.take_dmg2(sprite)
        else:
            Player.take_dmg1(sprite)
    else:
        Player.take_dmg1(sprite)

if __name__ == "__main__":
    play()

    # def take_dmg1(self):
    #     self.image = pygame.transform.scale(self.image_sprite, (self.wd/11, self.ht/11))
    #
    # def take_dmg2(self):
    #     self.image = pygame.transform.scale(self.image_inv, (self.wd/11, self.ht/11))

    # def death_check(self, li):
    #     if li <= 0:
    #         self.take_dmg2()
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------