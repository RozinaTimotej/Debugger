import pygame


class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, folder ,job, settings):
        super().__init__()
        self.job = job
        self.settings = settings
        self.imageNormal = pygame.image.load('./Assets/menu/'+folder+'/'+job+".png").convert_alpha()
        self.imageHover = pygame.image.load('./Assets/menu/'+folder+'/'+job+"_hover.png").convert_alpha()
        self.played = False

        self.image = self.imageNormal
        self.rect = self.image.get_rect(topleft=(x-self.imageHover.get_width()/2, y))

    def update(self, el):
        mouse = pygame.mouse.get_pos()
        pressed = pygame.mouse.get_pressed()[0]
        if self.rect.collidepoint(mouse):
            if not self.played:
                pygame.mixer.Sound.play(self.settings.HoverSound)
                self.played = True
            if self.rect.collidepoint(mouse) and pressed:
                if self.job == "playing" and not el.state == "pause_menu":
                    self.settings.menuMusic.stop()
                    self.settings.gameMusic.play(-1, 0, 2000)
                if self.job == "main_menu" and (el.state == "pause_menu" or el.state == "die_menu"):
                    self.settings.gameMusic.stop()
                    self.settings.menuMusic.play(-1, 0, 2000)
                el.state = self.job
                if el.state == "playing":
                    self.settings.pause = False
                if el.state == "settings":
                    el.settingsMenu.updatePrevSound()
                pygame.mixer.Sound.play(self.settings.ClickSound)
            self.image = self.imageHover

        else:
            self.played = False
            self.image = self.imageNormal


class MainMenu:
    def __init__(self, surface, settings, settingsMenu):
        self.menu = None
        self.settings = settings
        self.state = "main_menu"
        self.settingsMenu = settingsMenu
        self.display_surface = surface
        self.init_menu()

    def init_menu(self):
        self.menu = pygame.sprite.Group()
        self.menu.add(Button(self.settings.screen_w / 2, 100,"main", "select", self.settings))
        self.menu.add(Button(self.settings.screen_w / 2, 200,"main", "settings", self.settings))
        self.menu.add(Button(self.settings.screen_w / 2, 300,"main", "exit_to_desktop", self.settings))

    def draw(self):
        self.state = "main_menu"
        self.display_surface.fill("black")
        self.menu.update(self)
        self.menu.draw(self.display_surface)
        return self.state

class PauseMenu:
    def __init__(self, surface, settings, settingsMenu):
        self.menu = None
        self.settings = settings
        self.state = "pause_menu"
        self.settingsMenu = settingsMenu
        self.display_surface = surface
        self.init_menu()

    def init_menu(self):
        self.menu = pygame.sprite.Group()
        self.menu.add(Button(self.settings.screen_w / 2, 100,"pause", "playing", self.settings))
        self.menu.add(Button(self.settings.screen_w / 2, 200,"pause", "main_menu", self.settings))
        self.menu.add(Button(self.settings.screen_w / 2, 300,"pause", "settings", self.settings))
        self.menu.add(Button(self.settings.screen_w / 2, 400,"pause", "exit_to_desktop", self.settings))

    def draw(self):
        self.state = "pause_menu"
        self.menu.update(self)
        self.menu.draw(self.display_surface)
        return self.state
