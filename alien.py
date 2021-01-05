import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    '''class for the alien enemy in the game'''
    def __init__(self, ai_settings, screen):
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # Load the image of the ship onto the screen
        self.image = pygame.image.load("images/alien_ship.bmp")
        self.rect = self.image.get_rect()

        # start each alien at the top left of the screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # store the current position of the alien
        self.x = float(self.rect.x)

    def blitme(self):
        '''draw the alien and its current position'''
        self.screen.blit(self.image, self.rect)

    def update(self):
        '''move the alien to the right or left'''
        self.x += (self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction)
        self.rect.x = self.x

    def check_edges(self):
        '''check to see when the fleet has touched either of the borders'''
        screen_rect = self.screen.get_rect()

        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

