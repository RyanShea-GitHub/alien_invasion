# This will be used to create the ship on screen and give most of its functionality

import pygame
from pygame.sprite import Sprite

# This is the class for this ship
# All the information about the ship and how it will be rendered is contained here
class Ship(Sprite):
    '''initialize the ship and get its starting position'''
    def __init__(self, ai_settings, screen):
        super(Ship, self).__init__()
        
        self.screen = screen
        self.image = pygame.image.load('images/spaceship.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings

        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        self.center = float(self.rect.centerx)

        self.moving_right = False
        self.moving_left = False

    def update(self):
        # Creates collision with the left and right borders of the window
        # If you are moving right AND the most right pixel is less than the right most pixel of the screen, do this
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed
        # If you are moving left and your left most pixel is higher than zero, do this
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed
        # This sets your center from an int to a float so that we can manipulate the speed of the ship more effectively
        self.rect.centerx = self.center
        

    '''draw the ship at its current location'''
    def blitme(self):
        # This creates a surface on the screen
        self.screen.blit(self.image, self.rect)


    def center_ship(self):
        '''center the ship after it has been hit'''
        self.center = self.screen_rect.centerx