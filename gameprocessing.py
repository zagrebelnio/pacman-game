import pygame.time
from pacman import *
from food import *
from block import *
from ghost import *
from door import *
from button import *
from scorebar import *
from music import *
from error import *

def show_menu(screen, music, volume_index):
    volume_images = ["images/menu/volume_on.png", "images/menu/volume_off.png"]
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

        volume_button = ImageButton(screen.getWidth() - 100, screen.getHeight() - 100, 60, 60, volume_images[volume_index])
        volume_button.draw(screen)

        next_track_button = ImageButton(screen.getWidth() - 70, screen.getHeight() - 150, 40, 40, "images/menu/skip.png")
        next_track_button.draw(screen)

        previous_track_button = ImageButton(screen.getWidth() - 110, screen.getHeight() - 150, 40, 40, "images/menu/skip.png", 180)
        previous_track_button.draw(screen)

        screen.showImage(pygame.transform.scale(pygame.image.load("images/pacman_frames/pacman_frame_3.png"), (100, 100)), 10, 40)
        screen.showImage(pygame.transform.scale(pygame.image.load("images/ghosts_frames/red/right/1.png"), (100, 100)), 10, 200)
        screen.showImage(pygame.transform.scale(pygame.image.load("images/ghosts_frames/pink/up/pixil-frame-3.png"), (100, 100)),10, 325)
        screen.showImage(pygame.transform.scale(pygame.image.load("images/ghosts_frames/orange/left/1.png"), (100, 100)), 10, 450)
        screen.showImage(pygame.transform.scale(pygame.image.load("images/ghosts_frames/lightblue/down/pixil-frame-2.png"), (100, 100)), 10, 575)

        for event in pygame.event.get():
            if start_button.checkClick(event):
                return "start", volume_index
            if statistics_button.checkClick(event):
                return "statistics", volume_index
            if exit_button.checkClick(event):
                return "exit", volume_index
            if volume_button.checkClick(event):
                if volume_index == 0:
                    music.soundOff()
                    volume_index = 1
                else:
                    music.sounfOn()
                    volume_index = 0
            if next_track_button.checkClick(event):
                music.next_menu_track()
            if previous_track_button.checkClick(event):
                music.previous_menu_track()
            if event.type == pygame.QUIT:
                return "exit", volume_index
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "exit", volume_index

        pygame.display.update()

def read_score(file_path, screen):
    scores = []
    try:
        if not os.path.exists(file_path):
            error_message = ["Error in storing the score:", "No file 'scores.txt'", "in 'result' folder!"]
            raise Error(error_message)
        with open(file_path, "r") as file:
            line_num = 1
            for line in file:
                score = line.strip()
                if score.isdigit():
                    scores.append(score)
                else:
                    error_message = ["Error in reading scores:", "The file 'scores.txt' in the", "'result' folder must contain", "only digits!", "The wrong line in the file is:", f"{score}", f"Line number: {line_num}"]
                    raise Error(error_message)
                line_num += 1
        return scores
    except Error as e:
        return display_error_message(screen, e.getMessage())

def show_statistics(screen, music, volume_index):
    volume_images = ["images/menu/volume_on.png", "images/menu/volume_off.png"]
    scores = read_score("result/scores.txt", screen)
    if type(scores) is str:
        return scores, volume_index
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

        volume_button = ImageButton(screen.getWidth() - 100, screen.getHeight() - 100, 60, 60,volume_images[volume_index])
        volume_button.draw(screen)

        next_track_button = ImageButton(screen.getWidth() - 70, screen.getHeight() - 150, 40, 40, "images/menu/skip.png")
        next_track_button.draw(screen)

        previous_track_button = ImageButton(screen.getWidth() - 110, screen.getHeight() - 150, 40, 40, "images/menu/skip.png", 180)
        previous_track_button.draw(screen)

        for event in pygame.event.get():
            if menu_button.checkClick(event):
                return "menu", volume_index
            if volume_button.checkClick(event):
                if volume_index == 0:
                    music.soundOff()
                    volume_index = 1
                else:
                    music.sounfOn()
                    volume_index = 0
            if next_track_button.checkClick(event):
                music.next_menu_track()
            if previous_track_button.checkClick(event):
                music.previous_menu_track()
            if event.type == pygame.QUIT:
                return "exit", volume_index
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "menu", volume_index

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

def starting_screen(screen, game_field, pacman, food, bonus, ghost, ghost_guardian, ghost_patrol, ghost_haunter, door, clock):
    start_time = pygame.time.get_ticks() / 1000
    game_start_sound = pygame.mixer.Sound("sounds/game/game_start.wav")
    game_start_sound.set_volume(0.3)
    pygame.mixer.Sound.play(game_start_sound)
    clock_stop_time = pygame.time.get_ticks()
    while pygame.time.get_ticks() / 1000 - start_time < game_start_sound.get_length():
        dt = pygame.time.get_ticks() - clock_stop_time
        clock_stop_time = pygame.time.get_ticks()
        screen.fill()
        game_field.draw(screen)
        pacman.draw(screen)
        food.draw(screen)
        bonus.draw(screen)
        ghost.draw(screen, game_field)
        ghost_guardian.draw(screen, game_field)
        ghost_patrol.draw(screen, game_field)
        ghost_haunter.draw(screen, game_field)
        door.draw(screen)
        pygame.display.update()
        pygame.time.delay(max(0, 250 - dt))
    clock.tick_busy_loop(250)

def death_screen(screen, game_field, pacman, ghost, clock):
    start_time = pygame.time.get_ticks() / 1000
    death_sound = pygame.mixer.Sound("sounds/game/death_1.wav")
    death_sound.set_volume(0.3)
    pygame.mixer.Sound.play(death_sound)
    clock_stop_time = pygame.time.get_ticks()
    while pygame.time.get_ticks() / 1000 - start_time < death_sound.get_length():
        dt = pygame.time.get_ticks() - clock_stop_time
        clock_stop_time = pygame.time.get_ticks()
        screen.fill()
        pacman.draw(screen)
        ghost.draw(screen, game_field)
        pygame.display.update()
        pygame.time.delay(max(0, 250 - dt))
    clock.tick_busy_loop(250)

def game_loop(game_field, screen):
    pacman, clock, food, bonus, block, ghost, ghost_guardian, ghost_patrol, ghost_haunter, door, scorebar = initialize_game(game_field, screen)
    game_field.setStatus("normal")
    starting_screen(screen, game_field, pacman, food, bonus, ghost, ghost_guardian, ghost_patrol, ghost_haunter, door, clock)
    game_over = False
    start_time = pygame.time.get_ticks() / 1000
    bonused_start = None
    game_result = None
    game_start = pygame.time.get_ticks() / 1000
    exit_to_menu = True
    eating_sound = pygame.mixer.Sound("sounds/game/wakawaka (mp3cut.net).mp3")
    eating_sound.set_volume(0.1)
    siren_sound = pygame.mixer.Sound("sounds/game/siren_1.wav")
    siren_sound.set_volume(0.1)
    bonus_sound = pygame.mixer.Sound("sounds/game/power_pellet.wav")
    bonus_sound.set_volume(0.1)
    ghost_death_sound = pygame.mixer.Sound("sounds/game/eat_ghost.wav")
    ghost_death_sound.set_volume(0.3)
    while not game_over:
        siren_sound.play(-1)
        if pygame.time.get_ticks() / 1000 - start_time > 3:
            door.open()
        dt = clock.tick(250)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
                exit_to_menu = False
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
        scorebar.setLifes(pacman)
        scorebar.draw(screen)
        food.draw(screen)
        if food.eat(pacman):
            scorebar.increaseScore(1)
            siren_sound.stop()
            eating_sound.play(maxtime=450)
        bonus.draw(screen)
        if bonus.eat(pacman):
            scorebar.increaseScore(10)
            siren_sound.stop()
            eating_sound.play(maxtime=450)
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
            siren_sound.stop()
            bonus_sound.play()
            if pygame.time.get_ticks() / 1000 - bonused_start > 10:
                game_field.setStatus("normal")
                if ghost.isAlive():
                    ghost.setSpeed(0.11)
                if ghost_patrol.isAlive():
                    ghost_patrol.setSpeed(0.11)
                if ghost_guardian.isAlive():
                    ghost_guardian.setSpeed(0.11)
                if ghost_haunter.isAlive():
                    ghost_haunter.setSpeed(0.11)
                bonused_start = None
        block.check_wall_collisions(pacman)
        block.check_wall_collisions(ghost)
        block.check_wall_collisions(ghost_guardian)
        block.check_wall_collisions(ghost_patrol)
        block.check_wall_collisions(ghost_haunter)
        pacman.draw(screen)
        pacman.setCell(game_field)
        ghost.draw(screen, game_field)
        ghost.setCell(game_field)
        ghost.setTarget(pacman)
        ghost.changeDirection(game_field, door, pacman)
        ghost.move(dt, screen)
        ghost_guardian.draw(screen, game_field)
        ghost_guardian.setCell(game_field)
        ghost_guardian.setBonusTarget(bonus)
        ghost_guardian.setTarget(bonus, game_field)
        ghost_guardian.changeDirection(game_field, door, pacman)
        ghost_guardian.move(dt, screen)
        ghost_patrol.draw(screen, game_field)
        ghost_patrol.setCell(game_field)
        ghost_patrol.setTarget(game_field)
        ghost_patrol.changeDirection(game_field, door, pacman)
        ghost_patrol.move(dt, screen)
        ghost_haunter.draw(screen, game_field)
        ghost_haunter.setCell(game_field)
        ghost_haunter.setTarget(pacman)
        ghost_haunter.changeDirection(game_field, door, pacman)
        ghost_haunter.move(dt, screen)
        if ghost.pacmanCollision(pacman):
            if game_field.getStatus() == "normal":
                siren_sound.stop()
                death_screen(screen, game_field, pacman, ghost, clock)
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
                    bonus_sound.stop()
                    ghost_death_sound.play()
                ghost.killed()

        elif ghost_guardian.pacmanCollision(pacman):
            if game_field.getStatus() == "normal":
                siren_sound.stop()
                death_screen(screen, game_field, pacman, ghost_guardian, clock)
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
                    bonus_sound.stop()
                    ghost_death_sound.play()
                ghost_guardian.killed()

        elif ghost_patrol.pacmanCollision(pacman):
            if game_field.getStatus() == "normal":
                siren_sound.stop()
                death_screen(screen, game_field, pacman, ghost_patrol, clock)
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
                    bonus_sound.stop()
                    ghost_death_sound.play()
                ghost_patrol.killed()

        elif ghost_haunter.pacmanCollision(pacman):
            if game_field.getStatus() == "normal":
                siren_sound.stop()
                death_screen(screen, game_field, pacman, ghost_haunter, clock)
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
                    bonus_sound.stop()
                    ghost_death_sound.play()
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
    siren_sound.stop()
    bonus_sound.stop()
    ghost_death_sound.stop()
    eating_sound.stop()
    return game_result, scorebar.getScore(), game_time, player_lifes, exit_to_menu

def win_screen(screen, score):
    win_sound = pygame.mixer.Sound("music/win/We-Are-The-Champions-_8-Bit-Remix-Cover-Version_-_Tribute-to-Queen_-8-Bit-Universe.mp3")
    win_sound.set_volume(0.1)
    win_sound.play(-1)
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
                win_sound.stop()
                return "menu"
            if event.type == pygame.QUIT:
                win_sound.stop()
                return "exit"
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                win_sound.stop()
                return "menu"

        pygame.display.update()

def lose_screen(screen, score):
    lose_sound = pygame.mixer.Sound("music/lose/Eminem-Sing-For-The-Moment-8-bit.mp3")
    lose_sound.set_volume(0.1)
    lose_sound.play(-1)
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
                lose_sound.stop()
                return "menu"
            if event.type == pygame.QUIT:
                lose_sound.stop()
                return "exit"
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                lose_sound.stop()
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

def store_score(screen, score):
    score_file = "result/scores.txt"
    try:
        if not os.path.exists(score_file):
            error_message = ["Error in storing the score:", "No file 'scores.txt'", "in 'result' folder!"]
            raise Error(error_message)
        with open(score_file, 'a') as file:
            file.write(str(score) + '\n')
            return True
    except Error as e:
        return display_error_message(screen, e.getMessage())

def display_error_message(screen, message):
    font = pygame.font.Font("fonts/Pixeboy-z8XGD.ttf", 48)
    ok_button = Button("OK", screen.getWidth() / 2 - 175, screen.getHeight() - 150)

    while True:
        screen.fill()
        top_margin = 150
        for line in message:
            error_message = font.render(line, True, "white")
            error_rect = [(screen.getWidth() - error_message.get_width()) // 2, top_margin, error_message.get_width(), error_message.get_height()]
            screen.showText(error_message, error_rect)
            top_margin += 50
        ok_button.draw(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if ok_button.checkClick(event):
                    return "menu"
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "menu"
        pygame.display.update()