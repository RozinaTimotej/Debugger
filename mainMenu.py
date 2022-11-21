import pygame
from settings import screen_w

class StartButton(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.imageNormal = pygame.image.load('./Assets/menu/start.png').convert_alpha()
        self.imageHover = pygame.image.load('./Assets/menu/start_hover.png').convert_alpha()
        self.image = self.imageNormal
        self.rect = self.image.get_rect(topleft=(x, y))
        self.HoverSound = pygame.mixer.Sound("./Assets/sounds/hover.wav")
        self.ClickSound = pygame.mixer.Sound("./Assets/sounds/test.wav")
        pygame.mixer.Sound.set_volume(self.HoverSound, 0.1)
        pygame.mixer.Sound.set_volume(self.ClickSound, 0.1)
        self.played = False

    def update(self, el):
        mouse = pygame.mouse.get_pos()
        pressed = pygame.mouse.get_pressed()[0]
        if self.rect.collidepoint(mouse):
            if not self.played:
                pygame.mixer.Sound.play(self.HoverSound)
                self.played = True
            if self.rect.collidepoint(mouse) and pressed:
                el.state = "playing"
                pygame.mixer.Sound.play(self.ClickSound)
            self.image = self.imageHover

        else:
            self.played = False
            self.image = self.imageNormal


class MainMenu:
    def __init__(self, surface):
        self.menu = None
        self.state = "main_menu"
        self.display_surface = surface
        self.init_menu()

    def init_menu(self):
        self.menu = pygame.sprite.Group()
        self.menu.add(StartButton(screen_w/2-30, 100))

    def draw(self):
        self.menu.update(self)
        self.menu.draw(self.display_surface)
        return self.state