import pygame

class Button:
    def __init__(self, text, x, y):
        self.__x = x
        self.__y = y
        self.__width = 350
        self.__height = 125
        self.__color = "yellow"
        self.__hover_color = "red"
        self.__size = 50
        self.__font = pygame.font.Font("fonts/Pixeboy-z8XGD.ttf", 50)
        self.__text = self.__font.render(text, True, self.__color)
        self.__text_rect = [self.__x + (self.__width - self.__text.get_width()) // 2, self.__y + (self.__height - self.__text.get_height()) // 2, self.__text.get_width(), self.__text.get_height()]

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        if self.__x <= mouse_pos[0] <= self.__x + self.__width and self.__y <= mouse_pos[1] <= self.__y + self.__height:
            current_color = self.__hover_color
        else:
            current_color = self.__color
        pygame.draw.rect(screen.getWindow(), current_color, [self.__x, self.__y, self.__width, self.__height], 10, 40)
        screen.showText(self.__text, self.__text_rect)

    def checkClick(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if self.__x <= mouse_pos[0] <= self.__x + self.__width and self.__y <= mouse_pos[1] <= self.__y + self.__height:
                return True
            return False
