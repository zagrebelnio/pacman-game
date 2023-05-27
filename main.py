from pygame.locals import *
from gameprocessing import *
from gamefield import *
from screen import *
from door import *

pygame.init()

game_field = GameField()
screen = Screen(game_field)
pygame.display.set_caption("Pacman")

application_is_on = True

while application_is_on:
    menu_decision = show_menu(screen)
    if menu_decision == "exit":
        application_is_on = False
    elif menu_decision == "start":
        game_result, score = game_loop(game_field, screen)
        if game_result is True:
            store_score(score)
            win_screen(screen, score)
        elif game_result is False:
            store_score(score)
            lose_screen(screen, score)
        elif game_result is None:
            application_is_on = False

pygame.quit()