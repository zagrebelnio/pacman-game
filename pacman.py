import pygame
import os

class Pacman:
    def __init__(self, game_field):
        self.__x = 10 * game_field.getGridSize() + game_field.getGridSize() / 2
        self.__y = 15 * game_field.getGridSize() + game_field.getGridSize() / 2
        self.__radius = game_field.getGridSize() / 2
        self.__size = game_field.getGridSize()
        self.__direction = "right"
        self.__cell = [int(self.__y // game_field.getGridSize()), int(self.__x // game_field.getGridSize())]
        self.__speed = 0.1
        self.__color = "yellow"
        self.__lifes = 3
        self.__frames = []
        for file_name in os.listdir("images/pacman_frames"):
            frame = pygame.transform.scale(pygame.image.load("images/pacman_frames" + os.sep + file_name), (self.__size + 5, self.__size + 5))
            self.__frames.append(frame)
        self.__counter = 0
        self.__animating_forward = True

    def setX(self, x):
        self.__x = x

    def setY(self, y):
        self.__y = y

    def setDirection(self, direction):
        self.__direction = direction

    def setCell(self, game_field):
        self.__cell = [int(self.__y // game_field.getGridSize()), int(self.__x // game_field.getGridSize())]

    def getX(self):
        return self.__x

    def getY(self):
        return self.__y

    def getRadius(self):
        return self.__radius

    def getSize(self):
        return self.__size

    def getDirection(self):
        return self.__direction

    def getCell(self):
        return self.__cell

    def getLifes(self):
        return self.__lifes

    def decrementLifes(self):
        self.__lifes -= 1

    def reset(self, game_field):
        self.__x = 10 * game_field.getGridSize() + game_field.getGridSize() / 2
        self.__y = 15 * game_field.getGridSize() + game_field.getGridSize() / 2
        self.__direction = "right"

    def move(self, dt, screen):
        if self.__x < 0 - self.__radius:
            self.__x = screen.getWidth() + self.__radius
        elif self.__x > screen.getWidth() + self.__radius:
            self.__x = 0 - self.__radius
        if self.__direction == "right":
            self.__x += self.__speed * dt
        elif self.__direction == "left":
            self.__x -= self.__speed * dt
        elif self.__direction == "up":
            self.__y -= self.__speed * dt
        elif self.__direction == "down":
            self.__y += self.__speed * dt

    def can_turn(self, direction, game_field): #detects wether pacman can move in the specific direction
        if self.__cell[1] <= 0 or self.__cell[1] >= game_field.getCols() - 1:
            if self.__direction == "left" and direction == "right":
                return True
            elif self.__direction == "right" and direction == "left":
                return True
        else:
            if direction == "left" and self.__direction != "left" and self.__getNeighhbourCell(direction, game_field) <= 1 and self.__cell[0] * game_field.getGridSize() + self.__radius - 2 <= self.__y <= (self.__cell[0] + 1) * game_field.getGridSize() - self.__radius + 2:
                return True
            elif direction == "right" and self.__direction != "right" and self.__getNeighhbourCell(direction, game_field) <= 1 and self.__cell[0] * game_field.getGridSize() + self.__radius - 2 <= self.__y <= (self.__cell[0] + 1) * game_field.getGridSize() - self.__radius + 2:
                return True
            elif direction == "up" and self.__direction != "up" and self.__getNeighhbourCell(direction, game_field) <= 1 and self.__cell[1] * game_field.getGridSize() + self.__radius - 2 <= self.__x <= (self.__cell[1] + 1) * game_field.getGridSize() - self.__radius + 2:
                return True
            elif direction == "down" and self.__direction != "down" and self.__getNeighhbourCell(direction, game_field) <= 1 and self.__cell[1] * game_field.getGridSize() + self.__radius - 2 <= self.__x <= (self.__cell[1] + 1) * game_field.getGridSize() - self.__radius + 2:
                return True
        return False
    def draw(self, screen):
        divider = 5
        if self.__animating_forward:
            if self.__counter < len(self.__frames) * divider - 1:
                self.__counter += 1
            else:
                self.__animating_forward = False
        else:
            if self.__counter > 1:
                self.__counter -= 1
            else:
                self.__animating_forward = True
        if self.__direction == "left":
            screen.showImage(pygame.transform.flip(self.__frames[self.__counter // divider], True, False), self.__x - self.__radius, self.__y - self.__radius)
        elif self.__direction == "right":
            screen.showImage(self.__frames[self.__counter // divider], self.__x - self.__radius, self.__y - self.__radius)
        elif self.__direction == "up":
            screen.showImage(pygame.transform.rotate(self.__frames[self.__counter // divider], 90), self.__x - self.__radius, self.__y - self.__radius)
        elif self.__direction == "down":
            screen.showImage(pygame.transform.rotate(self.__frames[self.__counter // divider], 270), self.__x - self.__radius, self.__y - self.__radius)

    def __getNeighhbourCell(self, direction, game_field):
        if direction == "left":
            return game_field.getMatrix()[self.__cell[0]][self.__cell[1] - 1]
        elif direction == "right":
            return game_field.getMatrix()[self.__cell[0]][self.__cell[1] + 1]
        elif direction == "up":
            return game_field.getMatrix()[self.__cell[0] - 1][self.__cell[1]]
        elif direction == "down":
            return game_field.getMatrix()[self.__cell[0] + 1][self.__cell[1]]