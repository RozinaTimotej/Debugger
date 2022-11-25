import pygame
import os





class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, settings, frames):
        super().__init__()
        self.settings = settings
        self.frames = frames
        self.dir_i = "run"
        self.frame_index = 0
        self.image = self.frames[self.dir_i][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)
        self.facing_right = True
        self.speed = 1
        self.speedInfo = self.speed
        self.animMult = {"front": 6, "run": 6, "jump": 6, "fall": 6, "holdWall": 6}
        self.direction = pygame.math.Vector2(0.0)
        self.direction.x = 1

    def update(self, move):
        self.rect.x += move

        self.frame_index += 0.02 * self.animMult[self.dir_i]
        if self.frame_index >= len(self.frames[self.dir_i]):
            self.frame_index = 0

        if self.facing_right:
            self.image = self.frames[self.dir_i][int(self.frame_index)]
        else:
            self.image = pygame.transform.flip(self.frames[self.dir_i][int(self.frame_index)], True, False)
