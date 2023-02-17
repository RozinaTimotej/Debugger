import pygame

class Logo(pygame.sprite.Sprite):
    def __init__(self, settings):
        super().__init__()
        self.settings = settings
        self.surf =  pygame.transform.scale(pygame.image.load('./Assets/background/logo.png').convert_alpha(),(443*self.settings.screen_mul,62*self.settings.screen_mul))
        self.image = self.surf
        self.rect = self.image.get_rect(topleft=(self.settings.screen_w/2 - self.image.get_width()/2, self.settings.screen_w/4 - self.image.get_width()/2))

    def resize(self):
        self.image = pygame.transform.scale(self.surf, ( self.surf.get_width() * self.settings.screen_mul, self.surf.get_height() * self.settings.screen_mul))
        self.rect = self.image.get_rect(topleft=(self.settings.screen_w / 2 - self.image.get_width() / 2, self.settings.screen_w / 4 - self.image.get_width() / 2))
