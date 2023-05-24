import pygame
import math

class Ghost:
    def __init__(self, game_field):
        self.x = 10 * game_field.grid_size + game_field.grid_size / 2
        self.y = 9 * game_field.grid_size + game_field.grid_size / 2
        self.radius = game_field.grid_size / 2
        self.direction = "up"
        self.size = game_field.grid_size
        self.color = "red"
        self.cell = [int(self.y // game_field.grid_size), int(self.x // game_field.grid_size)]
        self.speed = 0.1
        self.target_cell = []
        self.turn_directions = {"left": False, "right": False, "up": False, "down": False }
    def draw(self, screen):
        pygame.draw.circle(screen.window, self.color, (self.x, self.y), self.radius, self.size)
        pygame.draw.rect(screen.window, self.color, (self.x - self.radius, self.y, 2*self.radius, self.radius))
    def setTarget(self, pacman):
        if self.cell != [9, 9] and self.cell != [9, 10] and self.cell != [9, 11]:
            self.target_cell = pacman.cell
        else:
            self.target_cell = [10, 7]
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

    def checkNeighbourCells(self, game_field):
        if self.cell[1] <= 0 or self.cell[1] >= game_field.cols - 1:
            self.turn_directions["left"] = True
            self.turn_directions["right"] = True
        else:
            # left cell
            if game_field.matrix[self.cell[0]][self.cell[1] - 1] != 1:
                self.turn_directions["left"] = True
            else:
                self.turn_directions["left"] = False
            # right cell
            if game_field.matrix[self.cell[0]][self.cell[1] + 1] != 1:
                self.turn_directions["right"] = True
            else:
                self.turn_directions["right"] = False
            # top cell
            if game_field.matrix[self.cell[0] - 1][self.cell[1]] != 1:
                self.turn_directions["up"] = True
            else:
                self.turn_directions["up"] = False
            # bottom cell
            if game_field.matrix[self.cell[0] + 1][self.cell[1]] != 1:
                self.turn_directions["down"] = True
            else:
                self.turn_directions["down"] = False

    def getNeighbourCell(self, direction):
        if direction == "left":
            return [self.cell[0], self.cell[1] - 1]
        elif direction == "right":
            return [self.cell[0], self.cell[1] + 1]
        elif direction == "up":
            return [self.cell[0] - 1, self.cell[1]]
        elif direction == "down":
            return [self.cell[0] + 1, self.cell[1]]

    def makeChoice(self, directions):
        cells = []
        for direction in directions:
            cells.append(self.getNeighbourCell(direction))
        distances = []
        for cell in cells:
            distances.append(math.sqrt(math.pow((self.target_cell[0] - cell[0]), 2) + math.pow((self.target_cell[1] - cell[1]), 2)))
        for i in range(len(distances)):
            if distances[i] == min(distances):
                return directions[i]

    def turn(self, next_direction, game_field):
        if self.cell[1] * game_field.grid_size + self.radius - 1 <= self.x <= self.cell[1] * game_field.grid_size + self.radius + 1 and self.cell[0] * game_field.grid_size + self.radius - 1 <= self.y <= self.cell[0] * game_field.grid_size + self.radius + 1:
            self.direction = next_direction
    def changeDirection(self, game_field):
        self.checkNeighbourCells(game_field)
        is_in_impasse = True
        if self.direction == "left":
            self.turn_directions["right"] = False
        elif self.direction == "right":
            self.turn_directions["left"] = False
        elif self.direction == "up":
            self.turn_directions["down"] = False
        elif self.direction == "down":
            self.turn_directions["up"] = False
        for direction in self.turn_directions.values():
            if direction:
                is_in_impasse = False
        if is_in_impasse:
            if self.direction == "left":
                self.turn_directions["right"] = True
            elif self.direction == "right":
                self.turn_directions["left"] = True
            elif self.direction == "up":
                self.turn_directions["down"] = True
            elif self.direction == "down":
                self.turn_directions["up"] = True
        choices = 0
        for turn_direction in self.turn_directions.values():
            if turn_direction == True:
                choices += 1
        if choices > 1:
            keys = list(self.turn_directions.keys())
            i = 0
            directions = []
            for turn_direction in self.turn_directions.values():
                if turn_direction == True:
                    directions.append(keys[i])
                i += 1
            next_direction = self.makeChoice(directions)
            self.turn(next_direction, game_field)

        elif choices == 1:
            values = list(self.turn_directions.values())
            keys = list(self.turn_directions.keys())
            position = values.index(True)
            self.turn(keys[position], game_field)

    def check_cell(self, game_field):
        self.cell = [int(self.y // game_field.grid_size), int(self.x // game_field.grid_size)]
