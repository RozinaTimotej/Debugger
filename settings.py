import os
import pygame

d = 'levels'


def sound(path, volume):  # nalaganje vseh *.png datotek
    arr = []
    for filename in os.listdir(path):
        if not filename.endswith('.ogg'):
            continue
        x = pygame.mixer.Sound(path + filename)
        pygame.mixer.Sound.set_volume(x, volume)
        arr.append(x)
    return arr


def tiles(path):  # nalaganje vseh *.png datotek
    arr = {}
    for filename in os.listdir(path):
        if not filename.endswith('.png'):
            continue
        id = filename.split(".")[0].split("_")[1]
        arr[id]=pygame.image.load(path+filename).convert_alpha()
    return arr

map = []
for filename in os.listdir("./levels"):
    arr = []
    if not filename.endswith('.txt'):
        continue
    with open("./levels/" + filename, 'r') as f:  # nalaganje levela iz datoteke
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
        pygame.mixer.init()
        global music_volume, effects_volume, tile_size, screen_w, screen_h
        self.levelIndex = 0
        self.levels = map
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.tile_size = tile_size
        self.vol = [music_volume, effects_volume]
        self.playerJump = pygame.mixer.Sound("./Assets/sounds/jump_02.wav")
        self.menuMusic = pygame.mixer.Sound("./Assets/sounds/menumusic.mp3")
        self.gameMusic = pygame.mixer.Sound("./Assets/sounds/gameMusic.mp3")
        self.hitEnemy = pygame.mixer.Sound("./Assets/sounds/hit_enemy.wav")
        self.HoverSound = pygame.mixer.Sound("./Assets/sounds/hover.wav")
        self.ClickSound = pygame.mixer.Sound("./Assets/sounds/test.wav")
        self.playerWalk = sound("./Assets/sounds/walk/", self.vol[1])
        self.tile = tiles("./Assets/tla/")
        self.updateSound()
        self.menuMusic.play(-1, 0, 2000)

    def updateSound(self):
        pygame.mixer.Sound.set_volume(self.playerJump, self.vol[1])
        pygame.mixer.Sound.set_volume(self.menuMusic, self.vol[0])
        pygame.mixer.Sound.set_volume(self.gameMusic, self.vol[0])
        pygame.mixer.Sound.set_volume(self.hitEnemy, self.vol[1])
        pygame.mixer.Sound.set_volume(self.HoverSound, self.vol[1])
        pygame.mixer.Sound.set_volume(self.ClickSound, self.vol[1])
