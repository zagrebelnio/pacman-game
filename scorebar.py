import pygame

class ScoreBar:
    def __init__(self, game_field, screen):
        self.__width = game_field.getGridSize() * game_field.getCols()
        self.__height = screen.getHeight() - game_field.getGridSize() * game_field.getRows()
        self.__x = 0
        self.__y = game_field.getGridSize() * game_field.getRows()
        self.__font = pygame.font.Font("fonts/Pixeboy-z8XGD.ttf", 48)
        self.__score = 0
        self.__lifes = 3

    def draw(self, screen):
        score = self.__font.render(f"SCORE: {self.__score}", True, "white")
        score_rect = [self.__x + 10, self.__y + (self.__height - score.get_height()) // 2, score.get_width(), score.get_height()]
        screen.showText(score, score_rect)
        lifes = self.__font.render(f"LIFES: {self.__lifes}", True, "white")
        lifes_rect = [screen.getWidth() * 2 / 3 + 10, self.__y + (self.__height - lifes.get_height()) // 2, lifes.get_width(),
                      lifes.get_height()]
        screen.showText(lifes, lifes_rect)

    def setLifes(self, pacman):
        self.__lifes = pacman.getLifes()

    def increaseScore(self, points):
        self.__score += points

    def getScore(self):
        return self.__score