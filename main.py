from gameprocessing import *
import pygame

pygame.init()

game = Game()
pygame.display.set_caption("Pacman")
pygame.display.set_icon(pygame.image.load("images/pac-man-icon-8.jpg"))

application_is_on = True

menu = Menu(game.getScreen())

while application_is_on:
    menu.show_menu(game.getScreen())
    if menu.getStatus() == "exit":
        application_is_on = False
    elif menu.getStatus() == "statistics":
        menu.showStatistics(game.getScreen())
        if menu.getStatus() == "exit":
            application_is_on = False
    elif menu.getStatus() == "start":
        game_result, score, game_time, player_lifes, exit_to_menu = game.game_loop()
        if game_result is True:
            menu_decision = menu.show_score(game.getScreen(), score, game_time, player_lifes)
            if menu_decision == True:
                menu.win_screen(game.getScreen(), menu.getScore())
        elif game_result is False:
            menu_decision = menu.show_score(game.getScreen(), score, game_time, player_lifes)
            if menu_decision == True:
                menu.lose_screen(game.getScreen(), menu.getScore())
        elif game_result is None and exit_to_menu is False:
            application_is_on = False
        if menu.getStatus() == "exit":
            application_is_on = False
        menu.playMusic()

pygame.quit()