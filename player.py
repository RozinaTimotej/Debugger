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
        self.settings = settings
        self.image = self.frames[self.dir_i][self.frame_index]
        self.image = pygame.transform.scale(self.image, (self.image.get_width() * self.settings.screen_mul, self.image.get_height() * self.settings.screen_mul))
        self.rect = self.image.get_rect(topleft=pos)
        self.soundDelay = 0
        self.s_index = 0
        self.keys = {"left":False,"right":False,"up":False, "down": False}
        # premikanje igralca
        self.on_wall = False
        self.wall_jumped = True
        self.facing_right = True
        self.canJump = False
        self.jumps = 0
        self.doubleJump = False
        self.direction = pygame.math.Vector2(0.0)
        self.speed = 4*self.settings.screen_mul
        self.speedInfo = self.speed
        self.animMult = {"front": 6*self.settings.screen_mul, "run": 6, "jump": 6, "fall": 6,"holdWall":  6}
        self.gravity = 1*self.settings.screen_mul
        self.jumpHeight = -17*self.settings.screen_mul

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
            self.image = pygame.transform.scale(self.image, (self.image.get_width() * self.settings.screen_mul, self.image.get_height() * self.settings.screen_mul))
        else:
            self.image = pygame.transform.flip(self.frames[self.dir_i][int(self.frame_index)], True, False)
            self.image = pygame.transform.scale(self.image, (self.image.get_width() * self.settings.screen_mul, self.image.get_height() * self.settings.screen_mul))

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

    def detectKeys(self):
        for event in self.settings.event:
            if event.type == pygame.KEYDOWN:
                if self.settings.buttons["up"] == pygame.key.name(event.key):
                    self.keys["up"] = True
                elif self.settings.buttons["down"] == pygame.key.name(event.key):
                    self.keys["down"] = True
                elif self.settings.buttons["left"] == pygame.key.name(event.key):
                    self.keys["left"] = True
                elif self.settings.buttons["right"] == pygame.key.name(event.key):
                    self.keys["right"] = True
            else:
                if event.type == pygame.KEYUP:
                    if self.settings.buttons["up"] == pygame.key.name(event.key):
                        self.keys["up"] = False
                    elif self.settings.buttons["down"] == pygame.key.name(event.key):
                        self.keys["down"] = False
                    elif self.settings.buttons["left"] == pygame.key.name(event.key):
                        self.keys["left"] = False
                    elif self.settings.buttons["right"] == pygame.key.name(event.key):
                        self.keys["right"] = False
    def input(self):
        self.detectKeys()

        if not self.keys["up"]:
            self.canJump = True
        if self.keys["right"]:
            if self.soundDelay == -1:
                self.soundDelay = 0
            self.direction.x = 1
        elif self.keys["left"]:
            if self.soundDelay == -1:
                self.soundDelay = 0
            self.direction.x = -1
        else:
            self.soundDelay = -1
            self.direction.x = 0
        if self.keys["up"] and self.on_wall and not self.wall_jumped:
            self.jumpFromWall()
            pygame.mixer.Sound.play(self.settings.playerJump)

        if self.keys["up"] and self.canJump and self.jumps < 2 and not self.on_wall: #ce je na steni, mora biti do naslednjega skoka vsaj 1/4 sekunde, skoči lahko samo 2x
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
