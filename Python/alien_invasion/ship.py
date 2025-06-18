"""This module has the ship class. It controls all aspects of the spaceship."""

import pygame
from settings import Settings

class Ship():
    """A class for the player object i.e., spaceship"""

    def __init__(self, screen, game_set):
        """Initialize the spaceship and its starting position"""

        self.screen = screen
        self.game_settings = game_set

        #Load the ship image and get its rect
        self.image = pygame.image.load(r'alien_invasion\images\small_ship.png')

        self.rect = self.image.get_rect()
        self.screen_rect = self.screen.get_rect()

        # Start each new ship at the bottom center of the screen.
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        self.moving_left = False
        self.moving_right = False


    def update(self):
        if self.moving_left == True and self.rect.left >= self.screen_rect.left:
            self.rect.centerx -= self.game_settings.ship_speed
        if self.moving_right == True and self.rect.right <= self.screen_rect.right:
            self.rect.centerx += self.game_settings.ship_speed

    def blitme(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """Center the ship on the screen."""

        self.rect.centerx = self.screen_rect.centerx
