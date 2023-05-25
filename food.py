import pygame

class Food:
    def __init__(self, game_field):
        self._cords = []
        self._size = game_field.getGridSize() // 5
        self._radius = self._size / 2
        self._color = "white"

    def getCords(self):
        return self._cords


    def reset(self, game_field):
        for y in range(game_field.getRows()):
            for x in range(game_field.getCols()):
                if game_field.getMatrix()[y][x] == 0:
                    self._cords.append(((x * game_field.getGridSize()) + game_field.getGridSize() / 2, (y * game_field.getGridSize()) + game_field.getGridSize() / 2))

    def draw(self, screen):
        for cord in self._cords:
            pygame.draw.circle(screen.getWindow(), self._color, cord, self._radius, self._size)

    def eat(self, pacman):
        for i in range(len(self._cords)):
            if self._cords[i][0] - pacman.getRadius() + self._radius <= pacman.getX() <= self._cords[i][0] + pacman.getRadius() - self._radius and self._cords[i][1] - pacman.getRadius() + self._radius <= pacman.getY() <= self._cords[i][1] + pacman.getRadius() - self._radius:
                self._cords.pop(i)
                break

class Bonus(Food):

    def __init__(self, game_field):
        super().__init__(game_field)
        self._size = game_field.getGridSize() // 2
        self._radius = self._size / 2

    def getCords(self):
        return self._cords

    def reset(self, game_field):
        for y in range(game_field.getRows()):
            for x in range(game_field.getCols()):
                if game_field.getMatrix()[y][x] == 2:
                    self._cords.append(((x * game_field.getGridSize()) + game_field.getGridSize() / 2, (y * game_field.getGridSize()) + game_field.getGridSize() / 2))

    def draw(self, screen):
        super().draw(screen)

    def eat(self, pacman):
        super().eat(pacman)