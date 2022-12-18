import pygame

class Spike(pygame.sprite.Sprite):
    def __init__(self, pos, settings, frames):
        super().__init__()
        self.settings = settings
        self.frames = frames
        self.dir_i = "spike"
        self.frame_index = 0
        self.image = self.frames[self.dir_i][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)
        self.animMult = {"spike": 1}
        self.state = "alive"
        self.sleep1 = pygame.time.get_ticks()
        self.sleep2 = pygame.time.get_ticks()
        self.sleep3 = pygame.time.get_ticks()
        self.sleep4 = pygame.time.get_ticks()
        self.deadly = True

    def update(self, move):
        self.rect.x += move

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

        self.image = self.frames[self.dir_i][int(self.frame_index)]