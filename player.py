import pygame
import os


def import_folder(path):
    arr = []
    for filename in os.listdir(path):
        if not filename.endswith('.png'):
            continue
        arr.append(pygame.image.load(path + filename).convert_alpha())
    return arr


class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.frames = {"front": import_folder("../Assets/player/front/game/"),
                       "run": import_folder("../Assets/player/side/right/game/"),
                       "jump": [],
                       "fall": import_folder("../Assets/player/front/game/"),
                       "holdWall": []}
        self.dir_i = "front"
        self.frame_index = 0
        self.image = self.frames[self.dir_i][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)

        # movm
        self.on_wall = False
        self.wall_jumped = True
        self.facing_right = True
        self.jumpTime = 0
        self.jumps = 0
        self.doubleJump = False
        self.direction = pygame.math.Vector2(0.0)
        self.speed = 5
        self.speedInfo = self.speed
        self.animMult = {"front": 1, "run": 5, "jump": 3, "fall": 3}
        self.gravity = 1
        self.jumpHeight = -17

    def animate(self):
        if self.direction.x > 0:
            self.dir_i = "run"
            self.facing_right = True
        if self.direction.x < 0:
            self.dir_i = "run"
            self.facing_right = False
        if self.direction.x == 0:
            self.dir_i = "front"
        if self.direction.y > self.gravity:
            self.dir_i = "fall"

        self.frame_index += 0.02 * self.animMult[self.dir_i]
        if self.frame_index >= len(self.frames[self.dir_i]):
            self.frame_index = 0
        if self.facing_right:
            self.image = self.frames[self.dir_i][int(self.frame_index)]
        else:
            self.image = pygame.transform.flip(self.frames[self.dir_i][int(self.frame_index)], True, False)


    def jumpFromWall(self):
        if self.facing_right:
            self.direction.x = -1
        else:
            self.direction.x = 1
        self.direction.y += self.jumpHeight
        self.rect.x += self.direction.x * self.speed
        self.jumps = 2
        self.wall_jumped = True
        self.on_wall = False
        self.jumpTime = 0
    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
        else:
            self.direction.x = 0

        if keys[pygame.K_UP] and self.on_wall and not self.wall_jumped:
            self.jumpFromWall()

        if keys[pygame.K_UP] and self.jumpTime > 15 and self.jumps < 2 and not self.on_wall:
            if self.jumps == 0:
                self.direction.y += self.jumpHeight
                self.jumps += 1
            elif self.jumps == 1:
                self.direction.y = 0
                self.direction.y += 3 * self.jumpHeight / 4
                self.jumps += 1
            self.jumpTime = 0

        self.jumpTime += 1

    def set_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def update(self):
        self.input()
        self.animate()
