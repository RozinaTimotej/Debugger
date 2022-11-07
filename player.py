import pygame
import os


def import_folder(path): #nalaganje vseh *.png datotek
    arr = []
    for filename in os.listdir(path):
        if not filename.endswith('.png'):
            continue
        arr.append(pygame.transform.scale(pygame.image.load(path + filename).convert_alpha(), (44, 55)))
    return arr


class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.frames = {"front": import_folder("../Assets/player/idle/game/"),
                       "run": import_folder("../Assets/player/run/game/"),
                       "jump": import_folder("../Assets/player/jump/game/"),
                       "holdWall": import_folder("../Assets/player/hold/game/")}
        self.dir_i = "front"
        self.frame_index = 0
        self.image = self.frames[self.dir_i][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)

        # premikanje igralca
        self.on_wall = False
        self.wall_jumped = True
        self.facing_right = True
        self.jumpTime = 0
        self.jumps = 0
        self.doubleJump = False
        self.direction = pygame.math.Vector2(0.0)
        self.speed = 5
        self.speedInfo = self.speed
        self.animMult = {"front": 6, "run": 6, "jump": 6, "fall": 6,"holdWall":6}
        self.gravity = 1
        self.jumpHeight = -17

    def animate(self): #pregled stanja igralca in določitev ustrezne animacije
        if self.direction.x > 0:
            self.facing_right = True
        if self.direction.x < 0:
            self.facing_right = False

        if self.on_wall:
            self.dir_i = "holdWall"
        elif self.direction.y > 4*self.gravity/2:
            self.dir_i = "jump"
            self.frame_index = 3
        elif self.jumps > 0:
            self.dir_i = "jump"
        else:
            if self.direction.x != 0:
                self.dir_i = "run"
            if self.direction.x == 0:
                self.dir_i = "front"

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
        self.jumps += 1
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

        if keys[pygame.K_UP] and self.jumpTime > 15 and self.jumps < 2 and not self.on_wall: #ce je na steni, mora biti do naslednjega skoka vsaj 1/4 sekunde, skoči lahko samo 2x
            self.dir_i = "jump"
            self.frame_index = 0
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
