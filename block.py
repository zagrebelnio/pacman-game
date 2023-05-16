from constants import *

class Block:
    def __init__(self):
        self.rect = []
    def reset(self):
        for y in range(ROWS):
            for x in range(COLS):
                if GAME_FIELD[y][x] == 1:
                    self.rect.append([x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE])
    def check_wall_collisions(self, pacman):
        # pacman-block collisions
        for block in self.rect:
            # right collision
            if pacman.direction == "right" and block[0] - pacman.radius <= pacman.x <= block[0] + block[
                2] - pacman.radius and block[1] <= pacman.y <= block[1] + block[3]:
                pacman.x = block[0] - pacman.radius
            # left collision
            if pacman.direction == "left" and block[0] + pacman.radius <= pacman.x <= block[0] + block[
                2] + pacman.radius and block[1] <= pacman.y <= block[1] + block[3]:
                pacman.x = block[0] + block[2] + pacman.radius
            # top collision
            if pacman.direction == "up" and block[0] <= pacman.x <= block[0] + block[2] and block[
                1] + pacman.radius <= pacman.y <= block[1] + block[3] + pacman.radius:
                pacman.y = block[1] + block[2] + pacman.radius
            # bottom collision
            if pacman.direction == "down" and block[0] <= pacman.x <= block[0] + block[2] and block[
                1] - pacman.radius <= pacman.y <= block[1] + block[3] - pacman.radius:
                pacman.y = block[1] - pacman.radius