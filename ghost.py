import pygame
import math
import random

class Ghost:
    def __init__(self, game_field):
        self._x = 10 * game_field.getGridSize() + game_field.getGridSize() / 2
        self._y = 9 * game_field.getGridSize() + game_field.getGridSize() / 2
        self._radius = game_field.getGridSize() / 2
        self._direction = "up"
        self._size = game_field.getGridSize()
        self._color = "red"
        self._cell = [int(self._y // game_field.getGridSize()), int(self._x // game_field.getGridSize())]
        self._speed = 0.1
        self._target_cell = []
        self._turn_directions = {"left": False, "right": False, "up": False, "down": False}

    def setX(self, x):
        self._x = x

    def setY(self, y):
        self._y = y

    def setDirection(self, direction):
        self._direction = direction

    def setCell(self, game_field):
        self._cell = [int(self._y // game_field.getGridSize()), int(self._x // game_field.getGridSize())]

    def getX(self):
        return self._x

    def getY(self):
        return self._y

    def getRadius(self):
        return self._radius

    def getSize(self):
        return self._size

    def getDirection(self):
        return self._direction

    def getCell(self):
        return self._cell

    def getSpeed(self):
        return self._speed

    def draw(self, screen):
        pygame.draw.circle(screen.getWindow(), self._color, (self._x, self._y), self._radius, self._size)
        pygame.draw.rect(screen.getWindow(), self._color, (self._x - self._radius, self._y, 2 * self._radius, self._radius))

    def reset(self, game_field):
        self._x = 10 * game_field.getGridSize() + game_field.getGridSize() / 2
        self._y = 9 * game_field.getGridSize() + game_field.getGridSize() / 2
        self._direction = "up"

    def setTarget(self, pacman):
        if self._cell != [9, 9] and self._cell != [9, 10] and self._cell != [9, 11]:
            self._target_cell = pacman.getCell()
        else:
            self._target_cell = [10, 7]
    def move(self, dt, screen):
        if self._x < 0 - self._radius:
            self._x = screen.getWidth() + self._radius
        elif self._x > screen.getWidth() + self._radius:
            self._x = 0 - self._radius
        if self._direction == "right":
            self._x += self._speed * dt
        elif self._direction == "left":
            self._x -= self._speed * dt
        elif self._direction == "up":
            self._y -= self._speed * dt
        elif self._direction == "down":
            self._y += self._speed * dt

    def checkNeighbourCells(self, game_field):
        if self._cell[1] <= 0 or self._cell[1] >= game_field.getCols() - 1:
            self._turn_directions["left"] = True
            self._turn_directions["right"] = True
        else:
            # left cell
            if game_field.getMatrix()[self._cell[0]][self._cell[1] - 1] != 1:
                self._turn_directions["left"] = True
            else:
                self._turn_directions["left"] = False
            # right cell
            if game_field.getMatrix()[self._cell[0]][self._cell[1] + 1] != 1:
                self._turn_directions["right"] = True
            else:
                self._turn_directions["right"] = False
            # top cell
            if game_field.getMatrix()[self._cell[0] - 1][self._cell[1]] != 1:
                self._turn_directions["up"] = True
            else:
                self._turn_directions["up"] = False
            # bottom cell
            if game_field.getMatrix()[self._cell[0] + 1][self._cell[1]] != 1:
                self._turn_directions["down"] = True
            else:
                self._turn_directions["down"] = False

    def getNeighbourCell(self, direction):
        if direction == "left":
            return [self._cell[0], self._cell[1] - 1]
        elif direction == "right":
            return [self._cell[0], self._cell[1] + 1]
        elif direction == "up":
            return [self._cell[0] - 1, self._cell[1]]
        elif direction == "down":
            return [self._cell[0] + 1, self._cell[1]]

    def makeChoice(self, directions):
        cells = []
        for direction in directions:
            cells.append(self.getNeighbourCell(direction))
        distances = []
        for cell in cells:
            distances.append(math.sqrt(math.pow((self._target_cell[0] - cell[0]), 2) + math.pow((self._target_cell[1] - cell[1]), 2)))
        for i in range(len(distances)):
            if distances[i] == min(distances):
                return directions[i]

    def turn(self, next_direction, game_field):
        if self._cell[1] * game_field.getGridSize() + self._radius - 1 <= self._x <= self._cell[1] * game_field.getGridSize() + self._radius + 1 and self._cell[0] * game_field.getGridSize() + self._radius - 1 <= self._y <= self._cell[0] * game_field.getGridSize() + self._radius + 1:
            self._direction = next_direction
    def changeDirection(self, game_field):
        self.checkNeighbourCells(game_field)
        is_in_impasse = True
        if self._direction == "left":
            self._turn_directions["right"] = False
        elif self._direction == "right":
            self._turn_directions["left"] = False
        elif self._direction == "up":
            self._turn_directions["down"] = False
        elif self._direction == "down":
            self._turn_directions["up"] = False
        for direction in self._turn_directions.values():
            if direction:
                is_in_impasse = False
        if is_in_impasse:
            if self._direction == "left":
                self._turn_directions["right"] = True
            elif self._direction == "right":
                self._turn_directions["left"] = True
            elif self._direction == "up":
                self._turn_directions["down"] = True
            elif self._direction == "down":
                self._turn_directions["up"] = True
        choices = 0
        for turn_direction in self._turn_directions.values():
            if turn_direction == True:
                choices += 1
        if choices > 1:
            keys = list(self._turn_directions.keys())
            i = 0
            directions = []
            for turn_direction in self._turn_directions.values():
                if turn_direction == True:
                    directions.append(keys[i])
                i += 1
            next_direction = self.makeChoice(directions)
            self.turn(next_direction, game_field)

        elif choices == 1:
            values = list(self._turn_directions.values())
            keys = list(self._turn_directions.keys())
            position = values.index(True)
            self.turn(keys[position], game_field)

    def pacmanCollision(self, pacman):
        if pacman.getX() - self._radius / 3 <= self._x <= pacman.getX() + self._radius / 3 and pacman.getY() - self._radius / 3 <= self._y <= pacman.getY() + self._radius / 3:
            return True
        else:
            return False

class GhostGuardian(Ghost):

    def __init__(self, game_field):
        super().__init__(game_field)
        self._color = "pink"
        self._bonus_target = []

    def setX(self, x):
        super().setX(x)

    def setY(self, y):
        super().setY(y)

    def setDirection(self, direction):
        super().setDirection(direction)

    def setCell(self, game_field):
        super().setCell(game_field)

    def setBonusTarget(self, bonus):
        if bonus.getCords() == []:
            return None
        for bonus_cords in bonus.getCords():
            if self._bonus_target == bonus_cords:
                return None
        self._bonus_target = random.choice(bonus.getCords())
        print("bonus target reset")

    def getX(self):
        return super().getX()

    def getY(self):
        return super().getY()

    def getRadius(self):
        return super().getRadius()

    def getSize(self):
        return super().getSize()

    def getDirection(self):
        return super().getDirection()

    def getCell(self):
        return super().getCell()

    def getSpeed(self):
        return super().getSpeed()

    def draw(self, screen):
        super().draw(screen)

    def reset(self, game_field):
        super().reset(game_field)

    def setTarget(self, bonus, game_field):
        if self._cell != [9, 9] and self._cell != [9, 10] and self._cell != [9, 11]:
            self._target_cell = [self._bonus_target[1] // game_field.getGridSize(), self._bonus_target[0] // game_field.getGridSize()]
        else:
            self._target_cell = [10, 7]
    def move(self, dt, screen):
        super().move(dt, screen)

    def checkNeighbourCells(self, game_field):
        super().checkNeighbourCells(game_field)

    def getNeighbourCell(self, direction):
        return super().getNeighbourCell(direction)

    def makeChoice(self, directions):
        return super().makeChoice(directions)

    def turn(self, next_direction, game_field):
        super().turn(next_direction, game_field)
    def changeDirection(self, game_field):
        super().changeDirection(game_field)

    def pacmanCollision(self, pacman):
        return super().pacmanCollision(pacman)
