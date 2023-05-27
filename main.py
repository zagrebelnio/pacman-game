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
    menu_desicion = show_menu(screen)
    if menu_desicion == "exit":
        application_is_on = False
    elif menu_desicion == "start":
        game_result = game_loop(game_field, screen)
        if game_result is True:
            win_screen(screen)
        elif game_result is False:
            lose_screen(screen)
        elif game_result is None:
            application_is_on = False

pygame.quit()