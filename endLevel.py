import pygame
from mainMenu import Button

class DieMenu:
    def __init__(self, surface, settings):
        self.menu = None
        self.settings = settings
        self.state = "die_menu"
        self.display_surface = surface
        self.init_menu()

    def init_menu(self):
        self.menu = pygame.sprite.Group()
        self.menu.add(Button(self.settings.screen_w / 2, 150,"end", "restart", self.settings))
        self.menu.add(Button(self.settings.screen_w / 2, 250,"end", "main_menu", self.settings))
        self.menu.add(Button(self.settings.screen_w / 2, 350,"end", "exit_to_desktop", self.settings))

    def draw(self):
        self.state = "die_menu"
        self.menu.update(self)
        self.menu.draw(self.display_surface)
        if not self.state == "die_menu":
            self.settings.pause = False
        return self.state