# Each time that we want to add new settings to the game, we should leave it in a separate file (module) 
# as to not clutter up the main code for the game
# This will store a class that will hold all of the settings in one place

class Settings():
    # a class to store all of the settings in alien invasion

    def __init__(self):
        '''initialize the games static settings'''
        # screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_colour = (230,230,230)
        # Ship settings
        self.ship_limit = 3
        # Bullet setup
        self.bullet_width = 5
        self.bullet_height = 13
        self.bullet_colour = 60, 60, 60
        self.bullet_limit = 5
        # Alien settings
        self.fleet_drop_speed = 11
        # Fleet direction: 1 = right || 0 = left 
        self.fleet_direction = 1
        # Game speed-up/alien point value on level-up
        self.speedup_scale = 1.1
        self.score_scale = 1.5

        self.intialize_dynamic_settings()

    def intialize_dynamic_settings(self):
        '''intialize settings that will change throughout the game'''
        self.ship_speed = 0.6
        self.bullet_speed_factor = 2
        self.alien_speed_factor = 0.5

        # Scoring 
        self.alien_points = 50

    def increase_speed(self):
        '''increase speed settings'''
        self.ship_speed *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
