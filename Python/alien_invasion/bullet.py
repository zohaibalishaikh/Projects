"""A module about bullets"""

import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """A class to manage bullets fired from the ship."""

    def __init__(self, game_settings, screen, ship):
        super().__init__()
        self.screen = screen
        self.screen_rect = screen.get_rect()       
        self.color = game_settings.bullet_color
        self.speed_factor = game_settings.bullet_speed

        #Create a rect and position it at (0, 0) and then set at correct position
        self.rect = pygame.Rect(0, 0, game_settings.bullet_width, game_settings.bullet_height)

        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top
        self.y = float(self.rect.y)

    def update(self):
        """This function will move the bullet upwards."""
        #Update the decimal position of the bullet
        self.y -= self.speed_factor
        #Update the rect position
        self.rect.y = self.y

    def draw_bullet(self):
        """Draw the bullet on the screen"""
        pygame.draw.rect(self.screen, self.color, self.rect)
