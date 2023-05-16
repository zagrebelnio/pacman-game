from pygame.locals import *
from pacman import *
from food import *
from block import *

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

food = Food()
food.reset()
block = Block()
block.reset()

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
    food.draw(screen)
    food.eat(pacman)
    block.check_wall_collisions(pacman)
    pacman.draw(screen)

    if food.cords == []:
        game_over = True

    pacman.move(dt)
    pygame.display.update()

pygame.quit()