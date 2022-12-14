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
    def __init__(self, pos, settings,frames):
        super().__init__()
        self.frames = frames
        self.dir_i = "front"
        self.frame_index = 0
        self.image = self.frames[self.dir_i][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)
        self.settings = settings
        self.soundDelay = 0
        self.s_index = 0

        # premikanje igralca
        self.on_wall = False
        self.wall_jumped = True
        self.facing_right = True
        self.canJump = False
        self.jumps = 0
        self.doubleJump = False
        self.direction = pygame.math.Vector2(0.0)
        self.speed = 4
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

        if self.direction.y == 0 and not self.direction.x == 0 and self.soundDelay % 30 == 0:
            pygame.mixer.Sound.play(self.settings.playerWalk[self.s_index])
            self.s_index += 1
            if self.s_index > 1:
                self.s_index = 0
        if self.soundDelay != -1:
            self.soundDelay += 1
    def jumpFromWall(self):
        if self.facing_right:
            self.direction.x = -1
        else:
            self.direction.x = 1
        self.direction.y = self.jumpHeight
        self.rect.x += self.direction.x * self.speed
        self.jumps += 1
        self.wall_jumped = True
        self.on_wall = False
        self.canJump = False
    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] == False:
            self.canJump = True
        if keys[pygame.K_RIGHT]:
            if self.soundDelay == -1:
                self.soundDelay = 0
            self.direction.x = 1
        elif keys[pygame.K_LEFT]:
            if self.soundDelay == -1:
                self.soundDelay = 0
            self.direction.x = -1
        else:
            self.soundDelay = -1
            self.direction.x = 0
        if keys[pygame.K_UP] and self.on_wall and not self.wall_jumped:
            self.jumpFromWall()
            pygame.mixer.Sound.play(self.settings.playerJump)

        if keys[pygame.K_UP] and self.canJump == True and self.jumps < 2 and not self.on_wall: #ce je na steni, mora biti do naslednjega skoka vsaj 1/4 sekunde, skoči lahko samo 2x
            self.frame_index = 0
            pygame.mixer.Sound.play(self.settings.playerJump)
            if self.jumps == 0:
                self.direction.y = self.jumpHeight
                self.jumps += 1
            elif self.jumps == 1:
                self.direction.y = 0
                self.direction.y = 8 * self.jumpHeight / 9
                self.jumps += 1
            self.canJump = False

    def set_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def update(self):
        self.input()
        self.animate()
