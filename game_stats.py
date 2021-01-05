import pygame

class GameStats():
    '''track the statistics for alien invasion'''
    def __init__(self, ai_settings):
        '''initialize statistics'''
        self.ai_settings = ai_settings
        self.reset_stats()
        # Current game state
        self.game_active = False
        # Game score
        self.score = 0
        self.high_score = 0
        # Display the current level of the game
        self.level = 1 

    def reset_stats(self):
        '''initialize statistics that can change during the game'''
        self.ships_left = self.ai_settings.ship_limit