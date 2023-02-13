import pygame


class Background1(pygame.sprite.Sprite):
    def __init__(self, x, y, settings):
        super().__init__()
        self.settings = settings
        self.img = pygame.transform.scale(pygame.image.load('./Assets/background/bg1.png').convert_alpha(),(1367, self.settings.screen_w))
        self.image = pygame.transform.scale(self.img, (self.img.get_width() * self.settings.screen_mul, self.img.get_height() * self.settings.screen_mul))
        self.rect = self.image.get_rect(topleft=(x*self.settings.screen_mul, y*self.settings.screen_mul))

    def update(self, move):
        self.rect.x += move


class Background2(pygame.sprite.Sprite):
    def __init__(self, x, y, settings):
        super().__init__()
        self.settings = settings
        self.img = pygame.transform.scale(pygame.image.load('./Assets/background/bg2.png').convert_alpha(),(1367, self.settings.screen_w))
        self.image = pygame.transform.scale(self.img, (self.img.get_width() * self.settings.screen_mul, self.img.get_height() * self.settings.screen_mul))
        self.rect = self.image.get_rect(topleft=(x*self.settings.screen_mul, y*self.settings.screen_mul))

    def update(self, move):
        if move != 0:
            self.rect.x += move / 2
