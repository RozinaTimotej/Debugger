import pygame
from settings import screen_w


class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, job, settings):
        super().__init__()
        self.job = job
        self.settings = settings
        self.imageNormal = pygame.image.load('./Assets/menu/start.png').convert_alpha()
        self.imageHover = pygame.image.load('./Assets/menu/start_hover.png').convert_alpha()
        self.image = self.imageNormal
        self.rect = self.image.get_rect(topleft=(x, y))
        self.HoverSound = pygame.mixer.Sound("./Assets/sounds/hover.wav")
        self.ClickSound = pygame.mixer.Sound("./Assets/sounds/test.wav")
        pygame.mixer.Sound.set_volume(self.HoverSound, self.settings.vol[1])
        pygame.mixer.Sound.set_volume(self.ClickSound, self.settings.vol[1])
        self.played = False

    def updateSound(self):
        pygame.mixer.Sound.set_volume(self.HoverSound, self.settings.vol[1])
        pygame.mixer.Sound.set_volume(self.ClickSound, self.settings.vol[1])
    def update(self, el):
        self.updateSound()
        mouse = pygame.mouse.get_pos()
        pressed = pygame.mouse.get_pressed()[0]
        if self.rect.collidepoint(mouse):
            if not self.played:
                pygame.mixer.Sound.play(self.HoverSound)
                self.played = True
            if self.rect.collidepoint(mouse) and pressed:
                el.state = self.job
                pygame.mixer.Sound.play(self.ClickSound)
            self.image = self.imageHover

        else:
            self.played = False
            self.image = self.imageNormal


class MainMenu:
    def __init__(self, surface,settings):
        self.menu = None
        self.settings = settings
        self.state = "main_menu"
        self.display_surface = surface
        self.init_menu()

    def init_menu(self):
        self.menu = pygame.sprite.Group()
        self.menu.add(Button(screen_w / 2 - 30, 100, "playing",self.settings))
        self.menu.add(Button(screen_w / 2 - 30, 200, "settings",self.settings))
        self.menu.add(Button(screen_w / 2 - 30, 300, "exit_to_desktop",self.settings))

    def draw(self):
        self.display_surface.fill("black")
        self.menu.update(self)
        self.menu.draw(self.display_surface)
        return self.state
