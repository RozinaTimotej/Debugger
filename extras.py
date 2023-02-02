import os
import pygame
from settingMenu import Button

class About:
    def __init__(self, surface, settings):
        self.buttons = None
        self.settings = settings
        self.state = "about"
        self.y = 0
        self.display_surface = surface
        self.init_menu()

    def init_menu(self):
        self.groupButtons = pygame.sprite.Group()
        self.groupButtons.add(Button(self.settings.screen_w / 2 - 25, 500, "settings", "main_menu", self.settings))

    def draw(self):
        self.state = "about"
        self.settings.background.draw(self.display_surface)
        self.settings.logo.draw(self.display_surface)
        self.groupButtons.update(self)
        self.groupButtons.draw(self.display_surface)
        if self.state == "main_menu":
            self.settings.updateReadAbout()
        return self.state
