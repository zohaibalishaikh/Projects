"""A module to display score, highscore, level, current number of ships (aka lives)"""

import pygame

class Scoreboard():
    """A class to report scoring information"""

    def __init__(self, settings, screen, stats):
        """Initialize the scorekeeping attributes"""

        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.game_settings = settings
        self.stats = stats

        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)

        self.prep_score()
        self.prep_highscore()
        self.prep_level()

        # Create a ship icon to display no of ships left
        self.ship_icon = pygame.image.load(r'alien_invasion\images\smaller_ship.png')

        # Save the positions of ships beforehand.
        self.ship_positions = [(self.screen_rect.left + 10, self.score_rect.top),\
                               (self.screen_rect.left + 40, self.score_rect.top),\
                               (self.screen_rect.left + 70, self.score_rect.top)]

    def prep_score(self):
        """Turn the score into a rendered image."""

        score_str = "Score: {:,}".format(self.stats.score)
        self.score_image = self.font.render(score_str, True, self.text_color, self.game_settings.bg_color)

        # Display the score at the top right of the screen.
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_highscore(self):
        """Turn the high score in a rendered image."""
        high_score_str = "High Score: {:,}".format(self.stats.high_score)
        self.highscore_image = self.font.render(high_score_str, True, self.text_color, self.game_settings.bg_color)

        # Display the high score at the top center of the screen.
        self.highscore_rect = self.score_image.get_rect()
        self.highscore_rect.centerx = self.screen_rect.centerx
        self.highscore_rect.top = self.score_rect.top

    def prep_level(self):
        """Turn the level into a rendered image."""

        self.level_image = self.font.render(str(self.stats.level), True, self.text_color, self.game_settings.bg_color)

        # Display the level below the score.
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10     

    def draw_score(self):
        """Draw score to the screen"""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.highscore_image, self.highscore_rect)
        self.screen.blit(self.level_image, self.level_rect)

        for number in range(self.stats.ships_left):
            self.screen.blit(self.ship_icon, self.ship_positions[number])
