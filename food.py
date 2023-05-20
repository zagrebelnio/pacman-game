import pygame

class Food:
    def __init__(self, game_field):
        self.cords = []
        self.size = game_field.grid_size // 5
        self.radius = self.size / 2
        self.color = "white"

    def reset(self, game_field):
        for y in range(game_field.rows):
            for x in range(game_field.cols):
                if game_field.matrix[y][x] == 0:
                    self.cords.append(((x * game_field.grid_size) + game_field.grid_size / 2, (y * game_field.grid_size) + game_field.grid_size / 2))

    def draw(self, screen):
        for cord in self.cords:
            pygame.draw.circle(screen.window, self.color, cord, self.radius, self.size)

    def eat(self, pacman):
        for i in range(len(self.cords)):
            if self.cords[i][0] - pacman.radius + self.radius <= pacman.x <= self.cords[i][0] + pacman.radius - self.radius and self.cords[i][1] - pacman.radius + self.radius <= pacman.y <= self.cords[i][1] + pacman.radius - self.radius:
                self.cords.pop(i)
                break