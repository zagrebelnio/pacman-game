import os
import pygame

class Music:
    def __init__(self):
        self.__menu = []
        self.__menu_path = "music/menu"
        for filename in os.listdir(self.__menu_path):
            path = self.__menu_path + os.sep + filename
            self.__menu.append(path)
        self.__menu_music_index = 0
        pygame.mixer.music.set_volume(0.1)

    def playMenu(self):
        pygame.mixer.music.load(self.__menu[self.__menu_music_index])
        pygame.mixer.music.play(-1)

    def next_menu_track(self):
        if self.__menu_music_index + 1 == len(self.__menu):
            self.__menu_music_index = 0
        else:
            self.__menu_music_index += 1
        self.playMenu()

    def previous_menu_track(self):
        if self.__menu_music_index == 0:
            self.__menu_music_index = len(self.__menu) - 1
        else:
            self.__menu_music_index -= 1
        self.playMenu()

    def soundOff(self):
        pygame.mixer.music.set_volume(0)

    def sounfOn(self):
        pygame.mixer.music.set_volume(0.1)

    def menuStop(self):
        pygame.mixer.music.stop()