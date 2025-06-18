"""A module for creating interactive buttons"""
import pygame.font

class Button():
    def __init__(self, game_settings, screen, message, width = 200, height = 50, button_position=None, button_rect=None, color = (0, 255, 0)):
        """initialize the button attributes"""

        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.msg = message

        # Set the dimensions and properties of the button.
        self.width, self.height = width, height
        self.button_color = color
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        # Build the button's rect object.
        self.rect = pygame.Rect(0, 0, self.width, self.height)

        if button_rect != None:
            self.rect = button_rect
        elif button_position != None:
            self.rect.x, self.rect.y = button_position
        else:
            #Position not provided? put button in center
            self.rect.center = self.screen_rect.center

        # The button needs to be prepped only once
        self.prep_msg(message)

    def prep_msg(self, msg):
        """Turn the msg into a rendered image and center text on the button."""

        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        #Draw blank button and then draw message.
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)