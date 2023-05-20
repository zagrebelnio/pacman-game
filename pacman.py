import pygame

class Pacman:
    def __init__(self, game_field):
        self.x = 10 * game_field.grid_size + game_field.grid_size / 2
        self.y = 15 * game_field.grid_size + game_field.grid_size / 2
        self.radius = game_field.grid_size / 2
        self.size = game_field.grid_size
        self.direction = "right"
        self.cell = [int(self.y // game_field.grid_size), int(self.x // game_field.grid_size)]
        self.speed = 0.1
        self.color = "yellow"
    def move(self, dt, screen):
        if self.x < 0 - self.radius:
            self.x = screen.width + self.radius
        elif self.x > screen.width + self.radius:
            self.x = 0 - self.radius
        if self.direction == "right":
            self.x += self.speed * dt
        elif self.direction == "left":
            self.x -= self.speed * dt
        elif self.direction == "up":
            self.y -= self.speed * dt
        elif self.direction == "down":
            self.y += self.speed * dt

    def check_cell(self, game_field):
        self.cell = [int(self.y // game_field.grid_size), int(self.x // game_field.grid_size)]
    def can_turn(self, direction, game_field): #detects wether pacman can move in the specific direction
        if self.cell[1] <= 0 or self.cell[1] >= game_field.cols - 1:
            if self.direction == "left" and direction == "right":
                return True
            elif self.direction == "right" and direction == "left":
                return True
        else:
            if direction == "left" and self.direction != "left" and game_field.matrix[self.cell[0]][self.cell[1] - 1] == 0 and self.cell[0] * game_field.grid_size + self.radius - 2 <= self.y <= (self.cell[0] + 1) * game_field.grid_size - self.radius + 2:
                return True
            elif direction == "right" and self.direction != "right" and game_field.matrix[self.cell[0]][self.cell[1] + 1] == 0 and self.cell[0] * game_field.grid_size + self.radius - 2 <= self.y <= (self.cell[0] + 1) * game_field.grid_size - self.radius + 2:
                return True
            elif direction == "up" and self.direction != "up" and game_field.matrix[self.cell[0] - 1][self.cell[1]] == 0 and self.cell[1] * game_field.grid_size + self.radius - 2 <= self.x <= (self.cell[1] + 1) * game_field.grid_size - self.radius + 2:
                return True
            elif direction == "down" and self.direction != "down" and game_field.matrix[self.cell[0] + 1][self.cell[1]] == 0 and self.cell[1] * game_field.grid_size + self.radius - 2 <= self.x <= (self.cell[1] + 1) * game_field.grid_size - self.radius + 2:
                return True
        return False
    def draw(self, screen):
        pygame.draw.circle(screen.window, self.color, (self.x, self.y), self.radius, self.size)