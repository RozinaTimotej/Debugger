import pygame
import os
from math import atan2,pi,degrees,sqrt




class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, settings, frames, facingRight, startTicks):
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
        self.animMult = {"fly": 6,"die":20}
        self.state = "alive"
        self.startTicks = startTicks
        self.degs = 0
    def death(self):
        self.frame_index = 0
        self.dir_i = "die"
        self.state = "dying"
        self.rect.x -= self.rect.height/2 + 15
        self.rect.y -= self.rect.width/2 + 15

    def updateDest(self,destx,desty):
        dx = self.rect.x - destx
        dy = self.rect.y - desty
        rads = atan2(-dy, dx)
        rads %= 2 * pi
        self.degs = degrees(rads)


    def update(self, move):
        if pygame.time.get_ticks() - self.startTicks > 1500 and self.state == "alive":
            self.death()
        if self.state == "dying":
            self.degs = 0
        self.frame_index += 0.02 * self.animMult[self.dir_i]
        if self.frame_index >= len(self.frames[self.dir_i]):
            self.frame_index = 0
        if self.state == "dying" and self.frame_index + 0.02 * self.animMult[self.dir_i] >= len(self.frames[self.dir_i]):
            self.state = "dead"
        if self.facing_right:
            self.image = pygame.transform.rotate(self.frames[self.dir_i][int(self.frame_index)],self.degs)
        else:
            self.image = pygame.transform.rotate(pygame.transform.flip(self.frames[self.dir_i][int(self.frame_index)], True, False),self.degs)