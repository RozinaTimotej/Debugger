import pygame

class Logo(pygame.sprite.Sprite):
    def __init__(self, x, y, settings):
        super().__init__()
        self.settings = settings
        self.image = pygame.transform.scale(pygame.image.load('./Assets/background/logo.png').convert_alpha(),(443,62))
        self.rect = self.image.get_rect(topleft=(x, y))
