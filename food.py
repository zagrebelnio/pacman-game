import pygame
from constants import *

class Food:
    def __init__(self):
        self.cords = []
        self.radius = FOOD_SIZE / 2

    def reset(self):
        for y in range(ROWS):
            for x in range(COLS):
                if GAME_FIELD[y][x] == 0:
                    self.cords.append(((x * GRID_SIZE) + GRID_SIZE / 2, (y * GRID_SIZE) + GRID_SIZE / 2))

    def draw(self, screen):
        for cord in self.cords:
            pygame.draw.circle(screen, "white", cord, self.radius, FOOD_SIZE)

    def eat(self, pacman):
        for i in range(len(self.cords)):
            if self.cords[i][0] - pacman.radius + self.radius <= pacman.x <= self.cords[i][0] + pacman.radius - self.radius and self.cords[i][1] - pacman.radius + self.radius <= pacman.y <= self.cords[i][1] + pacman.radius - self.radius:
                self.cords.pop(i)
                break