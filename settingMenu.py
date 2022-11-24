import pygame


class Slider(pygame.sprite.Sprite):

    def __init__(self, x, y, id):
        super().__init__()
        self.id = id
        self.w = 300
        self.start = x - self.w / 2
        self.image = pygame.Surface((self.w, 10))
        self.image.fill("Red")
        self.rect = self.image.get_rect(topleft=(x - self.w / 2, y))

    def update(self, el):
        mouse = pygame.mouse.get_pos()
        pressed = pygame.mouse.get_pressed()[0]
        if self.rect.collidepoint(mouse) and pressed:
            el.settings.vol[self.id] = (mouse[0] - self.start) / self.w


class SliderMovable(pygame.sprite.Sprite):
    def __init__(self, x, y, id, volume):
        super().__init__()
        self.id = id
        self.y = y
        self.w = 300
        self.start = x - self.w / 2
        self.end = self.start + self.w
        self.image = pygame.Surface((25, 25))
        self.image.fill("blue")
        self.rect = self.image.get_rect(topleft=(self.start + (volume * self.w) - 12, y - 10))

    def update(self, el):
        self.rect.x = self.start + (el.settings.vol[self.id] * self.w) - 12


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

    def update(self, el):
        pygame.mixer.Sound.set_volume(self.HoverSound, self.settings.vol[1])
        pygame.mixer.Sound.set_volume(self.ClickSound, self.settings.vol[1])
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


class SettingsMenu:
    def __init__(self, surface, settings):
        self.groupSound = None
        self.settings = settings
        self.state = "settings"
        self.display_surface = surface
        self.init_menu()

    def init_menu(self):
        self.groupSound = pygame.sprite.Group()
        self.groupSound.add(Slider(self.settings.screen_w / 2, 100, 0))
        self.groupSound.add(SliderMovable(self.settings.screen_w / 2, 100, 0, self.settings.vol[0]))
        self.groupSound.add(Slider(self.settings.screen_w / 2, 200, 1))
        self.groupSound.add(SliderMovable(self.settings.screen_w / 2, 200, 1, self.settings.vol[1]))
        self.groupSound.add(Button(self.settings.screen_w / 2 - 30, 500, "main_menu", self.settings))

    def draw(self):
        self.display_surface.fill("black")
        self.groupSound.update(self)
        self.groupSound.draw(self.display_surface)
        return self.state
