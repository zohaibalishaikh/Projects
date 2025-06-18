"""Alien invasion game."""

import pygame
from pygame.sprite import Group
from settings import Settings
from ship import Ship
import game_functions as gf
from game_stats import GameStats
from alien import Alien
from button import Button
from scoreboard import Scoreboard

def run_game():
    """Initialize game a create a screen object."""

    pygame.init()
    game_settings = Settings()
    #Game screen
    screen = pygame.display.set_mode((game_settings.screen_width, game_settings.screen_height))
    #Space ship
    spaceship = Ship(screen, game_settings)
    
    #Group of bullets
    bullets = Group()
    #Group of aliens
    aliens = Group()

    #Create a fleet of aliens
    gf.create_fleet(game_settings, screen, spaceship, aliens)

    pygame.display.set_caption("Alien Invasion")

    # Make the play button
    play_button = Button(game_settings, screen, "Play")

    # Make the High scores button
    hs_button = Button(game_settings, screen, "High scores", 150, 30, (play_button.rect.x + 25, play_button.rect.bottom + 10), None, (0, 0, 200))

    # Create an instance to store game statistics.
    stats = GameStats(game_settings)

    # Create a score board
    sb = Scoreboard(game_settings, screen, stats)

    #Start the main loop for the game

    while True:
        #Check for events
        gf.check_events(game_settings, spaceship, screen, stats, bullets, aliens, sb, play_button, hs_button)

        if stats.game_active:
            gf.update_ship(spaceship)
            gf.update_bullets(bullets, aliens)
            gf.check_bullet_alien_collision(game_settings, screen, spaceship, aliens, bullets, stats, sb)
            gf.update_aliens(aliens)
            gf.check_aliens_hit_bottom(game_settings, stats, screen, spaceship, aliens, bullets)
            gf.check_ship_hit(game_settings, stats, screen, spaceship, aliens, bullets)
        
        gf.update_screen(game_settings, screen, stats, spaceship, bullets, aliens, sb, play_button, hs_button)

run_game()