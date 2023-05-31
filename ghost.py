import pygame
import math
import random
import os

class Ghost:
    def __init__(self, game_field):
        self._x = random.randint(9 * game_field.getGridSize() + game_field.getGridSize() / 2, 11 * game_field.getGridSize() + game_field.getGridSize() / 2)
        self._y = 9 * game_field.getGridSize() + game_field.getGridSize() / 2
        self._radius = game_field.getGridSize() / 2
        self._direction = "right"
        self._size = game_field.getGridSize()
        self._color = "red"
        self._initial_color = "red"
        self._cell = [int(self._y // game_field.getGridSize()), int(self._x // game_field.getGridSize())]
        self._speed = 0.11
        self._target_cell = []
        self._turn_directions = {"left": False, "right": False, "up": False, "down": False}
        self._status = "alive"
        self._previous_cell = []
        self._frames = []
        self._path = "images/ghosts_frames"
        self._counter = 0

    def _setFrames(self):
        self._frames.clear()
        path = self._path + os.sep + self._color + os.sep + self._direction
        for file_name in os.listdir(path):
            frame = pygame.transform.scale(pygame.image.load(path + os.sep + file_name),
                                           (self._size, self._size))
            self._frames.append(frame)

    def setX(self, x):
        self._x = x

    def setY(self, y):
        self._y = y

    def setDirection(self, direction):
        self._direction = direction

    def setCell(self, game_field):
        self._cell = [int(self._y // game_field.getGridSize()), int(self._x // game_field.getGridSize())]
        if self._cell == [9, 9] or self._cell == [9, 10] or self._cell == [9, 11]:
            self._status = "alive"
            self._speed = 0.11
            self._color = self._initial_color

    def setSpeed(self, speed):
        self._speed = speed

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

    def draw(self, screen, game_field):
        if game_field.getStatus() == "bonused" and self.isAlive():
            self._color = "scared"
        elif game_field.getStatus() == "normal" and self.isAlive():
            self._color = self._initial_color
        self._setFrames()
        divider = 15
        if self._counter < len(self._frames) * divider - 1:
            self._counter += 1
        else:
            self._counter = 0
        if self._direction == "left":
            screen.showImage(self._frames[self._counter // divider], self._x - self._radius, self._y - self._radius)
        elif self._direction == "right":
            screen.showImage(self._frames[self._counter // divider], self._x - self._radius, self._y - self._radius)
        elif self._direction == "up":
            screen.showImage(self._frames[self._counter // divider], self._x - self._radius, self._y - self._radius)
        elif self._direction == "down":
            screen.showImage(self._frames[self._counter // divider], self._x - self._radius, self._y - self._radius)

    def reset(self, game_field):
        self._x = random.randint(9 * game_field.getGridSize() + game_field.getGridSize() / 2, 11 * game_field.getGridSize() + game_field.getGridSize() / 2)
        self._y = 9 * game_field.getGridSize() + game_field.getGridSize() / 2
        self._direction = "right"
        self._previous_cell = []

    def setTarget(self, pacman):
        if self._status == "died":
            self._target_cell = [8, 10]
        elif self._status == "alive":
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

    def _checkNeighbourCells(self, game_field, door):
        if self._cell[1] <= 0 or self._cell[1] >= game_field.getCols() - 1:
            self._turn_directions["left"] = True
            self._turn_directions["right"] = True
        else:
            # left cell
            if game_field.getMatrix()[self._cell[0]][self._cell[1] - 1] <= 2:
                self._turn_directions["left"] = True
            else:
                self._turn_directions["left"] = False
            # right cell
            if game_field.getMatrix()[self._cell[0]][self._cell[1] + 1] <= 2:
                self._turn_directions["right"] = True
            else:
                self._turn_directions["right"] = False
            # top cell
            if game_field.getMatrix()[self._cell[0] - 1][self._cell[1]] <= 2:
                if game_field.getMatrix()[self._cell[0] - 1][self._cell[1]] == 2 and door.getStatus() == "closed":
                    self._turn_directions["up"] = False
                else:
                    self._turn_directions["up"] = True
            else:
                self._turn_directions["up"] = False
            # bottom cell
            if game_field.getMatrix()[self._cell[0] + 1][self._cell[1]] <= 2:
                if game_field.getMatrix()[self._cell[0] + 1][self._cell[1]] == 2 and door.getStatus() == "closed":
                    self._turn_directions["down"] = False
                else:
                    self._turn_directions["down"] = True
            else:
                self._turn_directions["down"] = False

    def _getNeighbourCell(self, direction):
        if direction == "left":
            return [self._cell[0], self._cell[1] - 1]
        elif direction == "right":
            return [self._cell[0], self._cell[1] + 1]
        elif direction == "up":
            return [self._cell[0] - 1, self._cell[1]]
        elif direction == "down":
            return [self._cell[0] + 1, self._cell[1]]

    def _makeChoice(self, directions, game_field, pacman):
        cells = []
        for direction in directions:
            cells.append(self._getNeighbourCell(direction))
        distances = []
        if game_field.getStatus() == "normal" or self._status == "died":
            for cell in cells:
                distances.append(math.sqrt(math.pow((self._target_cell[0] - cell[0]), 2) + math.pow((self._target_cell[1] - cell[1]), 2)))
            for i in range(len(distances)):
                if distances[i] == min(distances):
                    return directions[i]
        elif game_field.getStatus() == "bonused":
            for cell in cells:
                distances.append(math.sqrt(math.pow((pacman.getCell()[0] - cell[0]), 2) + math.pow((pacman.getCell()[1] - cell[1]), 2)))
            for i in range(len(distances)):
                if distances[i] == max(distances):
                    return directions[i]

    def _turn(self, next_direction, game_field):
        if self._cell[1] * game_field.getGridSize() + self._radius - 1 <= self._x <= self._cell[1] * game_field.getGridSize() + self._radius + 1 and self._cell[0] * game_field.getGridSize() + self._radius - 1 <= self._y <= self._cell[0] * game_field.getGridSize() + self._radius + 1:
            if self.getCell() != self._previous_cell:
                self._direction = next_direction
                self._previous_cell = self.getCell()
    def changeDirection(self, game_field, door, pacman):
        self._checkNeighbourCells(game_field, door)
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
            next_direction = self._makeChoice(directions, game_field, pacman)
            self._turn(next_direction, game_field)

        elif choices == 1:
            values = list(self._turn_directions.values())
            keys = list(self._turn_directions.keys())
            position = values.index(True)
            self._turn(keys[position], game_field)

    def pacmanCollision(self, pacman):
        if pacman.getX() - self._radius / 3 <= self._x <= pacman.getX() + self._radius / 3 and pacman.getY() - self._radius / 3 <= self._y <= pacman.getY() + self._radius / 3:
            return True
        else:
            return False

    def killed(self):
        self._status = "died"
        self._color = "dead"
        self._speed = 0.25

    def isAlive(self):
        if self._status == "alive":
            return True
        else:
            return False

class GhostGuardian(Ghost):

    def __init__(self, game_field):
        super().__init__(game_field)
        self._color = "pink"
        self._initial_color = "pink"
        self._bonus_target = []

    def _setFrames(self):
        super()._setFrames()

    def setX(self, x):
        super().setX(x)

    def setY(self, y):
        super().setY(y)

    def setDirection(self, direction):
        super().setDirection(direction)

    def setCell(self, game_field):
        super().setCell(game_field)

    def setSpeed(self, speed):
        super().setSpeed(speed)

    def setBonusTarget(self, bonus):
        if bonus.getCords() == []:
            return None
        for bonus_cords in bonus.getCords():
            if self._bonus_target == bonus_cords:
                return None
        self._bonus_target = random.choice(bonus.getCords())

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

    def draw(self, screen, game_field):
        super().draw(screen, game_field)

    def reset(self, game_field):
        super().reset(game_field)

    def setTarget(self, bonus, game_field):
        if self._status == "died":
            self._target_cell = [8, 10]
        elif self._status == "alive":
            if self._cell != [9, 9] and self._cell != [9, 10] and self._cell != [9, 11]:
                self._target_cell = [self._bonus_target[1] // game_field.getGridSize(), self._bonus_target[0] // game_field.getGridSize()]
            else:
                self._target_cell = [10, 7]
    def move(self, dt, screen):
        super().move(dt, screen)

    def _checkNeighbourCells(self, game_field, door):
        super()._checkNeighbourCells(game_field, door)

    def _getNeighbourCell(self, direction):
        return super()._getNeighbourCell(direction)

    def _makeChoice(self, directions, game_field, pacman):
        return super()._makeChoice(directions, game_field, pacman)

    def _turn(self, next_direction, game_field):
        super()._turn(next_direction, game_field)
    def changeDirection(self, game_field, door, pacman):
        super().changeDirection(game_field, door, pacman)

    def pacmanCollision(self, pacman):
        return super().pacmanCollision(pacman)

    def killed(self):
        super().killed()

    def isAlive(self):
        return super().isAlive()

class GhostPatrol(Ghost):

    def __init__(self, game_field):
        super().__init__(game_field)
        self._color = "lightblue"
        self._initial_color = "lightblue"
        self._possible_areas = [[3, 7, 5, 15], [11, 15, 5, 15]]
        self._patrol_area = random.choice(self._possible_areas)
        self._patrol_area_target = []
        self._path = "images/ghosts_frames"

    def _setFrames(self):
        super()._setFrames()

    def setX(self, x):
        super().setX(x)

    def setY(self, y):
        super().setY(y)

    def setDirection(self, direction):
        super().setDirection(direction)

    def setCell(self, game_field):
        super().setCell(game_field)
        if self._cell == self._target_cell:
            self.setPatrolAreaTarget(game_field)

    def setSpeed(self, speed):
        super().setSpeed(speed)

    def setPatrolAreaTarget(self, game_field):
        target = [random.randint(self._patrol_area[0], self._patrol_area[1]),
                  random.randint(self._patrol_area[2], self._patrol_area[3])]
        if game_field.getMatrix()[target[0]][target[1]] != 1:
            self._patrol_area_target = target
        else:
            self.setPatrolAreaTarget(game_field)

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

    def draw(self, screen, game_field):
        super().draw(screen, game_field)

    def reset(self, game_field):
        super().reset(game_field)

    def setTarget(self, game_field):
        if self._status == "died":
            self._target_cell = [8, 10]
        elif self._status == "alive":
            if self._cell != [9, 9] and self._cell != [9, 10] and self._cell != [9, 11]:
                self._target_cell = self._patrol_area_target
            else:
                self._target_cell = [10, 7]
    def move(self, dt, screen):
        super().move(dt, screen)

    def _checkNeighbourCells(self, game_field, door):
        super()._checkNeighbourCells(game_field, door)

    def _getNeighbourCell(self, direction):
        return super()._getNeighbourCell(direction)

    def _makeChoice(self, directions, game_field, pacman):
        return super()._makeChoice(directions, game_field, pacman)

    def _turn(self, next_direction, game_field):
        super()._turn(next_direction, game_field)
    def changeDirection(self, game_field, door, pacman):
        super().changeDirection(game_field, door, pacman)

    def pacmanCollision(self, pacman):
        return super().pacmanCollision(pacman)

    def killed(self):
        super().killed()

    def isAlive(self):
        return super().isAlive()

class GhostHaunter(Ghost):

    def __init__(self, game_field):
        super().__init__(game_field)
        self._color = "orange"
        self._initial_color = "orange"
        self._path = "images/ghosts_frames"

    def _setFrames(self):
        super()._setFrames()

    def setX(self, x):
        super().setX(x)

    def setY(self, y):
        super().setY(y)

    def setDirection(self, direction):
        super().setDirection(direction)

    def setCell(self, game_field):
        super().setCell(game_field)

    def setSpeed(self, speed):
        super().setSpeed(speed)

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

    def draw(self, screen, game_field):
        super().draw(screen, game_field)

    def reset(self, game_field):
        super().reset(game_field)

    def setTarget(self, pacman):
        if self._status == "died":
            self._target_cell = [8, 10]
        elif self._status == "alive":
            if self._cell != [9, 9] and self._cell != [9, 10] and self._cell != [9, 11]:
                target = pacman.getCell()
                if pacman.getDirection() == "left":
                    self._target_cell = [target[0], target[1] - 2]
                elif pacman.getDirection() == "right":
                    self._target_cell = [target[0], target[1] + 2]
                elif pacman.getDirection() == "up":
                    self._target_cell = [target[0] - 2, target[1]]
                elif pacman.getDirection() == "down":
                    self._target_cell = [target[0] + 2, target[1]]
            else:
                self._target_cell = [10, 7]
    def move(self, dt, screen):
        super().move(dt, screen)

    def _checkNeighbourCells(self, game_field, door):
        super()._checkNeighbourCells(game_field, door)

    def _getNeighbourCell(self, direction):
        return super()._getNeighbourCell(direction)

    def _makeChoice(self, directions, game_field, pacman):
        return super()._makeChoice(directions, game_field, pacman)

    def _turn(self, next_direction, game_field):
        super()._turn(next_direction, game_field)
    def changeDirection(self, game_field, door, pacman):
        super().changeDirection(game_field, door, pacman)

    def pacmanCollision(self, pacman):
        return super().pacmanCollision(pacman)

    def killed(self):
        super().killed()

    def isAlive(self):
        return super().isAlive()