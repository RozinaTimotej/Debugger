import pygame
import random
class Spike(pygame.sprite.Sprite):
    def __init__(self, pos, settings, frames,degs):
        super().__init__()
        self.settings = settings
        self.frames = frames
        self.degs = degs
        self.dir_i = "spike"
        self.frame_index = 0
        self.image = pygame.transform.rotate(self.frames[self.dir_i][self.frame_index],self.degs)
        self.rect = self.image.get_rect(topleft=pos)
        self.animMult = {"spike": 1 + (random.randrange(6,16)/10)}
        self.state = "alive"
        self.delayStart = pygame.time.get_ticks() + random.randrange(0,1500)
        self.active = False
        self.started = False
        self.sleep1 = pygame.time.get_ticks()
        self.sleep2 = pygame.time.get_ticks()
        self.sleep3 = pygame.time.get_ticks()
        self.sleep4 = pygame.time.get_ticks()
        self.deadly = True

    def update(self, move):
        self.rect.x += move
        if not self.started:
            self.delayStart = pygame.time.get_ticks() + random.randrange(250, 1500)
            self.started = True
        if pygame.time.get_ticks() > self.delayStart:
            self.active = True
        if self.active:
            if int(self.frame_index) == 2:
                self.deadly = False
            else:
                self.deadly = True

            if abs(pygame.time.get_ticks() - self.sleep1) > 1500 and int(self.frame_index) == 2:
                self.sleep4 = pygame.time.get_ticks()
                self.frame_index += 0.02 * self.animMult[self.dir_i]

            if abs(pygame.time.get_ticks() - self.sleep2) > 100 and int(self.frame_index) == 1:
                self.sleep1 = pygame.time.get_ticks()
                self.frame_index += 0.02 * self.animMult[self.dir_i]

            if abs(pygame.time.get_ticks() - self.sleep3) > 500 and int(self.frame_index) == 0:
                self.sleep2 = pygame.time.get_ticks()
                self.frame_index += 0.02 * self.animMult[self.dir_i]

            if abs(pygame.time.get_ticks() - self.sleep4) > 100 and int(self.frame_index) == 3:
                self.sleep3 = pygame.time.get_ticks()
                self.frame_index += 0.02 * self.animMult[self.dir_i]

            if self.frame_index >= len(self.frames[self.dir_i]):
                self.frame_index = 0

        self.image = pygame.transform.rotate(self.frames[self.dir_i][int(self.frame_index)],self.degs)