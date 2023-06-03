import pygame.time
from screen import *
from gamefield import *
from pacman import *
from food import *
from block import *
from ghost import *
from door import *
from button import *
from scorebar import *
from music import *
from error import *

class Menu:
    def __init__(self, screen):
        self.__font = pygame.font.Font("fonts/Pixeboy-z8XGD.ttf", 128)
        self.__game_title = self.__font.render("PACMAN", True, "yellow")
        self.__game_title_rect = [(screen.getWidth() - self.__game_title.get_width()) // 2, 100, self.__game_title.get_width(), self.__game_title.get_height()]
        self.__statistics_title = self.__font.render("STATISTICS", True, "yellow")
        self.__statistics_title_rect = [(screen.getWidth() - self.__statistics_title.get_width()) // 2, 30, self.__statistics_title.get_width(), self.__statistics_title.get_height()]
        self.__start_button = Button("START", screen.getWidth() / 2 - 175, 250)
        self.__statistics_button = Button("STATISTICS", screen.getWidth() / 2 - 175, 400)
        self.__exit_button = Button("EXIT", screen.getWidth() / 2 - 175, 550)
        self.__menu_button = Button("MENU", screen.getWidth() / 2 - 175, 550)
        self.__ok_button = Button("OK", screen.getWidth() / 2 - 175, screen.getHeight() - 150)
        self.__music = Music()
        self.__volume_images = ["images/menu/volume_on.png", "images/menu/volume_off.png"]
        self.__volume_index = 0
        self.__volume_button = ImageButton(screen.getWidth() - 100, screen.getHeight() - 100, 60, 60, self.__volume_images[self.__volume_index])
        self.__next_track_button = ImageButton(screen.getWidth() - 70, screen.getHeight() - 150, 40, 40, "images/menu/skip.png")
        self.__previous_track_button = ImageButton(screen.getWidth() - 110, screen.getHeight() - 150, 40, 40, "images/menu/skip.png", 180)
        self.__status = "menu"
        self.__music.playMenu()
        self.__score_file = FileManager()

    def getStatus(self):
        return self.__status

    def playMusic(self):
        self.__music.playMenu()

    def show_menu(self, screen):
        while True:
            screen.fill()
            screen.showText(self.__game_title, self.__game_title_rect)
            self.__start_button.draw(screen)
            self.__statistics_button.draw(screen)
            self.__exit_button.draw(screen)
            self.__volume_button.draw(screen)
            self.__next_track_button.draw(screen)
            self.__previous_track_button.draw(screen)
            screen.showImage(pygame.transform.scale(pygame.image.load("images/pacman_frames/pacman_frame_3.png"), (100, 100)), 10, 40)
            screen.showImage(pygame.transform.scale(pygame.image.load("images/ghosts_frames/red/right/1.png"), (100, 100)), 10, 200)
            screen.showImage(pygame.transform.scale(pygame.image.load("images/ghosts_frames/pink/up/pixil-frame-3.png"), (100, 100)),10, 325)
            screen.showImage(pygame.transform.scale(pygame.image.load("images/ghosts_frames/orange/left/1.png"), (100, 100)), 10, 450)
            screen.showImage(pygame.transform.scale(pygame.image.load("images/ghosts_frames/lightblue/down/pixil-frame-2.png"), (100, 100)), 10, 575)
            for event in pygame.event.get():
                if self.__start_button.checkClick(event):
                    self.__status = "start"
                    self.__music.menuStop()
                    return
                if self.__statistics_button.checkClick(event):
                    self.__status = "statistics"
                    return
                if self.__exit_button.checkClick(event):
                    self.__status = "exit"
                    return
                if self.__volume_button.checkClick(event):
                    if self.__volume_index == 0:
                        self.__music.soundOff()
                        self.__volume_index = 1
                        self.__volume_button = ImageButton(screen.getWidth() - 100, screen.getHeight() - 100, 60, 60, self.__volume_images[self.__volume_index])
                    else:
                        self.__music.sounfOn()
                        self.__volume_index = 0
                        self.__volume_button = ImageButton(screen.getWidth() - 100, screen.getHeight() - 100, 60, 60, self.__volume_images[self.__volume_index])
                if self.__next_track_button.checkClick(event):
                    self.__music.next_menu_track()
                if self.__previous_track_button.checkClick(event):
                    self.__music.previous_menu_track()
                if event.type == pygame.QUIT:
                    self.__status = "exit"
                    return
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.__status = "exit"
                    return

            pygame.display.update()

    def showStatistics(self, screen):
        scores, no_error = self.__score_file.read_score()
        if no_error is False:
            self.display_error_message(screen, scores)
            self.__status = "menu"
            return
        scores.sort(key=int, reverse=True)
        while True:
            screen.fill()
            screen.showText(self.__statistics_title, self.__statistics_title_rect)
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

            self.__menu_button.draw(screen)
            self.__volume_button.draw(screen)
            self.__next_track_button.draw(screen)
            self.__previous_track_button.draw(screen)

            for event in pygame.event.get():
                if self.__menu_button.checkClick(event):
                    self.__status = "menu"
                    return
                if self.__volume_button.checkClick(event):
                    if self.__volume_index == 0:
                        self.__music.soundOff()
                        self.__volume_index = 1
                        self.__volume_button = ImageButton(screen.getWidth() - 100, screen.getHeight() - 100, 60, 60, self.__volume_images[self.__volume_index])
                    else:
                        self.__music.sounfOn()
                        self.__volume_index = 0
                        self.__volume_button = ImageButton(screen.getWidth() - 100, screen.getHeight() - 100, 60, 60, self.__volume_images[self.__volume_index])
                if self.__next_track_button.checkClick(event):
                    self.__music.next_menu_track()
                if self.__previous_track_button.checkClick(event):
                    self.__music.previous_menu_track()
                if event.type == pygame.QUIT:
                    self.__status = "exit"
                    return
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.__status = "menu"
                    return

            pygame.display.update()

    def draw_score(self, screen, score):
        font = pygame.font.Font("fonts/Pixeboy-z8XGD.ttf", 96)
        title = font.render("YOUR SCORE IS", True, "white")
        title_rect = [(screen.getWidth() - title.get_width()) // 2, 250, title.get_width(), title.get_height()]
        screen.showText(title, title_rect)
        result = font.render(f"{score}", True, "white")
        result_rect = [(screen.getWidth() - result.get_width()) // 2, 350, result.get_width(), result.get_height()]
        screen.showText(result, result_rect)

    def win_screen(self, screen, score):
        win_sound = pygame.mixer.Sound("music/win/We-Are-The-Champions-_8-Bit-Remix-Cover-Version_-_Tribute-to-Queen_-8-Bit-Universe.mp3")
        win_sound.set_volume(0.1)
        win_sound.play(-1)
        while True:
            screen.fill()

            title = self.__font.render("YOU WON!", True, "yellow")
            title_rect = [(screen.getWidth() - title.get_width()) // 2, 100, title.get_width(), title.get_height()]
            screen.showText(title, title_rect)

            self.draw_score(screen, score)

            self.__menu_button.draw(screen)
            for event in pygame.event.get():
                if self.__menu_button.checkClick(event):
                    win_sound.stop()
                    self.__status = "menu"
                    return
                if event.type == pygame.QUIT:
                    win_sound.stop()
                    self.__status = "exit"
                    return
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    win_sound.stop()
                    self.__status = "menu"
                    return

            pygame.display.update()

    def lose_screen(self, screen, score):
        lose_sound = pygame.mixer.Sound("music/lose/Eminem-Sing-For-The-Moment-8-bit.mp3")
        lose_sound.set_volume(0.1)
        lose_sound.play(-1)
        while True:
            screen.fill()

            title = self.__font.render("YOU LOST!", True, "yellow")
            title_rect = [(screen.getWidth() - title.get_width()) // 2, 100, title.get_width(), title.get_height()]
            screen.showText(title, title_rect)

            self.draw_score(screen, score)

            self.__menu_button.draw(screen)

            for event in pygame.event.get():
                if self.__menu_button.checkClick(event):
                    lose_sound.stop()
                    self.__status = "menu"
                    return
                if event.type == pygame.QUIT:
                    lose_sound.stop()
                    self.__status = "exit"
                    return
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    lose_sound.stop()
                    self.__status = "menu"
                    return

            pygame.display.update()

    def getScore(self):
        return self.__score_file.getScore()

    def show_score(self, screen, score, game_time, player_lifes):
        self.__score_file.calculate_total_score(score, game_time, player_lifes)
        result = self.__score_file.store_score()
        if result == True:
            return result
        else:
            self.display_error_message(screen, result)

    def display_error_message(self, screen, message):
        font = pygame.font.Font("fonts/Pixeboy-z8XGD.ttf", 48)
        while True:
            screen.fill()
            top_margin = 150
            for line in message:
                error_message = font.render(line, True, "white")
                error_rect = [(screen.getWidth() - error_message.get_width()) // 2, top_margin, error_message.get_width(),
                              error_message.get_height()]
                screen.showText(error_message, error_rect)
                top_margin += 50
            self.__ok_button.draw(screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.__status = "exit"
                    return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.__ok_button.checkClick(event):
                        self.__status = "menu"
                        return
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.__status = "menu"
                    return
            pygame.display.update()

class FileManager:
    def __init__(self):
        self.__path = "result/scores.txt"
        self.__score = 0

    def getScore(self):
        return self.__score
    def read_score(self):
        scores = []
        try:
            if not os.path.exists(self.__path):
                error_message = ["Error in storing the score:", "No file 'scores.txt'", "in 'result' folder!"]
                raise Error(error_message)
            with open(self.__path, "r") as file:
                line_num = 1
                for line in file:
                    score = line.strip()
                    if score.isdigit():
                        scores.append(score)
                    else:
                        error_message = ["Error in reading scores:", "The file 'scores.txt' in the",
                                         "'result' folder must contain", "only digits!",
                                         "The wrong line in the file is:", f"{score}", f"Line number: {line_num}"]
                        raise Error(error_message)
                    line_num += 1
            return scores, True
        except Error as e:
            return e.getMessage(), False

    def calculate_total_score(self, score, game_time, player_lifes):
        if player_lifes == 0:
            self.__score = score
        else:
            lifes_coefs = {1: 1.5, 2: 2, 3: 3}
            time_coef = 1
            if game_time <= 300:
                time_coef = 300 / game_time
            self.__score = int(score * lifes_coefs[player_lifes] * time_coef)

    def store_score(self):
        try:
            if not os.path.exists(self.__path):
                error_message = ["Error in storing the score:", "No file 'scores.txt'", "in 'result' folder!"]
                raise Error(error_message)
            with open(self.__path, 'a') as file:
                file.write(str(self.__score) + '\n')
                return True
        except Error as e:
            return e.getMessage()

class Game:
    def __init__(self):
        self.__game_field = GameField()
        self.__screen = Screen(self.__game_field)
        self.__pacman = Pacman(self.__game_field)
        self.__clock = pygame.time.Clock()
        self.__food = Food(self.__game_field)
        self.__food.reset(self.__game_field)
        self.__bonus = Bonus(self.__game_field)
        self.__bonus.reset(self.__game_field)
        self.__block = Block()
        self.__block.reset(self.__game_field)

        self.__ghosts = []
        self.__ghost_types = [Ghost, GhostGuardian, GhostPatrol, GhostHaunter]
        for ghost_type in self.__ghost_types:
            ghost = ghost_type(self.__game_field)
            if isinstance(ghost, GhostPatrol):
                ghost.setPatrolAreaTarget(self.__game_field)
            self.__ghosts.append(ghost)

        self.__door = Door(self.__game_field)
        self.__scorebar = ScoreBar(self.__game_field, self.__screen)

    def getScreen(self):
        return self.__screen

    def getGameField(self):
        return self.__game_field

    def starting_screen(self):
        start_time = pygame.time.get_ticks() / 1000
        game_start_sound = pygame.mixer.Sound("sounds/game/game_start.wav")
        game_start_sound.set_volume(0.3)
        pygame.mixer.Sound.play(game_start_sound)
        clock_stop_time = pygame.time.get_ticks()
        while pygame.time.get_ticks() / 1000 - start_time < game_start_sound.get_length():
            dt = pygame.time.get_ticks() - clock_stop_time
            clock_stop_time = pygame.time.get_ticks()
            self.__screen.fill()
            self.__game_field.draw(self.__screen)
            self.__pacman.draw(self.__screen)
            self.__food.draw(self.__screen)
            self.__bonus.draw(self.__screen)
            for ghost in self.__ghosts:
                ghost.draw(self.__screen, self.__game_field)
            self.__door.draw(self.__screen)
            pygame.display.update()
            pygame.time.delay(max(0, 250 - dt))
        self.__clock.tick_busy_loop(250)

    def death_screen(self, ghost):
        start_time = pygame.time.get_ticks() / 1000
        death_sound = pygame.mixer.Sound("sounds/game/death_1.wav")
        death_sound.set_volume(0.3)
        pygame.mixer.Sound.play(death_sound)
        clock_stop_time = pygame.time.get_ticks()
        while pygame.time.get_ticks() / 1000 - start_time < death_sound.get_length():
            dt = pygame.time.get_ticks() - clock_stop_time
            clock_stop_time = pygame.time.get_ticks()
            self.__screen.fill()
            self.__pacman.draw(self.__screen)
            ghost.draw(self.__screen, self.__game_field)
            pygame.display.update()
            pygame.time.delay(max(0, 250 - dt))
        self.__clock.tick_busy_loop(250)

    def game_loop(self):
        self.reset()
        self.__game_field.setStatus("normal")
        self.starting_screen()
        game_over = False
        start_time = pygame.time.get_ticks() / 1000
        bonused_start = None
        game_result = None
        game_start = pygame.time.get_ticks() / 1000
        exit_to_menu = True
        sounds = {
            "eating": pygame.mixer.Sound("sounds/game/wakawaka (mp3cut.net).mp3"),
            "siren": pygame.mixer.Sound("sounds/game/siren_1.wav"),
            "bonus": pygame.mixer.Sound("sounds/game/power_pellet.wav"),
            "ghost_death": pygame.mixer.Sound("sounds/game/eat_ghost.wav")
        }
        for sound in sounds.values():
            sound.set_volume(0.1)
        sounds["ghost_death"].set_volume(0.3)
        while not game_over:
            sounds["siren"].play(-1)
            if pygame.time.get_ticks() / 1000 - start_time > 3:
                self.__door.open()
            dt = self.__clock.tick(250)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                    exit_to_menu = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    game_over = True
            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_LEFT]:
                if self.__pacman.can_turn("left", self.__game_field):
                    self.__pacman.setDirection("left")
            if pressed[pygame.K_RIGHT]:
                if self.__pacman.can_turn("right", self.__game_field):
                    self.__pacman.setDirection("right")
            if pressed[pygame.K_UP]:
                if self.__pacman.can_turn("up", self.__game_field):
                    self.__pacman.setDirection("up")
            if pressed[pygame.K_DOWN]:
                if self.__pacman.can_turn("down", self.__game_field):
                    self.__pacman.setDirection("down")
            self.__screen.fill()
            self.__game_field.draw(self.__screen)
            self.__door.draw(self.__screen)
            self.__scorebar.setLifes(self.__pacman)
            self.__scorebar.draw(self.__screen)
            self.__food.draw(self.__screen)
            if self.__food.eat(self.__pacman):
                self.__scorebar.increaseScore(1)
                sounds["siren"].stop()
                sounds["eating"].play(maxtime=450)
            self.__bonus.draw(self.__screen)
            if self.__bonus.eat(self.__pacman):
                self.__scorebar.increaseScore(10)
                sounds["siren"].stop()
                sounds["eating"].play(maxtime=450)
                bonused_start = pygame.time.get_ticks() / 1000
                self.__game_field.setStatus("bonused")

            if self.__game_field.getStatus() == "bonused":
                for ghost in self.__ghosts:
                    if ghost.isAlive():
                        ghost.setSpeed(0.08)

            if bonused_start != None:
                sounds["siren"].stop()
                sounds["bonus"].play()
                if pygame.time.get_ticks() / 1000 - bonused_start > 10:
                    self.__game_field.setStatus("normal")
                    for ghost in self.__ghosts:
                        if ghost.isAlive():
                            ghost.setSpeed(0.11)
                    bonused_start = None
            self.__block.check_wall_collisions(self.__pacman)
            for ghost in self.__ghosts:
                self.__block.check_wall_collisions(ghost)
            self.__pacman.draw(self.__screen)
            self.__pacman.setCell(self.__game_field)
            for ghost in self.__ghosts:
                ghost.draw(self.__screen, self.__game_field)
                ghost.setCell(self.__game_field)
                if isinstance(ghost, GhostGuardian):
                    ghost.setBonusTarget(self.__bonus)
                    ghost.setTarget(self.__bonus, self.__game_field)
                elif isinstance(ghost, GhostPatrol):
                    ghost.setTarget(self.__game_field)
                else:
                    ghost.setTarget(self.__pacman)
                ghost.changeDirection(self.__game_field, self.__door, self.__pacman)
                ghost.move(dt, self.__screen)
                if ghost.pacmanCollision(self.__pacman):
                    if self.__game_field.getStatus() == "normal":
                        sounds["siren"].stop()
                        self.death_screen(ghost)
                        if self.__pacman.getLifes() == 1:
                            game_over = True
                            game_result = False
                            break
                        start_time = pygame.time.get_ticks() / 1000
                        self.__door.close()
                        self.__pacman.decrementLifes()
                        for ghost in self.__ghosts:
                            ghost.reset(self.__game_field)
                        self.__pacman.reset(self.__game_field)
                    elif self.__game_field.getStatus() == "bonused":
                        if ghost.isAlive():
                            self.__scorebar.increaseScore(100)
                            sounds["bonus"].stop()
                            sounds["ghost_death"].play()
                        ghost.killed()

            if self.__food.getCords() == [] and self.__bonus.getCords() == []:
                game_over = True
                game_result = True

            self.__pacman.move(dt, self.__screen)
            pygame.display.update()

        player_lifes = 0
        if game_result == True:
            player_lifes = self.__pacman.getLifes()
        game_end = pygame.time.get_ticks() / 1000
        game_time = game_end - game_start
        sounds["siren"].stop()
        sounds["bonus"].stop()
        sounds["ghost_death"].stop()
        sounds["eating"].stop()
        return game_result, self.__scorebar.getScore(), game_time, player_lifes, exit_to_menu

    def reset(self):
        self.__pacman = Pacman(self.__game_field)
        self.__clock = pygame.time.Clock()
        self.__food = Food(self.__game_field)
        self.__food.reset(self.__game_field)
        self.__bonus = Bonus(self.__game_field)
        self.__bonus.reset(self.__game_field)
        self.__block = Block()
        self.__block.reset(self.__game_field)

        self.__ghosts = []
        self.__ghost_types = [Ghost, GhostGuardian, GhostPatrol, GhostHaunter]
        for ghost_type in self.__ghost_types:
            ghost = ghost_type(self.__game_field)
            if isinstance(ghost, GhostPatrol):
                ghost.setPatrolAreaTarget(self.__game_field)
            self.__ghosts.append(ghost)

        self.__door = Door(self.__game_field)
        self.__scorebar = ScoreBar(self.__game_field, self.__screen)