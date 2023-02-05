import os
import pygame
from settingMenu import Button
from lvlSelect import Block

class Text(pygame.sprite.Sprite):
    def __init__(self, x, y, settings, txt):
        super().__init__()
        self.settings = settings
        self.image = txt
        self.rect = self.image.get_rect(topleft=(x, y))
    def update(self,el):
        self.rect.y += el.y

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
        self.ui = pygame.sprite.Group()
        self.text = pygame.sprite.Group()
        self.groupButtons.add(Button(self.settings.screen_w / 2 - 25, 650, "settings", "main_menu", self.settings))
        self.ui.add(Block(0, 0, self.settings.screen_w, self.settings.screen_h / 5, self.settings))
        self.text.add(Text(90, 275, self.settings, self.settings.about))  # 255,255,0

    def draw(self):
        self.state = "about"
        self.settings.background.draw(self.display_surface)
        self.groupButtons.update(self)
        self.text.draw(self.display_surface)
        self.ui.draw(self.display_surface)
        self.settings.logo.draw(self.display_surface)
        self.groupButtons.draw(self.display_surface)
        if self.state == "main_menu":
            self.settings.updateReadAbout()
        return self.state

class License:
    def __init__(self, surface, settings):
        self.buttons = None
        self.settings = settings
        self.state = "license"
        self.y = 0
        self.display_surface = surface
        self.init_menu()

    def init_menu(self):
        self.groupButtons = pygame.sprite.Group()
        self.ui = pygame.sprite.Group()
        self.text = pygame.sprite.Group()
        self.groupButtons.add(Button(self.settings.screen_w / 2 - 25, 650, "main", "main_menu", self.settings))
        self.ui.add(Block(0, 0, self.settings.screen_w, self.settings.screen_h / 5, self.settings))
        self.text.add(Text(90, 189, self.settings, self.settings.license)) #255,255,0

    def draw(self):
        self.state = "license"
        if self.y > 0:
            self.y -= 1
        elif self.y < 0:
            self.y += 1
        scroll_lckup = False
        scroll_lckdown = False
        if self.text.sprites()[-1].rect.bottom < (4 * self.settings.screen_h / 5) - 100:
            scroll_lckup = True
            if self.y < 0:
                self.y = 0
        if self.text.sprites()[0].rect.top > (self.settings.screen_h / 5) + 35:
            scroll_lckdown = True
            if self.y > 0:
                self.y = 0
        for event in self.settings.event:
            if event.type == pygame.MOUSEWHEEL:
                if event.y > 0 and not scroll_lckdown:
                    self.y += event.y * 2
                elif event.y < 0 and not scroll_lckup:
                    self.y += event.y * 2
        self.text.update(self)
        self.settings.background.draw(self.display_surface)
        self.groupButtons.update(self)
        self.text.draw(self.display_surface)
        self.ui.draw(self.display_surface)
        self.settings.logo.draw(self.display_surface)
        self.groupButtons.draw(self.display_surface)
        return self.state
