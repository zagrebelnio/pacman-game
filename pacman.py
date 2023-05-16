import pygame
from constants import *

class Pacman:
    def __init__(self):
        self.x = PACMAN_START_X
        self.y = PACMAN_START_Y
        self.radius = GRID_SIZE / 2
        self.direction = "right"
    def move(self, dt):
        if self.x < 0 - self.radius:
            self.x = SCREEN_WIDTH + self.radius
        elif self.x > SCREEN_WIDTH + self.radius:
            self.x = 0 - self.radius
        if self.direction == "right":
            self.x += PACMAN_SPEED * dt
        elif self.direction == "left":
            self.x -= PACMAN_SPEED * dt
        elif self.direction == "up":
            self.y -= PACMAN_SPEED * dt
        elif self.direction == "down":
            self.y += PACMAN_SPEED * dt
    def can_turn(self, direction): #detects wether pacman can move in the specific direction
        current_pos = [int(self.y // GRID_SIZE), int(self.x // GRID_SIZE)]
        if current_pos[1] <= 0 or current_pos[1] >= COLS - 1:
            if self.direction == "left" and direction == "right":
                return True
            elif self.direction == "right" and direction == "left":
                return True
        else:
            if direction == "left" and self.direction != "left" and GAME_FIELD[current_pos[0]][current_pos[1] - 1] == 0 and current_pos[0] * GRID_SIZE + self.radius - 2 <= self.y <= (current_pos[0] + 1) * GRID_SIZE - self.radius + 2:
                return True
            elif direction == "right" and self.direction != "right" and GAME_FIELD[current_pos[0]][current_pos[1] + 1] == 0 and current_pos[0] * GRID_SIZE + self.radius - 2 <= self.y <= (current_pos[0] + 1) * GRID_SIZE - self.radius + 2:
                return True
            elif direction == "up" and self.direction != "up" and GAME_FIELD[current_pos[0] - 1][current_pos[1]] == 0 and current_pos[1] * GRID_SIZE + self.radius - 2 <= self.x <= (current_pos[1] + 1) * GRID_SIZE - self.radius + 2:
                return True
            elif direction == "down" and self.direction != "down" and GAME_FIELD[current_pos[0] + 1][current_pos[1]] == 0 and current_pos[1] * GRID_SIZE + self.radius - 2 <= self.x <= (current_pos[1] + 1) * GRID_SIZE - self.radius + 2:
                return True
        return False
    def draw(self, screen):
        pygame.draw.circle(screen, "yellow", (self.x, self.y), self.radius, PACMAN_SIZE)