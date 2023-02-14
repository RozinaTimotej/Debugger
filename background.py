import pygame


class Background1(pygame.sprite.Sprite):
    def __init__(self, x, y, settings):
        super().__init__()
        self.settings = settings
        self.image = pygame.transform.scale(pygame.image.load('./Assets/background/bg1.png').convert_alpha(),(1367, self.settings.screen_h))
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self, move):
        #self.rect.x += move
        pass


class Background2(pygame.sprite.Sprite):
    def __init__(self, x, y, settings):
        super().__init__()
        self.settings = settings
        self.image = pygame.transform.scale(pygame.image.load('./Assets/background/bg2.png').convert_alpha(),(1367, self.settings.screen_h))
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self, move):
        # self.rect.x += move
        pass
