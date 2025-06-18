"""This module handles all the game functions"""

import sys
import pygame
import json
from bullet import Bullet
from alien import Alien
from time import sleep

def fire_bullet(game_settings, screen, ship, bullets):
    #Create a new bullet and add it to the group
    if len(bullets) < game_settings.bullets_allowed:
        new_bullet = Bullet(game_settings, screen, ship)
        bullets.add(new_bullet)

def check_keydown_events(event, game_settings, ship, screen, bullets):

    if event.key == pygame.K_RIGHT:
        #Start moving the ship to right
        ship.moving_right = True

    elif event.key == pygame.K_LEFT:
        #Start moving the ship to left
        ship.moving_left = True

    elif event.key == pygame.K_SPACE:
        fire_bullet(game_settings, screen, ship, bullets)

    elif event.key == pygame.K_q:
        sys.exit()

def check_keyup_events(event, game_settings, ship):

    if event.key == pygame.K_RIGHT:
        #Stop moving the ship to right
        ship.moving_right = False

    elif event.key == pygame.K_LEFT:
        #Stop moving the ship to left
        ship.moving_left = False

def reset_settings(settings):
    settings.ship_speed = 2
    settings.bullet_speed = 2
    settings.alien_speed = 1
    settings.alien_drop_speed = 50
    #Right direction is denoted by 1 and left by -1
    settings.alien_direction = 1
    settings.alien_points = 50

def new_game_start(stats, settings, ship, screen, bullets, aliens, sb):
    if not stats.game_active:
        # Reset statistics and activate game
        stats.reset_stats()
        stats.game_active = True

        # Reset the score board
        sb.prep_score()
        sb.prep_highscore()
        sb.prep_level()

        # Remove existing aliens and bullets
        aliens.empty()
        bullets.empty()

        reset_settings(settings)

        # Create new fleet of aliens
        create_fleet(settings, screen, ship, aliens)

        # Center the ship
        ship.center_ship()

def show_highscores(stats, screen, settings):
    """Show top 5 highscores"""
    heading_font = pygame.font.SysFont(None, 48)
    text_font = pygame.font.SysFont(None, 24)
    close_window = False
    text = []
    
    for highscore in stats.hall_of_fame:
        text.append(str(highscore))

    text.append("Press x to close")

    screen_rect = screen.get_rect()
    
    # Build the highscore windows's rect object and center it.
    window_rect = pygame.Rect(0, 0, settings.hs_window_width, settings.hs_window_height)
    window_rect.center = screen_rect.center

    # Draw the highscore window first.
    screen.fill(settings.hs_bg_color, window_rect)

    # Create the highscore image
    text_img = heading_font.render("HALL OF FAME", True, settings.hs_text_color, settings.hs_bg_color)

    # Position the headline in center anchored to the highscore window
    image_rect = text_img.get_rect()
    image_rect.centerx = window_rect.centerx
    image_rect.top = window_rect.top + image_rect.height

    # Draw the headline line-by-line
    screen.blit(text_img, image_rect)

    # Text vertical position below headline
    text_top = image_rect.bottom + 15

    for line in text:

        # Create the highscore image
        text_img = text_font.render(line, True, settings.hs_text_color, settings.hs_bg_color)

        # Position the text in center anchored to the highscore window
        image_rect = text_img.get_rect()
        image_rect.centerx = window_rect.centerx
        image_rect.top = text_top + image_rect.height

        # Draw the text line-by-line
        screen.blit(text_img, image_rect)

        # Add a gap between lines
        text_top += 30

    while not close_window:
        # Keep updating the same screen until the key x is pressed.
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_x:
                close_window = True
                break



def button_operation(button, stats, settings, ship, screen, bullets, aliens, sb):
    if button.msg == "Play":
        new_game_start(stats, settings, ship, screen, bullets, aliens, sb)
    elif button.msg == "High scores":
        show_highscores(stats, screen, settings)


def check_events(game_settings, ship, screen, stats, bullets, aliens, sb, *buttons):
    """Check for an event and take appropriate action"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()

            for button in buttons:
                if button.rect.collidepoint(mouse_x, mouse_y):
                    button_operation(button, stats, game_settings, ship, screen, bullets, aliens, sb)
                    break

        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, game_settings, ship, screen, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, game_settings, ship)


def update_screen(game_settings, screen, stats, spaceship, bullets, aliens, scoreboard, *buttons):
    #Redraw screen on each iteration
    screen.fill(game_settings.bg_color)
    spaceship.blitme()

    for bullet in bullets.sprites():
        bullet.draw_bullet()

    aliens.draw(screen)

    scoreboard.draw_score()

    if not stats.game_active:
        for button in buttons:
            button.draw_button()
    
    #Make the most recently drawn screen visible
    pygame.display.flip()

def update_bullets(bullets, aliens):
    """This function updates the bullets position and remove disappeared bullets"""
    
    bullets.update()

    #Remove disappeared bullets
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

def check_bullet_alien_collision(game_settings, screen, ship, aliens, bullets, stats, scoreboard):
    """Respond to the bullet alien collision"""
    
    # Check if a bullet has hit an alien, if so get rid of the bullet and the alien
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        for aliens in collisions.values():
            stats.score += game_settings.alien_points * len(aliens)
            scoreboard.prep_score()
        check_high_score(stats, scoreboard)

    if len(aliens) == 0:
        # Destroy existing bullets if aliens are eradicated
        bullets.empty()
        game_settings.level_up()
        stats.level += 1
        scoreboard.prep_level()
        create_fleet(game_settings, screen, ship, aliens)

def check_ship_hit(game_settings, stats, screen, ship, aliens, bullets):
    # Look for a alien-ship collision.
    if pygame.sprite.spritecollideany(ship, aliens):
        # Decrement ships left
        stats.ships_left -= 1

        # Empty the list of aliens and bullets.
        aliens.empty()
        bullets.empty()

        # Create a new fleet and center the ship.
        create_fleet(game_settings, screen, ship, aliens)
        ship.center_ship()

        # Pause
        sleep(0.5)

    # Game Over
    if stats.ships_left <= 0:
        stats.game_active = False
        stats.update_hall_of_fame()

def check_aliens_hit_bottom(game_settings, stats, screen, ship, aliens, bullets):
    """Check if any aliens have reached the bottom of the screen."""

    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Decrement ships left
            stats.ships_left -= 1

            # Empty the list of aliens and bullets.
            aliens.empty()
            bullets.empty()

            # Create a new fleet and center the ship.
            create_fleet(game_settings, screen, ship, aliens)
            ship.center_ship()

            # Pause
            sleep(0.5)
            break

    if stats.ships_left <= 0:
        stats.game_active = False

def get_number_of_aliens(game_settings, screen, ship):
    """Calculate how many aliens can fit in a fleet depends on size of screen, alien, and ship"""
    # Create an alien and find the number of aliens in a fleet.
    # Spacing between each alien in a row/coloumn is equal to one alien width.
    alien = Alien(game_settings, screen)
    aliens_x = 0
    aliens_y = 0

    alien_width = alien.rect.width
    alien_height = alien.rect.height
    available_space_x = game_settings.screen_width - game_settings.alien_offsets_x * alien_width
    aliens_x = int(available_space_x / (2 * game_settings.alien_gap_x * alien_width))
    available_space_y = (game_settings.screen_height - ((game_settings.alien_offsets_y + game_settings.alien_ship_gap) * alien_height) - ship.rect.height)
    aliens_y = int(available_space_y / (2 * game_settings.alien_gap_y * alien_height))

    
    return (aliens_x, aliens_y)

def create_fleet(game_settings, screen, ship, aliens):
    """Create a full fleet of aliens"""

    aliens_in_a_row, number_rows = get_number_of_aliens(game_settings, screen, ship)

    for row_number in range(number_rows):
        # Create the a row of aliens.
        for alien_number in range(aliens_in_a_row):
            # Create an alien and place it in the row.
            alien = Alien(game_settings, screen)
            alien.x = alien.rect.width + 2 * alien.rect.width * alien_number
            alien.rect.x = alien.x
            alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
            aliens.add(alien)

def update_aliens(aliens):
    """update the aliens position"""

    aliens.update()

def update_ship(ship):
    """Update ship location"""

    ship.update()

def check_high_score(stats, sb):
    """Check to see if there's a new high score."""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_highscore()