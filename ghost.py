import pygame
import math

class Ghost:
    def __init__(self, game_field):
        self.__x = 10 * game_field.getGridSize() + game_field.getGridSize() / 2
        self.__y = 9 * game_field.getGridSize() + game_field.getGridSize() / 2
        self.__radius = game_field.getGridSize() / 2
        self.__direction = "up"
        self.__size = game_field.getGridSize()
        self.__color = "red"
        self.__cell = [int(self.__y // game_field.getGridSize()), int(self.__x // game_field.getGridSize())]
        self.__speed = 0.1
        self.__target_cell = []
        self.__turn_directions = {"left": False, "right": False, "up": False, "down": False }

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

    def getSpeed(self):
        return self.__speed

    def draw(self, screen):
        pygame.draw.circle(screen.getWindow(), self.__color, (self.__x, self.__y), self.__radius, self.__size)
        pygame.draw.rect(screen.getWindow(), self.__color, (self.__x - self.__radius, self.__y, 2*self.__radius, self.__radius))
    def setTarget(self, pacman):
        if self.__cell != [9, 9] and self.__cell != [9, 10] and self.__cell != [9, 11]:
            self.__target_cell = pacman.getCell()
        else:
            self.__target_cell = [10, 7]
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

    def checkNeighbourCells(self, game_field):
        if self.__cell[1] <= 0 or self.__cell[1] >= game_field.getCols() - 1:
            self.__turn_directions["left"] = True
            self.__turn_directions["right"] = True
        else:
            # left cell
            if game_field.getMatrix()[self.__cell[0]][self.__cell[1] - 1] != 1:
                self.__turn_directions["left"] = True
            else:
                self.__turn_directions["left"] = False
            # right cell
            if game_field.getMatrix()[self.__cell[0]][self.__cell[1] + 1] != 1:
                self.__turn_directions["right"] = True
            else:
                self.__turn_directions["right"] = False
            # top cell
            if game_field.getMatrix()[self.__cell[0] - 1][self.__cell[1]] != 1:
                self.__turn_directions["up"] = True
            else:
                self.__turn_directions["up"] = False
            # bottom cell
            if game_field.getMatrix()[self.__cell[0] + 1][self.__cell[1]] != 1:
                self.__turn_directions["down"] = True
            else:
                self.__turn_directions["down"] = False

    def getNeighbourCell(self, direction):
        if direction == "left":
            return [self.__cell[0], self.__cell[1] - 1]
        elif direction == "right":
            return [self.__cell[0], self.__cell[1] + 1]
        elif direction == "up":
            return [self.__cell[0] - 1, self.__cell[1]]
        elif direction == "down":
            return [self.__cell[0] + 1, self.__cell[1]]

    def makeChoice(self, directions):
        cells = []
        for direction in directions:
            cells.append(self.getNeighbourCell(direction))
        distances = []
        for cell in cells:
            distances.append(math.sqrt(math.pow((self.__target_cell[0] - cell[0]), 2) + math.pow((self.__target_cell[1] - cell[1]), 2)))
        for i in range(len(distances)):
            if distances[i] == min(distances):
                return directions[i]

    def turn(self, next_direction, game_field):
        if self.__cell[1] * game_field.getGridSize() + self.__radius - 1 <= self.__x <= self.__cell[1] * game_field.getGridSize() + self.__radius + 1 and self.__cell[0] * game_field.getGridSize() + self.__radius - 1 <= self.__y <= self.__cell[0] * game_field.getGridSize() + self.__radius + 1:
            self.__direction = next_direction
    def changeDirection(self, game_field):
        self.checkNeighbourCells(game_field)
        is_in_impasse = True
        if self.__direction == "left":
            self.__turn_directions["right"] = False
        elif self.__direction == "right":
            self.__turn_directions["left"] = False
        elif self.__direction == "up":
            self.__turn_directions["down"] = False
        elif self.__direction == "down":
            self.__turn_directions["up"] = False
        for direction in self.__turn_directions.values():
            if direction:
                is_in_impasse = False
        if is_in_impasse:
            if self.__direction == "left":
                self.__turn_directions["right"] = True
            elif self.__direction == "right":
                self.__turn_directions["left"] = True
            elif self.__direction == "up":
                self.__turn_directions["down"] = True
            elif self.__direction == "down":
                self.__turn_directions["up"] = True
        choices = 0
        for turn_direction in self.__turn_directions.values():
            if turn_direction == True:
                choices += 1
        if choices > 1:
            keys = list(self.__turn_directions.keys())
            i = 0
            directions = []
            for turn_direction in self.__turn_directions.values():
                if turn_direction == True:
                    directions.append(keys[i])
                i += 1
            next_direction = self.makeChoice(directions)
            self.turn(next_direction, game_field)

        elif choices == 1:
            values = list(self.__turn_directions.values())
            keys = list(self.__turn_directions.keys())
            position = values.index(True)
            self.turn(keys[position], game_field)
