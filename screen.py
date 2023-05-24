import pygame

class Screen():
    def __init__(self, game_field):
        self.__width = game_field.getGridSize() * game_field.getCols()
        self.__height = game_field.getGridSize() * game_field.getRows()
        self.__background_color = (0, 0, 0)
        self.__window = pygame.display.set_mode((self.__width, self.__height))

    def getWidth(self):
        return self.__width

    def getHeight(self):
        return self.__height

    def getBackgroundColor(self):
        return self.__background_color

    def getWindow(self):
        return self.__window

    def fill(self):
        self.__window.fill(self.__background_color)