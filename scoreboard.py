# The score is written to the screen so we gave to import the pygame fonts
import pygame.font
from pygame.sprite import Group

from ship import Ship

class Scoreboard():
    '''a class to keep track of the scoring in the game'''

    def __init__ (self, ai_settings, screen, stats):
        '''initialize the scorekeeping stats'''
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings
        self.stats = stats

        # Font settings for scoring
        self.text_colour = (30,30,30)
        self.font = pygame.font.SysFont(None, 38)

        # Prepare the intial score display 
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()


    def prep_score(self):
        '''turn the score in game into a rendered image on the screen'''
        # Rounds the score to the nearest 10
        rounded_score = int(round(self.stats.score, -1))
        # Format the score string so that there are decimal places when you build a large score
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True, self.text_colour, self.ai_settings.bg_colour)

        # Display the score at the top right of the screen
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        '''turn the high score into a rendered image.'''
        high_score = int(round(self.stats.high_score, -1))
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True, self.text_colour, self.ai_settings.bg_colour)

        # Center the high score at the top of the screen
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.screen_rect.top + 20

    def prep_level(self):
        '''turn the current level into a rendered image'''
        self.level_image = self.font.render(str(self.stats.level), True, self.text_colour, self.ai_settings.bg_colour)
        
        # Position the level below the score
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_ships(self):
        '''display the number of remaining ships'''
        # Creates empty grouop to hold the ship instances
        self.ships = Group()
        # For each ship left in teh settings, set each ship with 10p margin on either side 
        for ship_number in range (self.stats.ships_left):
            ship = Ship(self.ai_settings, self.screen)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)

    def show_score(self):
        '''show the score on the screen'''
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)

        # Draw remaining ships 
        self.ships.draw(self.screen)