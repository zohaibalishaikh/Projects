"""Settings module keeps all the game settings in one place."""

class Settings ():
    """A class to store all the settings of the alien invasion"""

    def __init__(self):
        """initialize the game settings with defaults."""

        self.screen_width = 1500
        self.screen_height = 800
        self.bg_color = (100, 100, 100)
        self.speedup_scale = 1.1
        #Ship settings
        self.ship_speed = 2
        self.ship_limit = 3
        #Bullet settings
        self.bullet_speed = 2
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3
        #Alien settings
        self.alien_gap_x = 1 # Gap between two aliens on horizontal axis is 1 x alien width
        self.alien_gap_y = 1 # Gap between two aliens on vertical axis is 1 x alien height
        self.alien_ship_gap = 2
        self.alien_offsets_x = 2
        self.alien_offsets_y = 1
        self.alien_speed = 1
        self.alien_drop_speed = 50
        #Right direction is denoted by 1 and left by -1
        self.alien_direction = 1
        # Score settings
        self.alien_points = 50
        self.score_scale = 10 # 10 points increase in every level for hitting an alien
        # High score window settings
        self.hs_bg_color = (255 ,255, 255) # Background white
        self.hs_text_color = (0, 0, 0) # Text color black
        self.hs_window_width = 400
        self.hs_window_height = 300
        

    def level_up(self):
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_drop_speed *= self.speedup_scale

        self.alien_points += self.score_scale
