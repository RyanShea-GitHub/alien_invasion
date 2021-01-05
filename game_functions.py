#  This file will store a lot of the functionality of the game and keep the code base in the main file neat

import sys
from time import sleep
import pygame

from bullet import Bullet
from alien import Alien


def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets):
    '''this will check if there are any keypresses in the game'''
    # For each event(action) performed, check each of these statements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y)


def check_keydown_events(event, ai_settings, screen, ship, bullets):
    '''Check when the key is pushed down'''
    # Checks what kind of key is being pushed down and acts on it
    if event.key == pygame.K_d:
        ship.moving_right = True
    elif event.key == pygame.K_a:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_ESCAPE:
        sys.exit()


def check_keyup_events(event, ship):
    '''this will check for when a key is released'''
    # Check when the key is released to stop the movement of the ship
    if event.key == pygame.K_d:
        ship.moving_right = False
    elif event.key == pygame.K_a:
        ship.moving_left = False

def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    '''check to see if the play button was clicked'''
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # Reset the game settings
        ai_settings.intialize_dynamic_settings()
        # Hide the cursor once the game has started
        pygame.mouse.set_visible(False)
        # Reset the game statistics
        stats.reset_stats()
        stats.game_active = True
        # Reset the scoreboard images
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()
        # Reset the aliens and the bullets 
        aliens.empty()
        bullets.empty()
        # create a new fleet and center the ship
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()


def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets):
    '''respond to bullet and alien collision'''
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        # Check to see if the high-score has been beaten
        check_high_scores(stats, sb)
    if len(aliens) == 0:
        # Destroy the existing fleet,increase the level, speed up the game, and create a new fleet
        bullets.empty()
        ai_settings.increase_speed()

        # Increase the level
        stats.level += 1
        sb.prep_level()

        create_fleet(ai_settings, screen, ship, aliens)


def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets):
    '''check to see when an alien has hit the bottom of the screen'''
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
            break


def check_fleet_edges(ai_settings, aliens):
    '''respond if any of the aliens have touched the bounds'''
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

def check_high_scores(stats, sb):
    '''check to see if theres a new high score'''
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()

# -----------------------------------------------------------------------------------------------------------------------------------------------------------------#

def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button):
    '''update images on the screen and flip to a new screen'''
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)

    # Draw the scoreboard information
    sb.show_score()

    if not stats.game_active:
        play_button.draw_button()


def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    '''used to limit and remove bullets from the group'''
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom <=0:
            bullets.remove(bullet)
    
    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets)


def update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets):
    '''check if the aliens are at an edge, then update the positions of all aliens in the fleet'''
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # look for alien -> ship collisions
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)

    check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets)

# --------------------------------------------------------------------------------------------------------------------------------------------------------#

def get_number_aliens_x(ai_settings, alien_width):
    '''determine the number of aliens that fit in a row'''
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def get_number_rows(ai_settings, ship_height, alien_height):
    '''determine the number of rows of aliens that fit on the screen'''
    available_space_y = (ai_settings.screen_height - (6 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows

# ----------------------------------------------------------------------------------------------------------------------------------------------------#

def fire_bullet(ai_settings, screen, ship, bullets):
    '''fire a bullet if the fire-limit is not yet reached'''
    if len(bullets) < ai_settings.bullet_limit:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets):
    '''respond to the ship being hit by an alien'''
    if stats.ships_left > 1:
        stats.ships_left -= 1
        
        # Update scoreboard
        sb.prep_ships()

        #Get rid of the remaining bullets and aliens 
        aliens.empty()
        bullets.empty()

        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        # pause the game
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)
        

def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    '''create alien and place it in the row'''
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def create_fleet(ai_settings, screen, ship, aliens):
    '''create the full fleet of aliens'''
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)
    # Create the first row of aliens
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)
       

def change_fleet_direction(ai_settings, aliens):
    '''drop the fleet and change its direction'''
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1