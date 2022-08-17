# ============================================================================================================== #
#                                             GAME PROGRAM
# Written by: Louis Pattern     12/08/2022
# Known bugs:  none
# ============================================================================================================== #

from sys import exit
from sprites import *
# from messages import *
from settings import *
import login


def play():
    pygame.init()
    width = int(get_setting("WIDTH"))
    height = int(get_setting("HEIGHT"))

    # 960 x 600
    screen = pygame.display.set_mode((width, height))  # Game window
    pygame.display.set_caption("Space Game")
    clock = pygame.time.Clock()

    font1 = pygame.font.Font("graphics/fonts/ARCADE_I.ttf", round(width / 19))
    font2 = pygame.font.Font("graphics/fonts/ARCADE_N.ttf", round(width / 19))
    score = 0
    level = 1
    versus_timer = 3600

    div_rect = pygame.Rect(0, height / 2.1, width * 2, height / 25)

    text_surface = font1.render("SPACE GAME", True, (180, 10, 10))
    text_rect = text_surface.get_rect(center=(width / 2, height / 8))
    game_over = font2.render("GAME OVER", True, (255, 0, 0))
    menu_text = font2.render("MENU", False, (200, 200, 200), (0, 0, 0))
    menu_rect = menu_text.get_rect(center=(width / 2, height / 4))
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
    timer_surf = font2.render(str(versus_timer//60), True, (20, 200, 20)).convert_alpha()
    timer_rect = timer_surf.get_rect(center=(width/2, height/2))

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
    ast = pygame.sprite.Group()
    options = pygame.sprite.Group()
    settings = pygame.sprite.Group()
    marker = pygame.sprite.Group()

    badlaser = pygame.sprite.Group()

    buttons = ["play", "settings", "versus", "highscores", "exit"]
    set_buttons = ["difficulty", "resolution", "colourblind", "controls"]

    for i in range(2):
        marker.add(SettingMarker(i, width, height))

    for i in buttons:
        options.add(Option(i, width, height))
    for i in set_buttons:
        settings.add(Settings(i, width, height))

    score2 = 0

    lives = 3
    lives_b = 3
    inv_frames = 0
    inv_frames_b = 0
    cooldown = 0
    cooldown_b = 0
    game_state = 0
    select = 0
    set_row = 0
    set_col = 0
    start_delay = 30

    set_delay = 10
    play_game = True

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
            screen.fill((0, 0, 0))
            screen.blit(menu_text, menu_rect)
            screen.blit(text_surface, text_rect)
            options.update(select)
            options.draw(screen)
            score = 0

            if (keys[pygame.K_RETURN] or keys[pygame.K_SPACE]) and select == 0 and start_delay <= 0:  # Play game
                i = 0
                text_delay = 0
                level_text = font2.render("", False, (255, 255, 255), (0, 0, 0))
                score = 0
                game_state = 4
                player.sprite.rect.centery = height / 2  # Reset ship pos
                player.sprite.rect.centerx = width / 10

            if (keys[pygame.K_RETURN] or keys[pygame.K_SPACE]) and select == 1 and start_delay <= 0:
                # Takes to settings screen
                game_state = 3
                set_delay = 10

            if (keys[pygame.K_RETURN] or keys[pygame.K_SPACE]) and select == 2 and start_delay <= 0:
                # Takes to versus mode
                versus_timer = 3600
                game_state = 5

            if (keys[pygame.K_RETURN] or keys[pygame.K_SPACE]) and select == 4 and start_delay <= 0:
                pygame.quit()
                # Logs off the user
                login2 = login.LoginWindow()
                login2.mainloop()
                return ()

            start_delay -= 1

        # Gameplay
        elif game_state == 1:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE] and cooldown < 1:  # Shooting input + max fire rate
                laser.add(Lasers(player.sprite.rect.centerx, player.sprite.rect.centery, width, height))
                cooldown = 15
            cooldown -= 1

            # Collision Detection
            if pygame.sprite.groupcollide(laser, ast, True, True):
                score += 10

            if (pygame.sprite.spritecollide(player.sprite, ast, False) or
                    pygame.sprite.spritecollide(player.sprite, badlaser, False)) and inv_frames <= 0:
                # game_state = 2
                lives -= 1
                inv_frames = 120

            if random.randint(0, 30) == 0:
                ast.add(Enemies(width, height, 0, height))
            if random.randint(0, 15) == 0:
                badlaser.add(EnemyLasers(width, random.randint(0, height), width, height))

            # Invincibility frames flashing animation
            if inv_frames >= 0:
                if inv_frames >= 100:
                    Player.take_dmg2(player.sprite)
                elif inv_frames >= 80:
                    Player.take_dmg1(player.sprite)
                elif inv_frames >= 60:
                    Player.take_dmg2(player.sprite)
                elif inv_frames >= 40:
                    Player.take_dmg1(player.sprite)
                elif inv_frames >= 20:
                    Player.take_dmg2(player.sprite)
                else:
                    Player.take_dmg1(player.sprite)
            else:
                Player.take_dmg1(player.sprite)

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
            ast.draw(screen)
            ast.update()

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
            screen.blit(game_over, (360, 250))
            screen.blit(score_surface, (400, 150))
            keys = pygame.key.get_pressed()
            score = 0
            laser.empty()  # Deletes all sprites on screen
            ast.empty()
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

            # Menu imput
            if keys[pygame.K_BACKSPACE] or keys[pygame.K_ESCAPE]:
                game_state = 0
                set_row = 0
                set_col = 0

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
            versus_timer -= 1

            keys = pygame.key.get_pressed()

            if pygame.sprite.spritecollide(player1.sprite, ast, False) and inv_frames <= 0:
                lives -= 1
                inv_frames = 120

            if pygame.sprite.spritecollide(player2.sprite, ast, False) and inv_frames_b <= 0:
                lives_b -= 1
                inv_frames_b = 120

            if inv_frames >= 0:
                if inv_frames >= 100:
                    Player.take_dmg2(player1.sprite)
                elif inv_frames >= 80:
                    Player.take_dmg1(player1.sprite)
                elif inv_frames >= 60:
                    Player.take_dmg2(player1.sprite)
                elif inv_frames >= 40:
                    Player.take_dmg1(player1.sprite)
                elif inv_frames >= 20:
                    Player.take_dmg2(player1.sprite)
                else:
                    Player.take_dmg1(player1.sprite)
            else:
                Player.take_dmg1(player1.sprite)

            if inv_frames_b >= 0:
                if inv_frames_b >= 100:
                    Player.take_dmg2(player2.sprite)
                elif inv_frames_b >= 80:
                    Player.take_dmg1(player2.sprite)
                elif inv_frames_b >= 60:
                    Player.take_dmg2(player2.sprite)
                elif inv_frames_b >= 40:
                    Player.take_dmg1(player2.sprite)
                elif inv_frames_b >= 20:
                    Player.take_dmg2(player2.sprite)
                else:
                    Player.take_dmg1(player2.sprite)
            else:
                Player.take_dmg1(player2.sprite)

            if versus_timer < 1:
                game_state = 6

            if keys[pygame.K_SPACE] and cooldown < 1:  # Shooting input + max fire rate
                laser.add(Lasers(player1.sprite.rect.centerx, player1.sprite.rect.centery, width, height))
                cooldown = 15
            cooldown -= 1

            if keys[pygame.K_KP0] and cooldown_b < 1:  # Shooting input + max fire rate
                laser2.add(Lasers(player2.sprite.rect.centerx, player2.sprite.rect.centery, width, height))
                cooldown_b = 15
            cooldown_b -= 1

            if pygame.sprite.groupcollide(laser, ast, True, True):
                score += 10

            if pygame.sprite.groupcollide(laser2, ast, True, True):
                score2 += 10

            if random.randint(0, 40) == 0:
                ast.add(Enemies(width, height, height / 2, height))
                ast.add(Enemies(width, height, 0, height / 2))

            score_surface = font2.render(str(score), True, (60, 60, 200), (10, 10, 10)).convert_alpha()
            score2_surface = font2.render(str(score2), True, (60, 60, 200), (10, 10, 10)).convert_alpha()

            timer_surf = font2.render(str(versus_timer//60), True, (20, 200, 20), (0, 0, 50)).convert_alpha()

            screen.fill((0, 0, 0))

            screen.blit(score_surface, score_rect)
            screen.blit(score2_surface, score2_rect)

            ast.update()
            ast.draw(screen)
            player1_lives.draw(screen)
            player1_lives.update(lives, inv_frames)
            player2_lives.draw(screen)
            player2_lives.update(lives_b, inv_frames_b)
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

            if lives == 0 or lives_b == 0 or versus_timer <= 0:
                game_state = 6

        # Versus mode end screen
        else:
            keys = pygame.key.get_pressed()

            if lives_b == 0:
                screen.fill("red")
            elif lives == 0:
                screen.fill("blue")
            else:
                if score > score2:
                    screen.fill("red")
                elif score2 > score:
                    screen.fill("blue")
                else:
                    screen.fill("black")

            if keys[pygame.K_RETURN]:
                start_delay = 30
                select = 0
                score = 0
                lives = 3
                inv_frames = 0
                inv_frames_b = 0
                game_state = 0
                player.sprite.rect.centery = 200  # Reset ship pos
                player.sprite.rect.centerx = 100

        # Update everything
        pygame.display.update()
        clock.tick(60)  # Caps at 60 fps


def setup():
    if is_first_launch():
        load_defualts()
    remember_launch()


if __name__ == "__main__":
    setup()
    play()
