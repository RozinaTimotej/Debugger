import pygame
import os

def import_folder(path):
    arr = [[],[],[]]

    for filename in os.listdir("../Assets/player/front/game/"):
        if not filename.endswith('.png'):
            continue
        arr[1].append(pygame.image.load("../Assets/player/front/game/" + filename).convert_alpha())

    for filename in os.listdir("../Assets/player/side/left/game/"):
        if not filename.endswith('.png'):
            continue
        arr[0].append(pygame.image.load("../Assets/player/side/left/game/" + filename).convert_alpha())

    for filename in os.listdir("../Assets/player/side/right/game/"):
        if not filename.endswith('.png'):
            continue
        arr[2].append(pygame.image.load("../Assets/player/side/right/game/" + filename).convert_alpha())

    return arr

class Player(pygame.sprite.Sprite):
    def __init__(self,pos):
        super().__init__()
        self.frames = import_folder("../Assets/player/front/game/")
        self.dir_i = 1
        self.frame_index = 0
        self.image = self.frames[self.dir_i][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)
        self.direction = 0

    def animate(self):
        self.frame_index += 0.15
        if self.frame_index >= len(self.frames[self.dir_i]):
            self.frame_index = 0
        self.image = self.frames[self.dir_i][int(self.frame_index)]

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.direction = 1
            self.dir_i = 2
        elif keys[pygame.K_LEFT]:
            self.direction = -1
            self.dir_i = 0
        else:
            self.direction = 0
            self.dir_i = 1

    def update(self):
        self.input()
        self.animate()
        self.rect.x += self.direction



