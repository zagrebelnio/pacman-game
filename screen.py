import pygame

class Screen():
    def __init__(self, game_field):
        self.__width = game_field.getGridSize() * game_field.getCols()
        self.__height = game_field.getGridSize() * (game_field.getRows() + 3)
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

    def showText(self, text, text_rect):
        self.__window.blit(text, text_rect)

    def showImage(self, image, x, y):
        self.__window.blit(image, (x, y))
