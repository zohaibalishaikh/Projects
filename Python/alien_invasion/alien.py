"""A module that controls all aspects of the alien ship"""

import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """A class to represent a single alien in the fleet."""

    def __init__(self, game_settings, screen):
        """Initialize the alien and its starting position."""
        super().__init__()
        self.screen = screen
        self.game_settings = game_settings

        #Load the alien image and set its attributes
        self.image = pygame.image.load(r'alien_invasion\images\small_alien_ufo.png')
        self.rect = self.image.get_rect()

        #start each new alien near the top left of the screen.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        #Store the alien's exact position
        self.x = float(self.rect.x)

        self.direction = game_settings.alien_direction

    def blitme(self):
        """Draw the alien at its current location"""
        self.screen.blit(self.image, self.rect)

    def is_out_of_screen(self):
        if self.rect.right >= self.screen.get_width() or self.rect.left <= 0:
            return True
        else:
            return False

    def update(self):
        """Move the alien"""

        self.x += (self.game_settings.alien_speed * self.direction)
        self.rect.x = self.x
        if self.is_out_of_screen() == True:
            self.direction *= -1
            self.rect.y += self.game_settings.alien_drop_speed

