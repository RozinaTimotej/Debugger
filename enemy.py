import pygame
import os


def import_folder(path):  # nalaganje vseh *.png datotek
    arr = []
    for filename in os.listdir(path):
        if not filename.endswith('.png'):
            continue
        arr.append(pygame.transform.scale(pygame.image.load(path + filename).convert_alpha(), (64, 64)))
    return arr


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.frames = {"run": import_folder("./Assets/enemy/run/game/")}
        self.dir_i = "run"
        self.frame_index = 0
        self.image = self.frames[self.dir_i][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)
        self.facing_right = True
        self.speed = 1
        self.speedInfo = self.speed
        self.animMult = {"front": 6, "run": 6, "jump": 6, "fall": 6, "holdWall": 6}
        self.direction = pygame.math.Vector2(0.0)
        self.direction.x = -1

    def update(self, move):
        self.rect.x += move

        self.frame_index += 0.02 * self.animMult[self.dir_i]
        if self.frame_index >= len(self.frames[self.dir_i]):
            self.frame_index = 0

        if self.facing_right:
            self.image = self.frames[self.dir_i][int(self.frame_index)]
        else:
            self.image = pygame.transform.flip(self.frames[self.dir_i][int(self.frame_index)], True, False)
