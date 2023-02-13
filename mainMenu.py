import pygame


class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, folder ,job, settings):
        super().__init__()
        self.job = job
        self.settings = settings
        self.x = x
        self.y = y
        self.imgNormal = pygame.image.load('./Assets/menu/'+folder+'/'+job+".png").convert_alpha()
        self.imgHover = pygame.image.load('./Assets/menu/'+folder+'/'+job+"_hover.png").convert_alpha()
        self.imageNormal = pygame.transform.scale(self.imgNormal,(self.imgNormal.get_width()*self.settings.screen_mul,self.imgNormal.get_height()*self.settings.screen_mul))
        self.imageHover = pygame.transform.scale(self.imgHover,(self.imgHover.get_width()*self.settings.screen_mul,self.imgHover.get_height()*self.settings.screen_mul))
        self.played = False

        self.image = self.imageNormal
        self.rect = self.image.get_rect(topleft=(x-self.imageHover.get_width()/2, y))

    def resize(self):
        self.imageNormal = pygame.transform.scale(self.imgNormal, (
        self.imgNormal.get_width() * self.settings.screen_mul, self.imgNormal.get_height() * self.settings.screen_mul))
        self.imageHover = pygame.transform.scale(self.imgHover, (
        self.imgHover.get_width() * self.settings.screen_mul, self.imgHover.get_height() * self.settings.screen_mul))
        self.image = self.imageNormal
        self.rect = self.image.get_rect(topleft=(self.x*self.settings.screen_mul - self.imageHover.get_width() / 2, self.y*self.settings.screen_mul))

    def update(self, el):
        mouse = pygame.mouse.get_pos()
        pressed = pygame.mouse.get_pressed()[0]
        if self.rect.collidepoint(mouse):
            if not self.played:
                pygame.mixer.Sound.play(self.settings.HoverSound)
                self.played = True
            if self.rect.collidepoint(mouse) and pressed and not self.settings.leftClick:
                self.settings.leftClick = True
                if self.job == "playing" and not el.state == "pause_menu":
                    self.settings.menuMusic.stop()
                    self.settings.gameMusic.play(-1, 0, 200)
                if self.job == "main_menu" and (el.state == "pause_menu" or el.state == "die_menu" or el.state == "finish_menu"):
                    self.settings.gameMusic.stop()
                    self.settings.menuMusic.play(-1, 0, 200)
                if el.state == "name" and ((el.valid and self.job == "main_menu") or (self.job == "exit_to_desktop")):
                    pygame.mixer.Sound.play(self.settings.ClickSound)
                elif not el.state == "name":
                    pygame.mixer.Sound.play(self.settings.ClickSound)
                el.state = self.job
                if el.state == "playing":
                    self.settings.pause = False
                if el.state == "settings":
                    el.settingsMenu.updatePrevSound()
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
        self.menu.add(Button(self.settings.screen_w / 2, 225,"main", "select", self.settings))
        self.menu.add(Button(self.settings.screen_w / 2, 275, "main", "highscoreselect", self.settings))
        self.menu.add(Button(self.settings.screen_w / 2, 325,"main", "settings", self.settings))
        self.menu.add(Button(self.settings.screen_w / 2, 375, "main", "about", self.settings))
        self.menu.add(Button(self.settings.screen_w / 2, 425, "main", "license", self.settings))
        self.menu.add(Button(self.settings.screen_w / 2, 475,"main", "exit_to_desktop", self.settings))

    def resize(self):
        for el in self.menu:
            el.resize()

    def draw(self):
        self.state = "main_menu"
        self.settings.background.draw(self.display_surface)
        self.settings.logo.draw(self.display_surface)
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
        self.menu.add(Button(self.settings.screen_w / 2, 200,"pause", "playing", self.settings))
        self.menu.add(Button(self.settings.screen_w / 2, 250, "pause", "restart", self.settings))
        self.menu.add(Button(self.settings.screen_w / 2, 300,"pause", "main_menu", self.settings))
        self.menu.add(Button(self.settings.screen_w / 2, 350,"pause", "settings", self.settings))
        self.menu.add(Button(self.settings.screen_w / 2, 400,"pause", "exit_to_desktop", self.settings))

    def resize(self):
        for el in self.menu:
            el.resize()

    def draw(self):
        self.state = "pause_menu"
        self.settings.logo.draw(self.display_surface)
        self.menu.update(self)
        self.menu.draw(self.display_surface)
        return self.state
