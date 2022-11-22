import pygame
from settings import screen_h


class Background1(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load('./Assets/background/bg1.png').convert_alpha(), (1367, screen_h))
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self, move):
        self.rect.x += move

class Background2(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load('./Assets/background/bg2.png').convert_alpha(), (1367, screen_h))
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self, move):
        if move != 0:
            self.rect.x += move/2
