import pygame
from math import sqrt,atan2,degrees,pi





class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, settings, frames):
        super().__init__()
        self.settings = settings
        self.frames = frames
        self.dir_i = "run"
        self.frame_index = 0
        self.image = self.frames[self.dir_i][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)
        self.facing_right = False
        self.speed = 1
        self.speedInfo = self.speed
        self.animMult = {"front": 6, "run": 6, "jump": 6, "fall": 6, "holdWall": 6}
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
        self.speed = 1
        self.speedInfo = self.speed
        self.animMult = {"fly": 6,"die":10,"shoot":10}
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
        self.speed = 2
        self.speedInfo = self.speed
        self.animMult = {"fly": 6,"die":10,"ready":6,"attack":6,"stand":6}
        self.dest = pygame.math.Vector2(0.0)
        self.state = "alive"

    def death(self):
        self.frame_index = 0

    def shoot(self):
        self.dest.x = self.rect.x
        self.dest.y = self.rect.y - 200
        self.state = "flying"
        self.dir_i = "fly"

    def kamikaze(self,x,y):
        self.dest.x = x
        self.dest.y = y
        self.frame_index = 0
        self.state = "attack"
        self.dir_i = "attack"
        self.speed *= 3

    def update(self, move):
        self.rect.x += move
        if not self.state == "dead":
            dx = self.dest.x - self.rect.x
            dy = self.dest.y - self.rect.y
            dist = (dx ** 2 + dy ** 2) ** .5
            if not dist == 0:
                dx /= dist
                dy /= dist

            self.rect.x += self.speed * dx
            self.rect.y += self.speed * dy

            rads = atan2(-dy, dx)
            rads %= 2 * pi
            degs = degrees(rads)
            if dx == 0 and dy == 0 and self.state == "flying":
                self.state = "ready"
                self.dir_i = "ready"
                self.frame_index = 0

            if dist < 5 and self.state == "attack":
                self.state = "dead"
                self.dir_i = "die"

            if not (self.state == "attack" and int(self.frame_index) == 2):
                self.frame_index += 0.02 * self.animMult[self.dir_i]

            if self.frame_index >= len(self.frames[self.dir_i]):
                self.frame_index = 0
                if self.state == "ready":
                    self.state = "locate_enemy"
                    self.dir_i = "fly"

        if self.state == "attack":
            self.image = pygame.transform.rotate(self.frames[self.dir_i][int(self.frame_index)], degs)
        else:
            self.image = pygame.transform.flip(self.frames[self.dir_i][int(self.frame_index)], self.facing_right, False)