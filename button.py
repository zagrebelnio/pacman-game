import pygame

class Button:
    def __init__(self, text, x, y):
        self._x = x
        self._y = y
        self._width = 350
        self._height = 125
        self.__color = "yellow"
        self.__hover_color = "red"
        self.__font = pygame.font.Font("fonts/Pixeboy-z8XGD.ttf", 50)
        self.__text = self.__font.render(text, True, self.__color)
        self.__text_rect = [self._x + (self._width - self.__text.get_width()) // 2, self._y + (self._height - self.__text.get_height()) // 2, self.__text.get_width(), self.__text.get_height()]
        self._sound = pygame.mixer.Sound("sounds/button/one_beep-99630.mp3")

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        if self._x <= mouse_pos[0] <= self._x + self._width and self._y <= mouse_pos[1] <= self._y + self._height:
            current_color = self.__hover_color
        else:
            current_color = self.__color
        pygame.draw.rect(screen.getWindow(), current_color, [self._x, self._y, self._width, self._height], 10, 40)
        screen.showText(self.__text, self.__text_rect)

    def checkClick(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if self._x <= mouse_pos[0] <= self._x + self._width and self._y <= mouse_pos[1] <= self._y + self._height:
                pygame.mixer.Sound.play(self._sound)
                return True
            return False

class ImageButton(Button):
    def __init__(self, x, y, width, height, path, rotation = 0):
        text = ""
        super().__init__(text, x, y)
        self._width = width
        self._height = height
        self.__image = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(path), (self._width, self._height)), rotation)

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        screen.showImage(self.__image, self._x, self._y)
        if self._x <= mouse_pos[0] <= self._x + self._width and self._y <= mouse_pos[1] <= self._y + self._height:
            pygame.draw.rect(screen.getWindow(), "red", [self._x, self._y, self._width, self._height], 3, 90)

    def checkClick(self, event):
        return super().checkClick(event)