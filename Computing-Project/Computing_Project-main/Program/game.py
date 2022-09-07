# ============================================================================================================== #
#                                             GAME PROGRAM
# Written by: Louis Pattern     12/08/2022
# Known bugs:  none
# ============================================================================================================== #

from sys import exit
import login
from HighscoresData import *
from Dates import *
from messages import *
import os


os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"  # Hides pygame welcome message, must be before sprite import
from sprites import *


def play(name):
    pygame.init()
    mixer.init()
    width = int(get_setting("WIDTH"))
    height = int(get_setting("HEIGHT"))

    screen = pygame.display.set_mode((width, height))  # Game window
    pygame.display.set_caption("Space Game")
    clock = pygame.time.Clock()

    font1 = pygame.font.Font("graphics/fonts/ARCADE_I.ttf", round(width / 19))
    font2 = pygame.font.Font("graphics/fonts/ARCADE_N.ttf", round(width / 19))
    score = 0
    level = 1
    game_timer = 3600

    div_rect = pygame.Rect(0, height / 2.1, width * 2, height / 25)

    text_surface = font1.render("SPACE GAME", True, (180, 10, 10))
    text_rect = text_surface.get_rect(center=(width / 2, height / 8))
    game_over = font2.render("GAME OVER", True, (255, 0, 0))
    # menu_text = font2.render("MENU", False, (200, 200, 200), (0, 0, 0))
    # menu_rect = menu_text.get_rect(center=(width / 2, height / 4))
    settings_text = font2.render("SETTINGS", False, (200, 200, 200), (0, 0, 0))
    settings_rect = settings_text.get_rect(center=(width / 4, height / 8))
    level_text = font2.render("", False, (255, 255, 255), (0, 0, 0))
    level_rect = level_text.get_rect(center=(width / 3, height / 2))

    cog_image = pygame.image.load("graphics/cog.jpg")
    cog_surf = pygame.transform.scale(cog_image, (width / 10, height / 8))
    back_image = pygame.image.load("graphics/menu/back.png")
    back_surf = pygame.transform.scale(back_image, (width / 10, height / 10))
    back_surf.set_colorkey("black")
    score_surface = font2.render(str(score), True, (60, 60, 200)).convert_alpha()
    score_rect = score_surface.get_rect(center=(width / 2, height / 10))

    score2_surface = font2.render(str(score), True, (60, 60, 200)).convert_alpha()
    score2_rect = score2_surface.get_rect(center=(width / 2, height / 1.5))
    timer_surf = font2.render(str(game_timer // 60), True, (20, 200, 20)).convert_alpha()
    timer_rect = timer_surf.get_rect(center=(width / 2, height / 2))

    bg_image = pygame.image.load("graphics/spacebg.jpg").convert_alpha()
    bg_surface = pygame.transform.scale(bg_image, (width, height))

    player = pygame.sprite.GroupSingle()
    player.add(Player(width, height))
    player1 = pygame.sprite.GroupSingle()
    player1.add(PlayerA(width, height))
    player2 = pygame.sprite.GroupSingle()
    player2.add(PlayerB(width, height))

    player1_lives = pygame.sprite.GroupSingle()
    player1_lives.add(Hearts(width, height, True))
    player2_lives = pygame.sprite.GroupSingle()
    player2_lives.add(Hearts(width, height, False))

    laser = pygame.sprite.Group()
    laser2 = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    aliens = pygame.sprite.Group()
    options = pygame.sprite.Group()
    settings = pygame.sprite.Group()
    marker = pygame.sprite.Group()
    hs_rows = pygame.sprite.Group()
    badlaser = pygame.sprite.Group()

    buttons = ["play", "settings", "versus", "highscores", "exit"]
    set_buttons = ["difficulty", "resolution", "colourblind", "controls"]

    for i in range(2):
        marker.add(SettingMarker(i, width, height))

    for i in buttons:
        options.add(Option(i, width, height))
    for i in set_buttons:
        settings.add(Settings(i, width, height))

    name_list = get_names()
    score_list = get_scores()

    for i in range(5):
        hs_rows.add(HighscoreRow(i, width, height, name_list[i], score_list[i]))

    dif = get_setting("difficulty").upper()

    # initialise variables

    score2 = 0
    lives = 3
    lives_b = 3
    inv_frames = 0
    inv_frames_b = 0
    cooldown = 0
    cooldown_b = 0
    alien_cooldown = 10
    game_state = 0
    select = 0
    set_row = 0
    set_col = 0
    start_delay = 30

    set_delay = 10
    play_game = True
    saved = False

    while play_game:  # Game loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and game_state == 0:
                if event.key == pygame.K_UP and select > 0:
                    select -= 1
                if event.key == pygame.K_DOWN and select < 4:
                    select += 1
            if event.type == pygame.KEYDOWN and game_state == 3:
                if event.key == pygame.K_LEFT:
                    set_col -= 1
                if event.key == pygame.K_RIGHT:
                    set_col += 1
                if event.key == pygame.K_UP and set_row > 0:
                    set_row -= 1
                    set_col = 0
                if event.key == pygame.K_DOWN and set_row < 2:
                    set_row += 1
                    set_col = 0

        # Main Menu
        if game_state == 0:
            keys = pygame.key.get_pressed()
            menu_text = font2.render("MENU", False, (200, 200, 200), (0, 0, 0))
            menu_rect = menu_text.get_rect(center=(width / 2, height / 4))
            screen.fill((0, 0, 0))
            screen.blit(menu_text, menu_rect)
            screen.blit(text_surface, text_rect)
            options.update(select)
            options.draw(screen)
            score = 0

            if (keys[pygame.K_RETURN] or keys[pygame.K_SPACE]) and select == 0 and start_delay <= 0:  # Play game
                saved = False
                i = 0
                text_delay = 0
                game_timer = 3600
                level_text = font2.render("", False, (255, 255, 255), (0, 0, 0))
                score = 0
                game_state = 4
                player.sprite.rect.centery = height / 2  # Reset ship pos
                player.sprite.rect.centerx = width / 10
                alien_cooldown = 0

            if (keys[pygame.K_RETURN] or keys[pygame.K_SPACE]) and select == 1 and start_delay <= 0:
                # Takes to settings screen
                game_state = 3
                set_delay = 10
                timer_change = False

            if (keys[pygame.K_RETURN] or keys[pygame.K_SPACE]) and select == 2 and start_delay <= 0:
                # Takes to versus mode
                game_timer = 3600
                game_state = 7
                start_delay = 60

            if (keys[pygame.K_RETURN] or keys[pygame.K_SPACE]) and select == 3 and start_delay <= 0:
                game_state = 8

            if (keys[pygame.K_RETURN] or keys[pygame.K_SPACE]) and select == 4 and start_delay <= 0:
                pygame.quit()
                # Logs off the user
                login2 = login.LoginWindow()
                login2.mainloop()
                return ()

            start_delay -= 1

        # Gameplay
        elif game_state == 1:
            if level == 1:
                alien_shot = False
                game_timer -= 1
                keys = pygame.key.get_pressed()

                if game_timer <= 1:
                    game_state = 9

                if keys[pygame.K_SPACE] and cooldown < 1:  # Shooting input + max fire rate
                    laser.add(Lasers(player.sprite.rect.centerx, player.sprite.rect.centery, width, height, True))
                    cooldown = 20
                cooldown -= 1

                # Collision Detection
                if pygame.sprite.groupcollide(laser, enemies, True, True):
                    score += 10

                if (pygame.sprite.spritecollide(player.sprite, enemies, False) or
                   pygame.sprite.spritecollide(player.sprite, badlaser, False)) and inv_frames <= 0:
                    lives -= 1
                    inv_frames = 120

                # Adding enemies
                if game_timer % 250 == 0:
                    attack_pattern1(enemies, width, height, random.randint(0, height))

                if game_timer % 350 == 0:
                    attack_pattern2(enemies, width, height, random.randint(0, height))

                if random.randint(0, game_timer+1000) <= 50:
                    badlaser.add(EnemyBullets(width, height, random.uniform(height*0.1, height*0.9)))

                if pygame.sprite.groupcollide(laser, aliens, True, False):
                    alien_shot = True
                    score += 50

                if game_timer % 400 == 0:
                    aliens.add(Alien(width, height))
                else:
                    for alien in aliens:
                        if alien_cooldown <= 0:
                            badlaser.add(EnemyLasers(alien.rect.centerx, alien.rect.centery, width, height, True))
                            if dif == "EASY":
                                alien_cooldown = 50
                            elif dif == "NORMAL":
                                alien_cooldown = 30
                            else:
                                alien_cooldown = 10
                alien_cooldown -= 1
                invincibility(inv_frames, player.sprite)

                # Drawing non - sprites
                # pygame.draw.rect(screen, "#FFFFFF", div_rect)
                screen.blit(bg_surface, (0, 0))
                # pygame.draw.rect(screen, "White", div_rect)
                screen.blit(score_surface, score_rect)
                score_surface = font2.render(str(score), True, (60, 60, 200), (10, 10, 10)).convert_alpha()

                inv_frames -= 1
                # Sprites drawing and updating
                player1_lives.draw(screen)
                player1_lives.update(lives, inv_frames)
                laser.draw(screen)
                laser.update()
                aliens.update(player.sprite.rect.centerx, player.sprite.rect.centery, player.sprite.rect.centerx,
                              player.sprite.rect.centery, alien_shot)

                aliens.draw(screen)
                enemies.draw(screen)
                enemies.update()

                badlaser.draw(screen)
                badlaser.update()

            if lives > 0:
                player.draw(screen)
                player.update(lives)
            else:
                game_state = 2

        elif game_state == 2:
            # Game Over screen
            screen.fill("black")
            screen.blit(game_over, (width / 4, height / 2))
            screen.blit(score_surface, (width / 2.5, height / 4))
            keys = pygame.key.get_pressed()
            score = 0
            laser.empty()  # Deletes all sprites on screen
            enemies.empty()
            badlaser.empty()
            if keys[pygame.K_RETURN]:
                select = 0
                start_delay = 30
                score = 0
                lives = 3
                inv_frames = 0
                game_state = 0
                player.sprite.rect.centery = 200  # Reset ship pos
                player.sprite.rect.centerx = 100

        elif game_state == 3:
            # Settings screen
            keys = pygame.key.get_pressed()
            screen.fill((0, 0, 0))
            settings.update(set_row, set_col, set_delay)
            settings.draw(screen)
            marker.update()
            marker.draw(screen)
            screen.blit(settings_text, settings_rect)
            screen.blit(back_surf, (width / 1.2, height / 16))
            screen.blit(cog_surf, (width / 2, height / 16))
            set_delay -= 1

            # Menu input
            if keys[pygame.K_BACKSPACE] or keys[pygame.K_ESCAPE]:
                game_state = 0
                set_row = 0
                set_col = 0
            if set_row == 1 and (keys[pygame.K_SPACE] or keys[pygame.K_RETURN]):
                show_message("Restart required", "Restarting program", 1)
                pygame.quit()
                login.restart()

        # Level transition screen
        elif game_state == 4:

            screen.fill((0, 0, 0))
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

        # Versus mode gameplay
        elif game_state == 5:
            inv_frames -= 1
            inv_frames_b -= 1
            game_timer -= 1
            alien_shot = False

            keys = pygame.key.get_pressed()

            if keys[pygame.K_SPACE] and cooldown < 1:  # Shooting input + max fire rate
                laser.add(Lasers(player1.sprite.rect.centerx, player1.sprite.rect.centery, width, height, True))
                cooldown = 20
            cooldown -= 1

            if keys[pygame.K_KP0] and cooldown_b < 1:  # Shooting input + max fire rate
                laser2.add(Lasers(player2.sprite.rect.centerx, player2.sprite.rect.centery, width, height, True))
                cooldown_b = 20
            cooldown_b -= 1

            if (pygame.sprite.spritecollide(player1.sprite, enemies, False) and inv_frames <= 0
                    or pygame.sprite.spritecollide(player1.sprite, aliens, False) and inv_frames <= 0
                    or pygame.sprite.spritecollide(player1.sprite, badlaser, False) and inv_frames <= 0):
                lives -= 1
                inv_frames = 120

            if (pygame.sprite.spritecollide(player2.sprite, enemies, False) and inv_frames_b <= 0
                    or pygame.sprite.spritecollide(player2.sprite, aliens, False) and inv_frames_b <= 0
                    or pygame.sprite.spritecollide(player2.sprite, badlaser, False) and inv_frames_b <= 0):
                lives_b -= 1
                inv_frames_b = 120

            invincibility(inv_frames, player1.sprite)
            invincibility(inv_frames_b, player2.sprite)

            if game_timer < 1:
                game_state = 6

            if len(laser2) > 0:
                for lase in laser2:
                    temp = pygame.image.load("graphics/laser.png")
                    temp.fill("#00a6e4")
                    lase.image = pygame.transform.scale(temp, (width / 40, height / 160))

            if pygame.sprite.groupcollide(laser, enemies, True, True):
                score += 10

            if pygame.sprite.groupcollide(laser2, enemies, True, True):
                score2 += 10

            if pygame.sprite.groupcollide(laser, aliens, True, False):
                alien_shot = True
                score += 50

            if pygame.sprite.groupcollide(laser2, aliens, True, False):
                alien_shot = True
                score2 += 50

            if random.randint(0, 50) == 0:
                enemies.add(Asteroids(width, height, width*1.1, random.uniform(height*0.1, height*0.5)))
                enemies.add(Asteroids(width, height, width * 1.1, random.uniform(height*0.6, height*0.9)))

            if game_timer % 300 == 0 and game_timer < 3500:
                aliens.add(Alien(width, height))

            else:
                for alien in aliens:
                    if alien_cooldown <= 0:
                        badlaser.add(EnemyLasers(alien.rect.centerx, alien.rect.centery, width, height, True))
                        if dif == "EASY":
                            alien_cooldown = 50
                        elif dif == "NORMAL":
                            alien_cooldown = 30
                        else:
                            alien_cooldown = 10

            alien_cooldown -= 1

            score_surface = font2.render(str(score), True, (60, 60, 200), (10, 10, 10)).convert_alpha()
            score2_surface = font2.render(str(score2), True, (60, 60, 200), (10, 10, 10)).convert_alpha()

            timer_surf = font2.render(str(game_timer // 60), True, (20, 200, 20), (0, 0, 50)).convert_alpha()

            screen.fill((0, 0, 0))

            screen.blit(score_surface, score_rect)
            screen.blit(score2_surface, score2_rect)

            enemies.update()
            enemies.draw(screen)
            aliens.update(player1.sprite.rect.centerx, player1.sprite.rect.centery, player2.sprite.rect.centerx,
                          player2.sprite.rect.centery, alien_shot)
            aliens.draw(screen)

            player1_lives.draw(screen)
            player1_lives.update(lives, inv_frames)
            player2_lives.draw(screen)
            player2_lives.update(lives_b, inv_frames_b)
            badlaser.draw(screen)
            badlaser.update()
            laser.draw(screen)
            laser2.draw(screen)
            laser.update()
            laser2.update()

            player1.draw(screen)
            player1.update(lives)
            player2.draw(screen)
            player2.update(lives_b)

            pygame.draw.rect(screen, "#FFFFFF", div_rect)
            screen.blit(timer_surf, timer_rect)

            if lives == 0 or lives_b == 0 or game_timer <= 0:
                game_state = 6

        # Versus mode end screen
        elif game_state == 6:
            keys = pygame.key.get_pressed()

            if lives_b == 0:
                screen.fill("red")
            elif lives == 0:
                screen.fill("blue")
            else:
                if score > score2:
                    # Plr 1 victory
                    screen.fill("red")
                elif score2 > score:
                    # Plr 2 victory
                    screen.fill("blue")
                else:
                    # Draw
                    screen.fill("black")

            laser.empty()  # Deletes all sprites on screen
            laser2.empty()
            enemies.empty()
            badlaser.empty()
            aliens.empty()

            if keys[pygame.K_RETURN]:
                start_delay = 30
                select = 0
                score = 0
                lives = 3
                inv_frames = 0
                inv_frames_b = 0
                game_state = 0
                player.sprite.rect.centery = height / 5  # Reset ship pos
                player.sprite.rect.centerx = width / 10

        elif game_state == 7:
            # Versus mode setup
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP] and not timer_change and game_timer < 7200:
                game_timer += 60
                timer_change = True
            if keys[pygame.K_DOWN] and not timer_change and game_timer > 60:
                game_timer -= 60
                timer_change = True
            if not (keys[pygame.K_UP] or keys[pygame.K_DOWN]):
                timer_change = False

            if keys[pygame.K_BACKSPACE] or keys[pygame.K_ESCAPE]:
                game_state = 0

            aliens.empty()
            lives = 3
            lives_b = 3
            score = 0
            score2 = 0
            timer_surf = font2.render(str(game_timer // 60), True, (20, 200, 20), (0, 0, 50)).convert_alpha()
            player1.sprite.rect.center = (width / 10, height / 4)
            player2.sprite.rect.center = (width / 10, height / 1.25)
            dif = get_setting("difficulty").upper()
            screen.fill("black")
            screen.blit(timer_surf, timer_rect)
            if keys[pygame.K_RETURN] and start_delay < 0:
                game_state = 5
            start_delay -= 1

        elif game_state == 8:
            # Highscores screen
            keys = pygame.key.get_pressed()
            menu_text = font2.render("HIGHSCORES", False, (200, 200, 200), (0, 0, 0))
            menu_rect = menu_text.get_rect(center=(width / 2, height / 7))

            if keys[pygame.K_BACKSPACE] or keys[pygame.K_ESCAPE]:
                game_state = 0

            screen.fill("black")
            screen.blit(menu_text, menu_rect)
            hs_rows.draw(screen)
            hs_rows.update()
        elif game_state == 9:
            screen.fill("pink")
            if not saved:
                enter_score(name, score, get_date())

        # Update everything
        pygame.display.update()
        clock.tick(60)  # Caps at 60 fps


def invincibility(inv_frames, sprite):
    # Invincibility frames flashing animation
    # Pycharm marks the passing of a sprite as a warning: "Expected type 'Player', got 'Sprite' instead"
    # but the program still functions normally with no errors.
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


def attack_pattern1(sprite_group, width, height, y):
    sprite_group.add(Asteroids(width, height, width * 1.1, y))
    sprite_group.add(Asteroids(width, height, width * 1.25, y))
    sprite_group.add(Asteroids(width, height, width * 1.4, y))


def attack_pattern2(sprite_group, width, height, y):
    sprite_group.add(Asteroids(width, height, width * 1.1, y-0.2*height))
    sprite_group.add(Asteroids(width, height, width * 1.1, y))
    sprite_group.add(Asteroids(width, height, width * 1.1, y+0.2*height))


def setup():
    if is_first_launch():
        load_defaults()
    remember_launch()


if __name__ == "__main__":
    setup()
    play("LOUIS1")
