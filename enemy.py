import pygame
from math import ceil,atan2,degrees,pi





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
        self.speed = 1*self.settings.screen_mul
        self.speedInfo = self.speed
        self.animMult = {"front": 6*self.settings.screen_mul, "run": 6*self.settings.screen_mul, "jump": 6*self.settings.screen_mul, "fall": 6*self.settings.screen_mul, "holdWall": 6*self.settings.screen_mul}
        self.state = "alive"
        self.direction = pygame.math.Vector2(0.0)
        self.direction.x = 1


    def death(self):
        self.state = "dead"

    def update(self, move):
        self.rect.x += move

        self.frame_index += 0.02 * self.animMult[self.dir_i]
        if self.frame_index >= len(self.frames[self.dir_i]):
            self.frame_index = 0

        if self.facing_right:
            self.image = self.frames[self.dir_i][int(self.frame_index)]
        else:
            self.image = pygame.transform.flip(self.frames[self.dir_i][int(self.frame_index)], True, False)

class FlyingEnemy(pygame.sprite.Sprite):
    def __init__(self, pos, settings, frames):
        super().__init__()
        self.settings = settings
        self.frames = frames
        self.dir_i = "fly"
        self.frame_index = 0
        self.image = self.frames[self.dir_i][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)
        self.facing_right = True
        self.speed = 1*self.settings.screen_mul
        self.speedInfo = self.speed
        self.animMult = {"fly": 6*self.settings.screen_mul,"die":10*self.settings.screen_mul,"shoot":10*self.settings.screen_mul}
        self.direction = pygame.math.Vector2(0.0)
        self.direction.x = 1
        self.state = "alive"

    def death(self):
        self.frame_index = 0
        self.dir_i = "die"
        self.state = "dying"

    def shoot(self):
        self.frame_index = 0
        self.dir_i = "shoot"
    def update(self, move):
        self.rect.x += move
        self.frame_index += 0.02 * self.animMult[self.dir_i]
        if self.frame_index >= len(self.frames[self.dir_i]):
            self.frame_index = 0
            if self.dir_i == "shoot":
                self.dir_i = "fly"
        if self.state == "dying" and self.frame_index + 0.02 * self.animMult[self.dir_i] >= len(self.frames[self.dir_i]):
            self.state = "dead"

        if self.facing_right:
            self.image = self.frames[self.dir_i][int(self.frame_index)]
        else:
            self.image = pygame.transform.flip(self.frames[self.dir_i][int(self.frame_index)], True, False)

class KamikazeEnemy(pygame.sprite.Sprite):
    def __init__(self, pos, settings, frames):
        super().__init__()
        self.settings = settings
        self.frames = frames
        self.dir_i = "stand"
        self.frame_index = 0
        self.image = self.frames[self.dir_i][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)
        self.facing_right = False
        self.speed = 3*self.settings.screen_mul
        self.speedInfo = self.speed
        self.animMult = {"fly": 6*self.settings.screen_mul,"die":10*self.settings.screen_mul,"ready":6*self.settings.screen_mul,"attack":6*self.settings.screen_mul,"stand":6*self.settings.screen_mul}
        self.dest = pygame.math.Vector2(0.0)
        self.state = "alive"
        self.dx = 0
        self.dy = 0
        self.degs = 0
        self.dist = 0

    def death(self,state):
        self.frame_index = 0
        self.tod = pygame.time.get_ticks()
        self.rect.x -= self.speed * self.dx
        self.dx = 0
        self.dy = 0
        self.degs = 0
        self.dist = 0
        self.speed = 3*self.settings.screen_mul
        self.state = state
        self.dir_i = "die"

    def shoot(self):
        self.dest.x = self.rect.x
        self.dest.y = self.rect.y - 100
        dx = self.dest.x - self.rect.x
        dy = self.dest.y - self.rect.y
        if dx > 0:
            self.facing_right = True
        else:
            self.facing_right = False
        self.dist = (dx ** 2 + dy ** 2) ** .5
        if not self.dist == 0:
            self.dx = dx/self.dist
            self.dy = dy/self.dist

        self.state = "flying"
        self.dir_i = "fly"

    def kamikaze(self,x,y):
        self.dest.x = x
        self.dest.y = y
        dx = self.dest.x - self.rect.x
        dy = self.dest.y - self.rect.y
        self.dist = (dx ** 2 + dy ** 2) ** .5
        if not self.dist == 0:
            self.dx = dx / self.dist
            self.dy = dy / self.dist
        rads = atan2(-dy, dx)
        rads %= 2 * pi
        self.degs = degrees(rads)-190
        self.frame_index = 0
        self.state = "attack"
        self.dir_i = "attack"
        self.speed *= 5

    def h_move(self):
        self.rect.x += self.speed * self.dx

    def v_move(self):
        self.rect.y += self.speed * self.dy
    def update(self, move):
        self.rect.x += move
        if not self.state == "dead" and not self.state == "alive" and not self.state == "super_dead":


            dx = self.dest.x - self.rect.x
            dy = self.dest.y - self.rect.y
            self.dist = (dx ** 2 + dy ** 2) ** .5

            if (self.dist < 10 or self.dist > 150) and self.state == "flying":
                self.dx = 0
                self.dy = 0
                self.state = "ready"
                self.dir_i = "ready"
                self.frame_index = 0

            if self.dist > 1500 and self.state == "attack":
                self.state = "remove"
                self.dir_i = "die"

            if not (self.state == "attack" and int(self.frame_index) == 2):
                self.frame_index += 0.02 * self.animMult[self.dir_i]

            if self.frame_index >= len(self.frames[self.dir_i]):
                self.frame_index = 0
                if self.state == "ready":
                    self.state = "locate_enemy"
                    self.dir_i = "fly"

        if self.state == "attack":
            self.image = pygame.transform.rotate(self.frames[self.dir_i][int(self.frame_index)], self.degs)
        else:
            self.image = pygame.transform.flip(self.frames[self.dir_i][int(self.frame_index)], self.facing_right, False)