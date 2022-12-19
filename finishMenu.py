import pygame
from mainMenu import Button

class FinishMenu:
    def __init__(self, surface, settings):
        self.menu = None
        self.settings = settings
        self.state = "finish_menu"
        self.display_surface = surface
        self.init_menu()

    def init_menu(self):
        self.menu = pygame.sprite.Group()
        self.menu.add(Button(self.settings.screen_w / 2, 150, "finish", "next_level", self.settings))
        self.menu.add(Button(self.settings.screen_w / 2, 250,"finish", "restart", self.settings))
        self.menu.add(Button(self.settings.screen_w / 2, 350,"finish", "main_menu", self.settings))
        self.menu.add(Button(self.settings.screen_w / 2, 450,"finish", "exit_to_desktop", self.settings))

    def draw(self):
        self.state = "finish_menu"
        self.menu.update(self)
        self.menu.draw(self.display_surface)
        if not self.state == "finish_menu":
            self.settings.pause = False
        return self.state