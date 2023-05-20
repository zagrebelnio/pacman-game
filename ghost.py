import pygame

class Ghost:
    def __init__(self, game_field):
        self.x = 10 * game_field.grid_size + game_field.grid_size / 2
        self.y = 9 * game_field.grid_size + game_field.grid_size / 2
        self.radius = game_field.grid_size / 2
        self.direction = "right"
        self.size = game_field.grid_size
        self.color = "red"
        self.cell = [int(self.y // game_field.grid_size), int(self.x // game_field.grid_size)]
        self.speed = 0.1
        self.target_cell = []
    def draw(self, screen):
        pygame.draw.circle(screen.window, self.color, (self.x, self.y), self.radius, self.size)
        pygame.draw.rect(screen.window, self.color, (self.x - self.radius, self.y, 2*self.radius, self.radius))
    def choose_target(self, pacman):
        self.target_cell = pacman.cell
    def move(self, dt):
        if self.direction == "right":
            self.x += self.speed * dt
        elif self.direction == "left":
            self.x -= self.speed * dt
        elif self.direction == "up":
            self.y += self.speed * dt
        elif self.direction == "down":
            self.y -= self.speed * dt
    def changeDirection(self):
        pass