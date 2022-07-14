# ============================================================================================================== #
#                                             GAME PROGRAM
# Written by: Louis Pattern     13/07/2022
# Known bugs:  none
# ============================================================================================================== #

import pygame
from sys import exit
import random


class Player(pygame.sprite.Sprite):  # Spaceship class
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("graphics/ship1.png").convert_alpha()
        self.rect = self.image.get_rect(center=(200, 200))

    def player_input(self):  # Ship movement from input
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LSHIFT]:
            if keys[pygame.K_s] and self.rect.centery < 600:
                self.rect.centery += 3

            if keys[pygame.K_w] and self.rect.centery > 0:
                self.rect.centery -= 3

            if keys[pygame.K_d]:
                self.rect.centerx += 3

            if keys[pygame.K_a]:
                self.rect.centerx -= 3
        else:
            if keys[pygame.K_s] and self.rect.centery < 600:
                self.rect.centery += 6

            if keys[pygame.K_w] and self.rect.centery > 0:
                self.rect.centery -= 6

            if keys[pygame.K_d]:
                self.rect.centerx += 6

            if keys[pygame.K_a]:
                self.rect.centerx -= 6

        if self.rect.left > 960:
            self.rect.right = 0
        if self.rect.right < 0:
            self.rect.left = 960

    def update(self):
        self.player_input()


class Lasers(pygame.sprite.Sprite):  # Weapons and projectile class
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("graphics/laser.png").convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))

    def shoot(self):
        self.rect.x += 24

    def delete(self):  # Deletes sprite when it goes off screen
        if self.rect.x > 1000:
            self.kill()

    def update(self):
        self.shoot()
        self.delete()


class Enemies(pygame.sprite.Sprite):  # Enemies and obstacles class
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("graphics/ast.png").convert_alpha()
        self.image.set_colorkey("white")
        self.rect = self.image.get_rect(center=(1000, random.randint(10, 590)))

    def move(self):
        self.rect.x -= 4

    def die(self):
        if self.rect.right < 1:
            self.kill()

    def update(self):
        self.move()
        self.die()

class Option(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        self.cycle = 0
        self.timer = 0
        self.toggle = True
        if type == "play":
            self.type = "play"
            self.image_sprite = [pygame.image.load("graphics/menu/option_play.png"),
                                 pygame.image.load("graphics/menu/option_play1.png"),
                                 pygame.image.load("graphics/menu/option_play2.png"),
                                 pygame.image.load("graphics/menu/option_play3.png"),
                                 pygame.image.load("graphics/menu/option_play4.png")]

            self.image = self.image_sprite[0]
            self.rect = self.image.get_rect(center=(460, 300))

        elif type == "settings":
            self.type = "settings"
            self.image_sprite = [pygame.image.load("graphics/menu/option_settings.png"),
                                 pygame.image.load("graphics/menu/option_settings1.png"),
                                 pygame.image.load("graphics/menu/option_settings2.png"),
                                 pygame.image.load("graphics/menu/option_settings3.png"),
                                 pygame.image.load("graphics/menu/option_settings4.png")]

            self.image = self.image_sprite[0]
            self.rect = self.image.get_rect(center=(460, 400))
        else:
            self.type = "versus"
            self.image_sprite = [pygame.image.load("graphics/menu/option_versus.png"),
                                 pygame.image.load("graphics/menu/option_versus1.png"),
                                 pygame.image.load("graphics/menu/option_versus2.png"),
                                 pygame.image.load("graphics/menu/option_versus3.png"),
                                 pygame.image.load("graphics/menu/option_versus4.png")]

            self.image = self.image_sprite[0]
            self.rect = self.image.get_rect(center=(460, 500))
    def animate(self, select):
        if self.type == "play":
            if select == 0:
                self.image = self.image_sprite[self.cycle]
            else:
                self.image = self.image_sprite[0]
        if self.type == "settings":
            if select == 1:
                self.image = self.image_sprite[self.cycle]
            else:
                self.image = self.image_sprite[0]
        if self.type == "versus":
            if select == 2:
                self.image = self.image_sprite[self.cycle]
            else:
                self.image = self.image_sprite[0]
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





def play():
    pygame.init()
    screen = pygame.display.set_mode((960, 600))  # Game window
    pygame.display.set_caption("Space Game")
    clock = pygame.time.Clock()

    test_font = pygame.font.Font(None, 50)
    score = 0
    div_rect = pygame.Rect(-300, 290, 2000, 10)
    text_surface = test_font.render("SPACE GAME", True, (180, 10, 10))
    game_over = test_font.render("GAME OVER", True, (255, 0, 0))
    menu_text = test_font.render("MENU", False, (200, 200, 200), (0, 0, 0))
    score_surface = test_font.render(str(score), True, (60, 60, 200)).convert_alpha()
    bg_surface = pygame.image.load("graphics/spacebg.png").convert_alpha()
    player = pygame.sprite.GroupSingle()
    player.add(Player())
    laser = pygame.sprite.Group()
    ast = pygame.sprite.Group()
    options = pygame.sprite.Group()
    buttons = ["play", "settings", "versus"]
    for i in buttons:
        options.add(Option(i))
    cooldown = 0
    game_state = 0
    select = 0
    play_game = True


    while play_game:  # Game loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and select > 0:
                    select -= 1
                if event.key == pygame.K_DOWN and select < 2:
                    select += 1

        # Main Menu
        if game_state == 0:
            screen.fill((0, 0, 0))
            screen.blit(menu_text, (400, 160))
            keys = pygame.key.get_pressed()
            screen.blit(text_surface, (340, 100))
            options.update(select)
            options.draw(screen)

            score = 0
            if keys[pygame.K_SPACE] and select == 0:
                score = 0
                game_state = 1
                player.sprite.rect.centery = 200  # Reset ship pos
                player.sprite.rect.centerx = 100

        # Gameplay
        elif game_state == 1:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE] and cooldown < 1:  # Shooting input + max fire rate
                laser.add(Lasers(player.sprite.rect.centerx, player.sprite.rect.centery))
                cooldown = 20
            cooldown -= 1

            # Collision Detection
            if pygame.sprite.groupcollide(laser, ast, True, True):
                score += 100
            if pygame.sprite.spritecollide(player.sprite, ast, False):
                game_state = 2

            if random.randint(0, 30) == 0:
                ast.add(Enemies())

            # Drawing non - sprites
            pygame.draw.rect(screen, "#FFFFFF", div_rect)
            screen.blit(bg_surface, (0, 0))
            pygame.draw.rect(screen, "White", div_rect)
            screen.blit(score_surface, (450, 280))
            score_surface = test_font.render(str(score), True, (60, 60, 200), (10, 10, 10)).convert_alpha()
            cooldown -= 1
            # Sprites drawing and updating
            laser.draw(screen)
            laser.update()
            ast.draw(screen)
            ast.update()
            player.draw(screen)
            player.update()

        else:
            # Game Over screen
            screen.fill("Black")
            screen.blit(game_over, (360, 250))
            screen.blit(score_surface, (400, 150))
            keys = pygame.key.get_pressed()
            score = 0
            laser.empty()  # Deletes all sprites on screen
            ast.empty()
            if keys[pygame.K_RETURN]:
                score = 0
                game_state = 0
                player.sprite.rect.centery = 200  # Reset ship pos
                player.sprite.rect.centerx = 100

        # Update everything
        pygame.display.update()
        clock.tick(60)  # Caps at 60 fps


if __name__ == "__main__":
    play()
