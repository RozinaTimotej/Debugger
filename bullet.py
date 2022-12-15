import pygame
import os
from math import atan2,pi,degrees,sqrt




class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, settings, frames, facingRight):
        super().__init__()
        self.settings = settings
        self.frames = frames
        self.dir_i = "fly"
        self.frame_index = 0
        self.image = self.frames[self.dir_i][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)
        self.facing_right = facingRight
        self.speed = 2
        self.speedInfo = self.speed
        self.animMult = {"fly": 6,"die":30}
        self.state = "alive"
    def death(self):
        self.frame_index = 0
        self.dir_i = "die"
        self.state = "dying"

    def updateDest(self,dest):
        self.destination = dest
        dx = self.rect.x - self.destination[0]
        dy = self.rect.y - self.destination[1]
        rads = atan2(-dy, dx)
        rads %= 2 * pi
        self.degs = degrees(rads)


    def update(self, move):
        self.frame_index += 0.02 * self.animMult[self.dir_i]
        if self.frame_index >= len(self.frames[self.dir_i]):
            self.frame_index = 0
        if self.state == "dying" and self.frame_index + 0.02 * self.animMult[self.dir_i] >= len(self.frames[self.dir_i]):
            self.state = "dead"
        if self.facing_right:
            self.image = pygame.transform.rotate(self.frames[self.dir_i][int(self.frame_index)],self.degs)
        else:
            self.image = pygame.transform.rotate(pygame.transform.flip(self.frames[self.dir_i][int(self.frame_index)], True, False),self.degs)