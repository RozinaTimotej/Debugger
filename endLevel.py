import pygame
from mainMenu import Button, CurrHighScore

class DieMenu:
    def __init__(self, surface, settings):
        self.menu = None
        self.settings = settings
        self.state = "die_menu"
        self.display_surface = surface
        self.init_menu()

    def init_menu(self):
        self.menu = pygame.sprite.Group()
        self.hs = pygame.sprite.GroupSingle()
        self.menu.add(Button(self.settings.screen_w / 2,0, 200,"end", "restart", self.settings))
        self.menu.add(Button(self.settings.screen_w / 2,0, 250,"end", "main_menu", self.settings))
        self.menu.add(Button(self.settings.screen_w / 2,0, 300,"end", "exit_to_desktop", self.settings))
        self.hs.add(CurrHighScore(self.settings.screen_w / 2, 350, self.settings))

    def resize(self):
        for el in self.menu:
            el.resize()
        self.hs.sprite.resize()

    def draw(self):
        self.state = "die_menu"
        self.menu.update(self)
        self.settings.logo.draw(self.display_surface)
        self.hs.update(self)
        self.hs.draw(self.display_surface)
        self.menu.draw(self.display_surface)
        if not self.state == "die_menu":
            self.settings.pause = False
        return self.state