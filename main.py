import pygame
from constants import *

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

game_over = False

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            game_over = True

    screen.fill(BACKGROUND_COLOR)
    draw_grid()
    draw_field()
    pygame.display.update()

pygame.quit()