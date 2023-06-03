import pygame

class Door:
    def __init__(self, game_field):
        self.__cell = [8, 10]
        self.__width = game_field.getGridSize()
        self.__height = game_field.getGridSize() / 5
        self.__status = "closed"
        self.__x = self.__cell[1] * game_field.getGridSize() + game_field.getGridSize() / 2
        self.__y = self.__cell[0] * game_field.getGridSize() + game_field.getGridSize() / 2
        self.__image = pygame.image.load("images/2_door.png")

    def getStatus(self):
        return self.__status

    def draw(self, screen):
        screen.showImage(self.__image, self.__x - self.__width / 2, self.__y - self.__width / 2)

    def open(self):
        self.__status = "opened"

    def close(self):
        self.__status = "closed"