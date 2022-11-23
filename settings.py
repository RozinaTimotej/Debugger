import os
import pygame
d = 'levels'

map = []
for filename in os.listdir("./levels"):
    arr = []
    if not filename.endswith('.txt'):
        continue
    with open("./levels/"+filename, 'r') as f:  # nalaganje levela iz datoteke
        for line in f.readlines():
            arr.append(line.strip().split(','))
    map.append(arr)

tile_size = 64
screen_w = 1200
screen_h = tile_size * len(map[0])
music_volume = 0.1
effects_volume = 0.1


class Settings():
    def __init__(self):
        global music_volume, effects_volume, tile_size, screen_w, screen_h
        self.levelIndex = 0
        self.levels = map
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.tile_size = tile_size
        self.vol = [music_volume, effects_volume]
        pygame.mixer.init()
        self.menuMusic = pygame.mixer.Sound("./Assets/sounds/menumusic.mp3")
        pygame.mixer.Sound.set_volume(self.menuMusic, self.vol[0])
        self.menuMusic.play(-1,0,2000)
        self.gameMusic = pygame.mixer.Sound("./Assets/sounds/gameMusic.mp3")
        pygame.mixer.Sound.set_volume(self.gameMusic, self.vol[0])
