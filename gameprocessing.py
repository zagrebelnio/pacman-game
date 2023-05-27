import pygame.time
from pacman import *
from food import *
from block import *
from ghost import *
from door import *
from button import *
from scorebar import *

def show_menu(screen):
    while True:
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
                return "statistics"
            if exit_button.checkClick(event):
                return "exit"
            if event.type == pygame.QUIT:
                return "exit"
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "exit"

        pygame.display.update()

def show_statistics(screen):
    scores = []
    with open("result/scores.txt", "r") as file:
        for line in file:
            score = line.strip()
            scores.append(score)
    scores.sort(key=int, reverse=True)
    while True:
        screen.fill()

        font = pygame.font.Font("fonts/Pixeboy-z8XGD.ttf", 128)
        title = font.render("STATISTICS", True, "yellow")
        title_rect = [(screen.getWidth() - title.get_width()) // 2, 30, title.get_width(), title.get_height()]
        screen.showText(title, title_rect)
        sheet_font = pygame.font.Font("fonts/Pixeboy-z8XGD.ttf", 48)
        if scores == []:
            text_lines = ["SORRY, BUT THERE", "ARE NO SCORES!"]
            y = 120
            for line in text_lines:
                line_text = sheet_font.render(line, True, "white")
                line_rect = [(screen.getWidth() - line_text.get_width()) // 2, y, line_text.get_width(),
                            line_text.get_height()]
                screen.showText(line_text, line_rect)
                y += 35
        else:
            heading = sheet_font.render("TOP SCORES", True, "white")
            heading_rect = [(screen.getWidth() - heading.get_width()) // 2, 120, heading.get_width(),
                            heading.get_height()]
            screen.showText(heading, heading_rect)
            y = 158
            length = 10
            if length > len(scores):
                length = len(scores)
            for i in range(length):
                score_text = sheet_font.render(f"{scores[i]}", True, "white")
                score_rect = [(screen.getWidth() - score_text.get_width()) // 2, y, score_text.get_width(),
                              score_text.get_height()]
                screen.showText(score_text, score_rect)
                y += 38

        menu_button = Button("MENU", screen.getWidth() / 2 - 175, 550)
        menu_button.draw(screen)
        for event in pygame.event.get():
            if menu_button.checkClick(event):
                return "menu"
            if event.type == pygame.QUIT:
                return "exit"
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "menu"

        pygame.display.update()


def initialize_game(game_field, screen):
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
    scorebar = ScoreBar(game_field, screen)
    return pacman, clock, food, bonus, block, ghost, ghost_guardian, ghost_patrol, ghost_haunter, door, scorebar

def game_loop(game_field, screen):
    pacman, clock, food, bonus, block, ghost, ghost_guardian, ghost_patrol, ghost_haunter, door, scorebar = initialize_game(game_field, screen)
    game_over = False
    start_time = pygame.time.get_ticks() / 1000
    bonused_start = None
    game_result = None
    game_start = pygame.time.get_ticks() / 1000
    while not game_over:
        if pygame.time.get_ticks() / 1000 - start_time > 5:
            door.open()
        dt = clock.tick(250)
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
        scorebar.setLifes(pacman)
        scorebar.draw(screen)
        food.draw(screen)
        if food.eat(pacman):
            scorebar.increaseScore(1)
        bonus.draw(screen)
        if bonus.eat(pacman):
            scorebar.increaseScore(10)
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
        ghost.setCell(game_field)
        ghost.setTarget(pacman)
        ghost.changeDirection(game_field, door, pacman)
        ghost.move(dt, screen)
        ghost_guardian.draw(screen)
        ghost_guardian.setCell(game_field)
        ghost_guardian.setBonusTarget(bonus)
        ghost_guardian.setTarget(bonus, game_field)
        ghost_guardian.changeDirection(game_field, door, pacman)
        ghost_guardian.move(dt, screen)
        ghost_patrol.draw(screen)
        ghost_patrol.setCell(game_field)
        ghost_patrol.setTarget(game_field)
        ghost_patrol.changeDirection(game_field, door, pacman)
        ghost_patrol.move(dt, screen)
        ghost_haunter.draw(screen)
        ghost_haunter.setCell(game_field)
        ghost_haunter.setTarget(pacman)
        ghost_haunter.changeDirection(game_field, door, pacman)
        ghost_haunter.move(dt, screen)
        if ghost.pacmanCollision(pacman):
            if game_field.getStatus() == "normal":
                if pacman.getLifes() == 1:
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
                if ghost.isAlive():
                    scorebar.increaseScore(100)
                ghost.killed()

        elif ghost_guardian.pacmanCollision(pacman):
            if game_field.getStatus() == "normal":
                if pacman.getLifes() == 1:
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
                if ghost_guardian.isAlive():
                    scorebar.increaseScore(100)
                ghost_guardian.killed()

        elif ghost_patrol.pacmanCollision(pacman):
            if game_field.getStatus() == "normal":
                if pacman.getLifes() == 1:
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
                if ghost_patrol.isAlive():
                    scorebar.increaseScore(100)
                ghost_patrol.killed()

        elif ghost_haunter.pacmanCollision(pacman):
            if game_field.getStatus() == "normal":
                if pacman.getLifes() == 1:
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
                if ghost_haunter.isAlive():
                    scorebar.increaseScore(100)
                ghost_haunter.killed()

        if food.getCords() == [] and bonus.getCords() == []:
            game_over = True
            game_result = True

        pacman.move(dt, screen)
        pygame.display.update()

    player_lifes = 0
    if game_result == True:
        player_lifes = pacman.getLifes()
    game_end = pygame.time.get_ticks() / 1000
    game_time = game_end - game_start
    return game_result, scorebar.getScore(), game_time, player_lifes

def win_screen(screen, score):
    while True:
        screen.fill()

        font = pygame.font.Font("fonts/Pixeboy-z8XGD.ttf", 128)
        title = font.render("YOU WON!", True, "yellow")
        title_rect = [(screen.getWidth() - title.get_width()) // 2, 100, title.get_width(), title.get_height()]
        screen.showText(title, title_rect)

        draw_score(screen, score)

        menu_button = Button("MENU", screen.getWidth() / 2 - 175, 550)
        menu_button.draw(screen)
        for event in pygame.event.get():
            if menu_button.checkClick(event):
                return "menu"
            if event.type == pygame.QUIT:
                return "exit"
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "menu"

        pygame.display.update()

def lose_screen(screen, score):
    while True:
        screen.fill()

        font = pygame.font.Font("fonts/Pixeboy-z8XGD.ttf", 128)
        title = font.render("YOU LOST!", True, "yellow")
        title_rect = [(screen.getWidth() - title.get_width()) // 2, 100, title.get_width(), title.get_height()]
        screen.showText(title, title_rect)

        draw_score(screen, score)

        menu_button = Button("MENU", screen.getWidth() / 2 - 175, 550)
        menu_button.draw(screen)
        for event in pygame.event.get():
            if menu_button.checkClick(event):
                return "menu"
            if event.type == pygame.QUIT:
                return "exit"
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "menu"

        pygame.display.update()

def draw_score(screen, score):
    font = pygame.font.Font("fonts/Pixeboy-z8XGD.ttf", 96)
    title = font.render("YOUR SCORE IS", True, "white")
    title_rect = [(screen.getWidth() - title.get_width()) // 2, 250, title.get_width(), title.get_height()]
    screen.showText(title, title_rect)
    result = font.render(f"{score}", True, "white")
    result_rect = [(screen.getWidth() - result.get_width()) // 2, 350, result.get_width(), result.get_height()]
    screen.showText(result, result_rect)

def calculate_total_score(score, game_time, player_lifes):
    if player_lifes == 0:
        return score
    else:
        lifes_coefs = {1: 1.5, 2: 2, 3: 3}
        time_coef = 1
        if game_time <= 480:
            time_coef = 480 / game_time
        return int(score * lifes_coefs[player_lifes] * time_coef)

def store_score(score):
    with open("result/scores.txt", 'a') as file:
        file.write(str(score) + '\n')