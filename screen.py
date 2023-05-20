import pygame

class Screen():
    def __init__(self, game_field):
        self.width = game_field.grid_size * game_field.cols
        self.height = game_field.grid_size * game_field.rows
        self.background_color = (0, 0, 0)
        self.window = pygame.display.set_mode((self.width, self.height))
    def fill(self):
        self.window.fill(self.background_color)