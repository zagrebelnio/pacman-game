from gameprocessing import *
from gamefield import *
from screen import *
import pygame

pygame.init()

game_field = GameField()
screen = Screen(game_field)
pygame.display.set_caption("Pacman")
pygame.display.set_icon(pygame.image.load("images/pac-man-icon-8.jpg"))

application_is_on = True

music = Music()
music.playMenu()
volume_index = 0

while application_is_on:
    menu_decision, volume_index = show_menu(screen, music, volume_index)
    if menu_decision == "exit":
        application_is_on = False
    elif menu_decision == "statistics":
        menu_decision,  volume_index = show_statistics(screen, music, volume_index)
        if menu_decision == "exit":
            application_is_on = False
    elif menu_decision == "start":
        music.menuStop()
        game_result, score, game_time, player_lifes, exit_to_menu = game_loop(game_field, screen)
        if game_result is True:
            score = calculate_total_score(score, game_time, player_lifes)
            menu_decision = store_score(screen, score)
            if menu_decision == True:
                win_screen(screen, score)
        elif game_result is False:
            score = calculate_total_score(score, game_time, player_lifes)
            menu_decision = store_score(screen, score)
            if menu_decision == True:
                lose_screen(screen, score)
        elif game_result is None and exit_to_menu is False:
            application_is_on = False
        if menu_decision == "exit":
            application_is_on = False
        music.playMenu()

pygame.quit()