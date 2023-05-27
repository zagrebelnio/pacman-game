import pygame.time
from pacman import *
from food import *
from block import *
from ghost import *
from door import *
from button import *

def show_menu(screen):
    screen.fill()

    font = pygame.font.Font("fonts/Pixeboy-z8XGD.ttf", 128)
    title = font.render("PACMAN", True, "yellow")
    title_rect = [(screen.getWidth() - title.get_width()) // 2, 100, title.get_width(), title.get_height()]
    screen.showText(title, title_rect)

    start_button = Button("START", screen.getWidth() / 2 - 175, 250)
    start_button.draw(screen)

    statistics_button = Button("STATISTICS", screen.getWidth() / 2 - 175, 400)
    statistics_button.draw(screen)

    exit_button = Button("EXIT", screen.getWidth() / 2 - 175, 550)
    exit_button.draw(screen)
    for event in pygame.event.get():
        if start_button.checkClick(event):
            return "start"
        if statistics_button.checkClick(event):
            print("statistics button clicked")
        if exit_button.checkClick(event):
            return "exit"
        if event.type == pygame.QUIT:
            return "exit"
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            return "exit"

    pygame.display.update()

def initialize_game(game_field):
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
    return pacman, clock, food, bonus, block, ghost, ghost_guardian, ghost_patrol, ghost_haunter, door

def game_loop(game_field, screen):
    pacman, clock, food, bonus, block, ghost, ghost_guardian, ghost_patrol, ghost_haunter, door = initialize_game(game_field)
    game_over = False
    start_time = pygame.time.get_ticks() / 1000
    bonused_start = None
    game_result = None
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
        if pressed[pygame.K_LEFT]:
            if pacman.can_turn("left", game_field):
                pacman.setDirection("left")
        if pressed[pygame.K_RIGHT]:
            if pacman.can_turn("right", game_field):
                pacman.setDirection("right")
        if pressed[pygame.K_UP]:
            if pacman.can_turn("up", game_field):
                pacman.setDirection("up")
        if pressed[pygame.K_DOWN]:
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
                    game_result = False
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
                    game_result = False
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
                    game_result = False
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
                    game_result = False
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
            game_result = True

        pacman.move(dt, screen)
        pygame.display.update()

    return game_result

def win_screen(screen):
    while True:
        screen.fill()

        font = pygame.font.Font("fonts/Pixeboy-z8XGD.ttf", 128)
        title = font.render("YOU WON!", True, "yellow")
        title_rect = [(screen.getWidth() - title.get_width()) // 2, 100, title.get_width(), title.get_height()]
        screen.showText(title, title_rect)

        menu_button = Button("MENU", screen.getWidth() / 2 - 175, 550)
        menu_button.draw(screen)
        for event in pygame.event.get():
            if menu_button.checkClick(event):
                return "menu"
            if event.type == pygame.QUIT:
                return "exit"
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "exit"

        pygame.display.update()

def lose_screen(screen):
    while True:
        screen.fill()

        font = pygame.font.Font("fonts/Pixeboy-z8XGD.ttf", 128)
        title = font.render("YOU LOST!", True, "yellow")
        title_rect = [(screen.getWidth() - title.get_width()) // 2, 100, title.get_width(), title.get_height()]
        screen.showText(title, title_rect)

        menu_button = Button("MENU", screen.getWidth() / 2 - 175, 550)
        menu_button.draw(screen)
        for event in pygame.event.get():
            if menu_button.checkClick(event):
                return "menu"
            if event.type == pygame.QUIT:
                return "exit"
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "exit"

        pygame.display.update()