import pygame

class GameField:
    def __init__(self):
        self.__matrix = [[-1, 6, 4, 4, 4, 4, 4, 4, 4, 4, 5, 4, 4, 4, 4, 4, 4, 4, 4, 7, -1],
                         [-1, 3, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 3, -1],
                         [-1, 3, 1, 8, 9, 0, 8, 4, 9, 0, 10, 0, 8, 4, 9, 0, 8, 9, 1, 3, -1],
                         [-1, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, -1],
                         [-1, 3, 0, 8, 9, 0, 13, 0, 8, 4, 5, 4, 9, 0, 13, 0, 8, 9, 0, 3, -1],
                         [-1, 3, 0, 0, 0, 0, 3, 0, 0, 0, 3, 0, 0, 0, 3, 0, 0, 0, 0, 3, -1],
                         [-1, 11, 4, 4, 7, 0, 14, 4, 9, 0, 10, 0, 8, 4, 15, 0, 6, 4, 4, 12, -1],
                         [-1, -1, -1, -1, 3, 0, 3, 0, 0, 0, 0, 0, 0, 0, 3, 0, 3, -1, -1, -1, -1],
                         [4, 4, 4, 4, 12, 0, 10, 0, 6, 4, 2, 4, 7, 0, 10, 0, 11, 4, 4, 4, 4],
                         [0, 0, 0, 0, 0, 0, 0, 0, 3, -1, -1, -1, 3, 0, 0, 0, 0, 0, 0, 0, 0],
                         [4, 4, 4, 4, 7, 0, 13, 0, 11, 4, 4, 4, 12, 0, 13, 0, 6, 4, 4, 4, 4],
                         [-1, -1, -1, -1, 3, 0, 3, 0, 0, 0, 0, 0, 0, 0, 3, 0, 3, -1, -1, -1, -1],
                         [-1, 6, 4, 4, 12, 0, 10, 0, 8, 4, 5, 4, 9, 0, 10, 0, 11, 4, 4, 7, -1],
                         [-1, 3, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 3, -1],
                         [-1, 3, 0, 8, 7, 0, 8, 4, 9, 0, 10, 0, 8, 4, 9, 0, 6, 9, 0, 3, -1],
                         [-1, 3, 1, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 1, 3, -1],
                         [-1, 14, 9, 0, 10, 0, 13, 0, 8, 4, 5, 4, 9, 0, 13, 0, 10, 0, 8, 15, -1],
                         [-1, 3, 0, 0, 0, 0, 3, 0, 0, 0, 3, 0, 0, 0, 3, 0, 0, 0, 0, 3, -1],
                         [-1, 3, 0, 8, 4, 4, 16, 4, 9, 0, 10, 0, 8, 4, 16, 4, 4, 9, 0, 3, -1],
                         [-1, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, -1],
                         [-1, 11, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 12, -1]]
        self.__rows = 21
        self.__cols = 21
        self.__grid_size = 30
        self.__background_color = (0, 0, 0)
        self.__grid_color = (100, 100, 100)
        self.__wall_color = (0, 0, 204)
        self.__status = "normal"
        self.__vertical_wall = pygame.image.load("images/3_vertical_wall.png")
        self.__horizontal_wall = pygame.image.load("images/4_horizontal_wall.png")
        self.__crossing_left_bottom_right = pygame.image.load("images/5_crossing_left-bottom-right.png")
        self.__turn_bottom_right = pygame.image.load("images/6_turn_bottom-right.png")
        self.__turn_bottom_left = pygame.image.load("images/7_turn_bottom-left.png")
        self.__convexity_right = pygame.image.load("images/8_convexity_right.png")
        self.__convexity_left = pygame.image.load("images/9_convexity_left.png")
        self.__convexity_top = pygame.image.load("images/10_convexity_top.png")
        self.__turn_top_right = pygame.image.load("images/11_turn_top-right.png")
        self.__turn_top_left = pygame.image.load("images/12_turn_top-left.png")
        self.__convexity_bottom = pygame.image.load("images/13_convexity_bottom.png")
        self.__crossing_bottom_right_top = pygame.image.load("images/14_crossing_bottom-right-top.png")
        self.__crossing_top_left_bottom = pygame.image.load("images/15_crossing_top-left-bottom.png")
        self.__crossing_left_top_right = pygame.image.load("images/16_crossing_left-top-right.png")

    def setStatus(self, status):
        self.__status = status

    def getStatus(self):
        return self.__status

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
                if self.__matrix[y][x] == 3:
                    screen.showImage(self.__vertical_wall, x * self.__grid_size, y * self.__grid_size)
                elif self.__matrix[y][x] == 4:
                    screen.showImage(self.__horizontal_wall, x * self.__grid_size, y * self.__grid_size)
                elif self.__matrix[y][x] == 5:
                    screen.showImage(self.__crossing_left_bottom_right, x * self.__grid_size, y * self.__grid_size)
                elif self.__matrix[y][x] == 6:
                    screen.showImage(self.__turn_bottom_right, x * self.__grid_size, y * self.__grid_size)
                elif self.__matrix[y][x] == 7:
                    screen.showImage(self.__turn_bottom_left, x * self.__grid_size, y * self.__grid_size)
                elif self.__matrix[y][x] == 8:
                    screen.showImage(self.__convexity_right, x * self.__grid_size, y * self.__grid_size)
                elif self.__matrix[y][x] == 9:
                    screen.showImage(self.__convexity_left, x * self.__grid_size, y * self.__grid_size)
                elif self.__matrix[y][x] == 10:
                    screen.showImage(self.__convexity_top, x * self.__grid_size, y * self.__grid_size)
                elif self.__matrix[y][x] == 11:
                    screen.showImage(self.__turn_top_right, x * self.__grid_size, y * self.__grid_size)
                elif self.__matrix[y][x] == 12:
                    screen.showImage(self.__turn_top_left, x * self.__grid_size, y * self.__grid_size)
                elif self.__matrix[y][x] == 13:
                    screen.showImage(self.__convexity_bottom, x * self.__grid_size, y * self.__grid_size)
                elif self.__matrix[y][x] == 14:
                    screen.showImage(self.__crossing_bottom_right_top, x * self.__grid_size, y * self.__grid_size)
                elif self.__matrix[y][x] == 15:
                    screen.showImage(self.__crossing_top_left_bottom, x * self.__grid_size, y * self.__grid_size)
                elif self.__matrix[y][x] == 16:
                    screen.showImage(self.__crossing_left_top_right, x * self.__grid_size, y * self.__grid_size)
