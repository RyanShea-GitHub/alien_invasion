
import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    '''class to manage bullets fired from the ship'''

    def __init__(self, ai_settings, screen, ship):
        super().__init__()
        self.screen = screen
        self.rect = pygame.Rect(0, 0, ai_settings.bullet_width, ai_settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        self.y = float(self.rect.y)

        self.colour = ai_settings.bullet_colour
        self.speed_factor = ai_settings.bullet_speed_factor

    
    def update(self):
        '''make the bullet move up the screen'''
        self.y -= self.speed_factor
        self.rect.y = self.y

    def draw_bullet(self):
        '''drawing the bullet on the screen'''
        pygame.draw.rect(self.screen, self.colour, self.rect)
