import os
import pygame
d = 'levels'

map = []

with open("D:\Faks\Debugger\levels\level1.txt", 'r') as f:  # nalaganje levela iz datoteke
    for line in f.readlines():
        map.append(line.strip().split(','))

tile_size = 64
screen_w = 1200
screen_h = tile_size * len(map)
music_volume = 0.1
effects_volume = 0.1


class Settings():
    def __init__(self):
        global music_volume, effects_volume, tile_size, screen_w, screen_h
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.tile_size = tile_size
        self.vol = [music_volume, effects_volume]
        pygame.mixer.init()
        self.menuMusic = pygame.mixer.Sound("./Assets/sounds/menumusic.mp3")
        pygame.mixer.Sound.set_volume(self.menuMusic, self.vol[0])
        self.menuMusic.play()
        self.gameMusic = pygame.mixer.Sound("./Assets/sounds/gameMusic.mp3")
        pygame.mixer.Sound.set_volume(self.gameMusic, self.vol[0])
