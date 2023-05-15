import pygame
from pygame.locals import *
from constants import *

class Pacman:
    def __init__(self):
        self.x = PACMAN_START_X
        self.y = PACMAN_START_Y
        self.radius = GRID_SIZE / 2
        self.direction = "right"
    def move(self, dt):
        if self.direction == "right":
            self.x += PACMAN_SPEED * dt
        elif self.direction == "left":
            self.x -= PACMAN_SPEED * dt
        elif self.direction == "up":
            self.y -= PACMAN_SPEED * dt
        elif self.direction == "down":
            self.y += PACMAN_SPEED * dt
    def can_turn(self, direcion): #detects wether pacman can move in the specific direction
        current_pos = [int(self.y // GRID_SIZE), int(self.x // GRID_SIZE)]
        if direcion == "left" and GAME_FIELD[current_pos[0]][current_pos[1] - 1] == 0:
            return True
        elif direcion == "right" and GAME_FIELD[current_pos[0]][current_pos[1] + 1] == 0:
            return True
        elif direcion == "up" and GAME_FIELD[current_pos[0] - 1][current_pos[1]] == 0:
            return True
        elif direcion == "down" and GAME_FIELD[current_pos[0] + 1][current_pos[1]] == 0:
            return True
        return False
    def draw(self):
        pygame.draw.circle(screen, "yellow", (self.x, self.y), self.radius, PACMAN_SIZE)
def draw_grid():
    for y in range(ROWS):
        for x in range(COLS):
            pygame.draw.rect(screen, GRID_COLOR, [x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE], 1)

def draw_field():
    for y in range(ROWS):
        for x in range(COLS):
            if GAME_FIELD[y][x] == 1:
                pygame.draw.rect(screen, WALL_COLOR, [x * GRID_SIZE + 1, y * GRID_SIZE + 1, GRID_SIZE - 2, GRID_SIZE - 2])

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pacman")

pacman = Pacman()

clock = pygame.time.Clock()

blocks_rect = []
for y in range(ROWS):
    for x in range(COLS):
        if GAME_FIELD[y][x] == 1:
            blocks_rect.append([x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE])

game_over = False

while not game_over:
    dt = clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            game_over = True
    pressed = pygame.key.get_pressed()
    if pressed[K_LEFT]:
        if pacman.can_turn("left"):
            pacman.direction = "left"
    if pressed[K_RIGHT]:
        if pacman.can_turn("right"):
            pacman.direction = "right"
    if pressed[K_UP]:
        if pacman.can_turn("up"):
            pacman.direction = "up"
    if pressed[K_DOWN]:
        if pacman.can_turn("down"):
            pacman.direction = "down"
    screen.fill(BACKGROUND_COLOR)
    draw_grid()
    draw_field()
    pacman.draw()
    #pacman-block collisions
    for block in blocks_rect:
        #right collision
        if pacman.direction == "right" and block[0] - pacman.radius <= pacman.x <= block[0] + block[2] - pacman.radius and block[1] <= pacman.y <= block[1] + block[3]:
            pacman.x = block[0] - pacman.radius
        #left collision
        if pacman.direction == "left" and block[0] + pacman.radius <= pacman.x <= block[0] + block[2] + pacman.radius and block[1] <= pacman.y <= block[1] + block[3]:
            pacman.x = block[0] + block[2] + pacman.radius
        #top collision
        if pacman.direction == "up" and block[0] <= pacman.x <= block[0] + block[2] and block[1] + pacman.radius <= pacman.y <= block[1] + block[3] + pacman.radius:
            pacman.y = block[1] + block[2] + pacman.radius
        #bottom collision
        if pacman.direction == "down" and block[0] <= pacman.x <= block[0] + block[2] and block[1] - pacman.radius <= pacman.y <= block[1] + block[3] - pacman.radius:
            pacman.y = block[1] - pacman.radius

    pacman.move(dt)
    pygame.display.update()

pygame.quit()