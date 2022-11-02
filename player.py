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
    def __init__(self,pos):
        super().__init__()
        self.frames = {"front":[],"run":[],"jump":[],"fall":[]}
        self.frames["front"] = import_folder("../Assets/player/front/game/")
        self.frames["run"] = import_folder("../Assets/player/side/right/game/")
        self.dir_i = "front"
        self.frame_index = 0
        self.image = self.frames[self.dir_i][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)

        #movm
        self.facing_right = True
        self.direction = pygame.math.Vector2(0.0)
        self.speed = 3
        self.speedInfo = 3
        self.animMult = {"front":1,"run":3,"jump":3,"fall":3}
        self.gravity = 1
        self.jumpHeight = -10

    def animate(self):
        self.frame_index += 0.02*self.animMult[self.dir_i]
        if self.frame_index >= len(self.frames[self.dir_i]):
            self.frame_index = 0
        if self.facing_right:
            self.image = self.frames[self.dir_i][int(self.frame_index)]
        else:
            self.image = pygame.transform.flip(self.frames[self.dir_i][int(self.frame_index)],True,False)

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.dir_i = "run"
            self.facing_right = True
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.dir_i ="run"
            self.facing_right = False
        else:
            self.direction.x = 0
            self.dir_i = "front"

        if keys[pygame.K_UP]:
            self.direction.y = self.jumpHeight

    def set_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y


    def update(self):
        self.input()
        self.animate()



