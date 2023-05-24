import pygame

class Food:
    def __init__(self, game_field):
        self.__cords = []
        self.__size = game_field.getGridSize() // 5
        self.__radius = self.__size / 2
        self.__color = "white"

    def getCords(self):
        return self.__cords


    def reset(self, game_field):
        for y in range(game_field.getRows()):
            for x in range(game_field.getCols()):
                if game_field.getMatrix()[y][x] == 0:
                    self.__cords.append(((x * game_field.getGridSize()) + game_field.getGridSize() / 2, (y * game_field.getGridSize()) + game_field.getGridSize() / 2))

    def draw(self, screen):
        for cord in self.__cords:
            pygame.draw.circle(screen.getWindow(), self.__color, cord, self.__radius, self.__size)

    def eat(self, pacman):
        for i in range(len(self.__cords)):
            if self.__cords[i][0] - pacman.getRadius() + self.__radius <= pacman.getX() <= self.__cords[i][0] + pacman.getRadius() - self.__radius and self.__cords[i][1] - pacman.getRadius() + self.__radius <= pacman.getY() <= self.__cords[i][1] + pacman.getRadius() - self.__radius:
                self.__cords.pop(i)
                break