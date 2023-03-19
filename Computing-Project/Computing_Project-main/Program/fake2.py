from sys import exit

import login
from HighscoresData import *
from dates import *
from messages import *
import os

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"  # Hides pygame welcome message, must be before pygame import
from sprites import *


def play(name):
    pygame.init()
    width = 960
    height = 540

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

    bg = pygame.sprite.GroupSingle()
    bg.add(Background(width, height, 1))

    player = pygame.sprite.GroupSingle()
    player.add(Player(width, height))
    player1 = pygame.sprite.GroupSingle()
    player1.add(PlayerA(width, height))
    player2 = pygame.sprite.GroupSingle()
    player2.add(PlayerB(width, height))
    star = pygame.sprite.GroupSingle()
    star.add(Pickup(width, height))

    player1_lives = pygame.sprite.GroupSingle()
    player1_lives.add(Hearts(width, height, True))
    player2_lives = pygame.sprite.GroupSingle()
    player2_lives.add(Hearts(width, height, False))

    message = pygame.sprite.GroupSingle()
    message.add(Texts(width, height, "word", font2, 0.1))

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

    # name_list = get_names()
    # score_list = get_scores()

    # for i in range(5):
    #     hs_rows.add(HighscoreRow(i, width, height, name_list[i], score_list[i]))

    # dif = get_setting("difficulty").upper()
    dif = get_setting("difficulty").upper()

    if dif == "EASY":
        lives = 5
        lives_b = 5
    elif dif == "NORMAL":
        lives = 3
        lives_b = 3
    else:
        lives = 2
        lives_b = 2

    # initialise variables

    score2 = 0
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
    timer_change = False
    saved = False
    bg_changed = False
    boss_active = False

    while play_game:  # Game loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and game_state == 0:
                if event.key == pygame.K_UP:
                    if select > 0:
                        select -= 1
                    else:
                        select = 4

                if event.key == pygame.K_DOWN:
                    if select < 4:
                        select += 1
                    else:
                        select = 0

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
            if event.type == pygame.KEYDOWN and (game_state == 1):
                if event.key == pygame.K_ESCAPE:
                    game_state = 10
                    text_delay = 40
            if event.type == pygame.KEYDOWN and (game_state == 10):
                if event.key == pygame.K_ESCAPE and text_delay <= 0:
                    game_state = 1
                if event.key == pygame.K_BACKSPACE and text_delay <= 0:
                    game_state = 0

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

            hs_rows.empty()
            hs_rows = update_scores(hs_rows, width, height)

            if (keys[pygame.K_RETURN] or keys[pygame.K_SPACE]) and select == 0 and start_delay <= 0:  # Play game
                saved = False
                boss_active = False
                dif = get_setting("difficulty").upper()
                if dif == "EASY":
                    lives = 5
                elif dif == "NORMAL":
                    lives = 3
                else:
                    lives = 2

                i = 0
                text_delay = 0
                level = 1
                game_timer = 2700  # 45 seconds
                level_text = font2.render("", False, (255, 255, 255), (0, 0, 0))
                score_rect = score_surface.get_rect(center=(width / 2, height / 10))
                score = 0
                game_state = 4
                player.sprite.position.x = height / 2  # Reset ship pos
                player.sprite.position.y = width / 10
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
                score_rect = score_surface.get_rect(center=(width / 2, height / 10))
                score2_rect = score2_surface.get_rect(center=(width / 2, height / 1.5))

            if (keys[pygame.K_RETURN] or keys[pygame.K_SPACE]) and select == 3 and start_delay <= 0:
                game_state = 8

            if (keys[pygame.K_RETURN] or keys[pygame.K_SPACE]) and select == 4 and start_delay <= 0:
                pygame.quit()
                # Logs off the user
                # login2 = login.LoginWindow()
                # login2.mainloop()
                return ()
            start_delay -= 1

        # Gameplay
        elif game_state == 1:
            bg_changed = False
            hide_star = False
            game_timer -= 1
            keys = pygame.key.get_pressed()

            if game_timer <= 1:
                game_timer = 3600  # 60 seconds
                text_delay = 0
                level_text = font2.render("", False, (255, 255, 255), (0, 0, 0))
                i = 0
                if level == 3:
                    game_state = 9
                else:
                    game_state = 4
                level += 1

            if keys[pygame.K_SPACE] and cooldown < 1:  # Shooting input + max fire rate
                laser.add(Lasers(player.sprite.rect.centerx, player.sprite.rect.centery, width, height, True))
                if dif == "HARD":
                    cooldown = 18
                elif dif == "NORMAL":
                    cooldown = 14
                else:
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

            if game_timer % 421 == 0:
                aliens.add(Alien(width, height, "normal"))
            elif game_timer % 579 == 0 and dif == "HARD":
                aliens.add(Alien(width, height, "normal"))

            else:
                for alien in aliens:
                    if alien_cooldown <= 0 and alien.__getattribute__("type") == "normal":
                        badlaser.add(EnemyLasers(alien.rect.centerx, alien.rect.centery, width, height, True))

                        if dif == "EASY":
                            alien_cooldown = 50
                        elif dif == "NORMAL":
                            alien_cooldown = 30
                        else:
                            alien_cooldown = 20
                    if (alien.__getattribute__("type") == "boss") and ((0 >= boss_timer >= -150) or
                                                                       (-250 >= boss_timer >= -2000)) and \
                            boss_timer % 3 == 0:
                        badlaser.add(EnemyLasers(alien.rect.centerx,
                                                 alien.rect.centery + (height / random.randint(7, 9)), width, height,
                                                 False))
                        badlaser.add(EnemyLasers(alien.rect.centerx,
                                                 alien.rect.centery - (height / random.randint(7, 9)), width, height,
                                                 False))

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
            aliens.update(player.sprite.rect.centerx, player.sprite.rect.centery, player.sprite.rect.centerx,
                          player.sprite.rect.centery, game_timer)

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
            # Game Over screen
            if not saved:
                enter_score(name, score, get_date())
                saved = True

            keys = pygame.key.get_pressed()
            screen.fill("black")
            screen.blit(game_over, (width / 4, height / 2))
            screen.blit(score_surface, (width / 2.5, height / 4))

            score = 0
            level = 1
            bg_changed = False
            laser.empty()  # Deletes all sprites on screen
            enemies.empty()
            aliens.empty()
            badlaser.empty()

            if keys[pygame.K_RETURN]:
                select = 0
                start_delay = 30
                score = 0
                inv_frames = 0
                game_state = 0
                player.sprite.position.x = height / 2  # Reset ship pos
                player.sprite.position.y = width / 10

        elif game_state == 3:
            # Settings screen
            keys = pygame.key.get_pressed()
            colour = False
            set_delay -= 1

            # Menu input
            settings.update(set_row, set_col, set_delay)
            if keys[pygame.K_RETURN] or keys[pygame.K_SPACE]:
                colour = True

            if keys[pygame.K_BACKSPACE] or keys[pygame.K_ESCAPE]:
                game_state = 0
                set_row = 0
                set_col = 0
            if set_row == 1 and (keys[pygame.K_SPACE] or keys[pygame.K_RETURN]):
                show_message("Restart required", "Restarting program", 1)
                pygame.quit()
                login.restart(name)

            screen.fill((0, 0, 0))
            settings.draw(screen)
            marker.update(colour)
            marker.draw(screen)
            screen.blit(settings_text, settings_rect)
            screen.blit(back_surf, (width / 1.2, height / 16))
            screen.blit(cog_surf, (width / 2, height / 16))

        # Level transition screen
        elif game_state == 4:
            screen.fill((0, 0, 0))

            if not bg_changed:
                bg.empty()
                bg.add(Background(width, height, level))
                bg_changed = True

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
            keys = pygame.key.get_pressed()
            inv_frames -= 1
            inv_frames_b -= 1
            game_timer -= 1

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

            # Alien hit detection
            for n in laser:
                for alien in aliens:
                    if pygame.sprite.collide_rect(n, alien):
                        n.kill()
                        alien.__setattr__("lives", alien.__getattribute__("lives") - 1)
                        if alien.__getattribute__("lives") <= 0:
                            score += 100


            for n in laser2:
                for alien in aliens:
                    if pygame.sprite.collide_rect(n, alien):
                        n.kill()
                        alien.__setattr__("lives", alien.__getattribute__("lives") - 1)
                        if alien.__getattribute__("lives") <= 0:
                            score2 += 100

            if random.randint(0, 50) == 0:
                enemies.add(Asteroids(width, height, width * 1.1, random.uniform(height * 0.1, height * 0.5)))
                enemies.add(Asteroids(width, height, width * 1.1, random.uniform(height * 0.6, height * 0.9)))

            if game_timer % 300 == 0 and game_timer < 3500:
                aliens.add(Alien(width, height, "normal"))

            else:
                for alien in aliens:
                    if alien_cooldown <= 0:
                        badlaser.add(EnemyLasers(alien.rect.centerx, alien.rect.centery, width, height, True))
                        if get_setting("difficulty").upper() == "EASY":
                            alien_cooldown = 60
                        elif get_setting("difficulty") == "NORMAL":
                            alien_cooldown = 40
                        else:
                            alien_cooldown = 20

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
                          player2.sprite.rect.centery, game_timer)
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
                # Plr 1 victory
                screen.fill("red")
                message.update("Red wins!", font2, 0.2, True)
                message.draw(screen)
            elif lives == 0:
                # Plr 2 victory
                screen.fill("blue")
                message.update("Blue wins!", font2, 0.2, True)
                message.draw(screen)
            else:
                if score > score2:
                    # Plr 1 victory
                    screen.fill("red")
                    message.update("Red wins!", font2, 0.2, True)
                    message.draw(screen)

                elif score2 > score:
                    # Plr 2 victory
                    screen.fill("blue")
                    message.update("Blue wins!", font2, 0.2, True)
                    message.draw(screen)
                else:
                    # Draw
                    screen.fill("black")
                    message.update("Draw", font2, 0.2, True)
                    message.draw(screen)

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
                game_state = 5 # This will be changed to 0 when the menu is added. For now it resets the versus game.
                player1.sprite.position.x = height / 5  # Reset ship pos
                player1.sprite.position.y = width / 10

        elif game_state == 7:
            # Versus mode setup
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP] and not timer_change and game_timer < 7200:
                game_timer += 300
                timer_change = True
            if keys[pygame.K_DOWN] and not timer_change and game_timer > 300:
                game_timer -= 300
                timer_change = True
            if not (keys[pygame.K_UP] or keys[pygame.K_DOWN]):
                timer_change = False

            if keys[pygame.K_BACKSPACE] or keys[pygame.K_ESCAPE]:
                game_state = 0

            aliens.empty()
            dif = get_setting("difficulty").upper()

            if dif == "EASY":
                lives = 5
                lives_b = 5
            elif dif == "NORMAL":
                lives = 3
                lives_b = 3
            else:
                lives = 2
                lives_b = 2

            score = 0
            score2 = 0
            timer_surf = font2.render(str(game_timer // 60), True, (20, 200, 20), (0, 0, 50)).convert_alpha()
            player1.sprite.rect.center = (width / 10, height / 4)
            player2.sprite.rect.center = (width / 10, height / 1.25)

            screen.fill("black")
            screen.blit(timer_surf, timer_rect)
            message.update("Set timer", font2, 0.14, True)
            message.sprite.rect.centery = height/4
            message.draw(screen)

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
            # Win screen
            keys = pygame.key.get_pressed()
            game_timer += 1

            screen.fill("black")
            score_rect = score_surface.get_rect(center=(width / 2, height / 1.5))

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
            if not saved:
                enter_score(name, score, get_date())
                saved = True
            if keys[pygame.K_RETURN]:
                game_state = 0
                start_delay = 30

        # Pause screen
        elif game_state == 10:
            text_delay -= 1
            message.update("PAUSED", font1, 0.15, True)
            message.draw(screen)

        # Update everything
        pygame.display.update()
        clock.tick(66)  # Caps at 60 fps


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


def update_scores(hs_rows, width, height):
    name_list = get_names()
    score_list = get_scores()

    for i in range(5):
        hs_rows.add(HighscoreRow(i, width, height, name_list[i], score_list[i]))

    return hs_rows


def setup():
    if is_first_launch():
        load_defaults()
        create_h_table()
    remember_launch()


if __name__ == "__main__":
    play("Guest")