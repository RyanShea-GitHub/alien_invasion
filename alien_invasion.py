# This is the game alien invasion
# What will we need to code? :
# A ship at the bottom of the screen that can move left and right
# This ship can also fire missiles using spacebar
# Enemies that come down from the top of the screen
# When the player shoots all of the aliens, a new fleet appears
# This new fleet will move faster and be more dangerous than prev
# When the player gets hit he will lose a life (3 lives total)


import pygame
import game_functions as gf

from settings import Settings
from game_stats import GameStats
from ship import Ship
from alien import Alien
from pygame.sprite import Group
from button import Button
from scoreboard import Scoreboard

def run_game():
    # This initializes the pygame screen
    pygame.init()

    # Creates Icon as surface, point to image in folder
    icon = pygame.image.load("images/spaceinvader.bmp")
    pygame.display.set_icon(icon)
    pygame.display.set_caption("Alien Invasion")

   # This variable is used to store the data from the file settings and make them usable in our main game file
    ai_settings = Settings()

    # Create a var to set the game stats
    stats = GameStats(ai_settings)

    # sets display mode and then pulls the settings from the other file to set the screen res
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    
    # Show the scoreboard on the screen
    sb = Scoreboard(ai_settings, screen, stats)

    # Draw play button
    play_button = Button(ai_settings, screen, "Play")

    # ship/alien variable = Ship/Alien class
    ship = Ship(ai_settings, screen)
    alien = Alien(ai_settings, screen)

    # Create a group for the live bullets/enemy aliens that are on the screen
    # The group class will hold multiple sprites
    bullets = Group()
    aliens = Group()

    #Create a fleet of enemy aliens
    gf.create_fleet(ai_settings, screen, ship, aliens)

    # While the game is running, do this:
    while True:
        screen.fill(ai_settings.bg_colour)

        gf.check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets)
        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button) 

        if stats.game_active:
            ship.update()

            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets)
            gf.update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets)

            ship.blitme()

            
        pygame.display.flip()

run_game()
