import pygame

class GameField:
    def __init__(self):
        self.__matrix = [[-1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, -1],
              [-1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, -1],
              [-1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, -1],
              [-1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, -1],
              [-1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, -1],
              [-1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, -1],
              [-1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, -1],
              [-1, -1, -1, -1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, -1, -1, -1, -1],
              [1, 1, 1, 1, 1, 0, 1, 0, 1, 1, -1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1],
              [0, 0, 0, 0, 0, 0, 0, 0, 1, -1, -1, -1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
              [1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1],
              [-1, -1, -1, -1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, -1, -1, -1, -1],
              [-1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, -1],
              [-1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, -1],
              [-1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, -1],
              [-1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, -1],
              [-1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, -1],
              [-1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, -1],
              [-1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, -1],
              [-1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, -1],
              [-1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, -1]]
        self.__rows = 21
        self.__cols = 21
        self.__grid_size = 30
        self.__background_color = (0, 0, 0)
        self.__grid_color = (100, 100, 100)
        self.__wall_color = (0, 0, 204)

    def getMatrix(self):
        return self.__matrix

    def getRows(self):
        return self.__rows

    def getCols(self):
        return self.__cols

    def getGridSize(self):
        return self.__grid_size

    def draw(self, screen):
        for y in range(self.__rows):
            for x in range(self.__cols):
                if self.__matrix[y][x] == 1:
                    pygame.draw.rect(screen.getWindow(), self.__wall_color,
                                     [x * self.__grid_size + 1, y * self.__grid_size + 1, self.__grid_size - 2, self.__grid_size - 2])

    def drawGrid(self, screen):
        for y in range(self.__rows):
            for x in range(self.__cols):
                pygame.draw.rect(screen.getWindow(), self.__grid_color,
                         [x * self.__grid_size, y * self.__grid_size, self.__grid_size, self.__grid_size], 1)
