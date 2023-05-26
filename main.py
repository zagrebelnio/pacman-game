import pygame.time
from pygame.locals import *
from gamefield import *
from screen import *
from pacman import *
from food import *
from block import *
from ghost import *
from door import *

pygame.init()

game_field = GameField()
screen = Screen(game_field)
pygame.display.set_caption("Pacman")

pacman = Pacman(game_field)

clock = pygame.time.Clock()

food = Food(game_field)
food.reset(game_field)
bonus = Bonus(game_field)
bonus.reset(game_field)
block = Block()
block.reset(game_field)
ghost = Ghost(game_field)
ghost_guardian = GhostGuardian(game_field)
ghost_patrol = GhostPatrol(game_field)
ghost_patrol.setPatrolAreaTarget(game_field)
ghost_haunter = GhostHaunter(game_field)
door = Door(game_field)

game_over = False
start_time = pygame.time.get_ticks() / 1000
bonused_start = None

while not game_over:
    if pygame.time.get_ticks() / 1000 - start_time > 5:
        door.open()
    dt = clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            game_over = True
    pressed = pygame.key.get_pressed()
    if pressed[K_LEFT]:
        if pacman.can_turn("left", game_field):
            pacman.setDirection("left")
    if pressed[K_RIGHT]:
        if pacman.can_turn("right", game_field):
            pacman.setDirection("right")
    if pressed[K_UP]:
        if pacman.can_turn("up", game_field):
            pacman.setDirection("up")
    if pressed[K_DOWN]:
        if pacman.can_turn("down", game_field):
            pacman.setDirection("down")
    screen.fill()
    game_field.draw(screen)
    door.draw(screen)
    game_field.drawGrid(screen)
    food.draw(screen)
    food.eat(pacman)
    bonus.draw(screen)
    if bonus.eat(pacman):
        bonused_start = pygame.time.get_ticks() / 1000
        game_field.setStatus("bonused")

    if game_field.getStatus() == "bonused":
        if ghost.isAlive():
            ghost.setSpeed(0.08)
        if ghost_patrol.isAlive():
            ghost_patrol.setSpeed(0.08)
        if ghost_guardian.isAlive():
            ghost_guardian.setSpeed(0.08)
        if ghost_haunter.isAlive():
            ghost_haunter.setSpeed(0.08)

    if bonused_start != None:
        if pygame.time.get_ticks() / 1000 - bonused_start > 15:
            game_field.setStatus("normal")
            if ghost.isAlive():
                ghost.setSpeed(0.1)
            if ghost_patrol.isAlive():
                ghost_patrol.setSpeed(0.1)
            if ghost_guardian.isAlive():
                ghost_guardian.setSpeed(0.1)
            if ghost_haunter.isAlive():
                ghost_haunter.setSpeed(0.1)
            bonused_start = None
    block.check_wall_collisions(pacman)
    block.check_wall_collisions(ghost)
    block.check_wall_collisions(ghost_guardian)
    block.check_wall_collisions(ghost_patrol)
    block.check_wall_collisions(ghost_haunter)
    pacman.draw(screen)
    pacman.setCell(game_field)
    ghost.draw(screen)
    ghost.setTarget(pacman)
    ghost.changeDirection(game_field, door, pacman)
    ghost.move(dt, screen)
    ghost.setCell(game_field)
    ghost_guardian.draw(screen)
    ghost_guardian.setBonusTarget(bonus)
    ghost_guardian.setTarget(bonus, game_field)
    ghost_guardian.changeDirection(game_field, door, pacman)
    ghost_guardian.move(dt, screen)
    ghost_guardian.setCell(game_field)
    ghost_patrol.draw(screen)
    ghost_patrol.setTarget(game_field)
    ghost_patrol.changeDirection(game_field, door, pacman)
    ghost_patrol.move(dt, screen)
    ghost_patrol.setCell(game_field)
    ghost_haunter.draw(screen)
    ghost_haunter.setTarget(pacman)
    ghost_haunter.changeDirection(game_field, door, pacman)
    ghost_haunter.move(dt, screen)
    ghost_haunter.setCell(game_field)
    if ghost.pacmanCollision(pacman):
        if game_field.getStatus() == "normal":
            if pacman.getLifes() == 0:
                game_over = True
            start_time = pygame.time.get_ticks() / 1000
            door.close()
            pacman.decrementLifes()
            ghost.reset(game_field)
            ghost_guardian.reset(game_field)
            ghost_patrol.reset(game_field)
            ghost_haunter.reset(game_field)
            pacman.reset(game_field)
        elif game_field.getStatus() == "bonused":
            ghost.killed()
    elif ghost_guardian.pacmanCollision(pacman):
        if game_field.getStatus() == "normal":
            if pacman.getLifes() == 0:
                game_over = True
            start_time = pygame.time.get_ticks() / 1000
            door.close()
            pacman.decrementLifes()
            ghost.reset(game_field)
            ghost_guardian.reset(game_field)
            ghost_patrol.reset(game_field)
            ghost_haunter.reset(game_field)
            pacman.reset(game_field)
        elif game_field.getStatus() == "bonused":
            ghost_guardian.killed()

    elif ghost_patrol.pacmanCollision(pacman):
        if game_field.getStatus() == "normal":
            if pacman.getLifes() == 0:
                game_over = True
            start_time = pygame.time.get_ticks() / 1000
            door.close()
            pacman.decrementLifes()
            ghost.reset(game_field)
            ghost_guardian.reset(game_field)
            ghost_patrol.reset(game_field)
            ghost_haunter.reset(game_field)
            pacman.reset(game_field)
        elif game_field.getStatus() == "bonused":
            ghost_patrol.killed()

    elif ghost_haunter.pacmanCollision(pacman):
        if game_field.getStatus() == "normal":
            if pacman.getLifes() == 0:
                game_over = True
            start_time = pygame.time.get_ticks() / 1000
            door.close()
            pacman.decrementLifes()
            ghost.reset(game_field)
            ghost_guardian.reset(game_field)
            ghost_patrol.reset(game_field)
            ghost_haunter.reset(game_field)
            pacman.reset(game_field)
        elif game_field.getStatus() == "bonused":
            ghost_haunter.killed()

    if food.getCords() == [] and bonus.getCords() == []:
        game_over = True

    pacman.move(dt, screen)
    pygame.display.update()

pygame.quit()