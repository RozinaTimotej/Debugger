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
        self.menu.add(Button(self.settings.screen_w / 2, 200, "finish", "next_level", self.settings))
        self.menu.add(Button(self.settings.screen_w / 2, 250,"finish", "restart", self.settings))
        self.menu.add(Button(self.settings.screen_w / 2, 300,"finish", "main_menu", self.settings))
        self.menu.add(Button(self.settings.screen_w / 2, 350,"finish", "exit_to_desktop", self.settings))

    def resize(self):
        for el in self.menu:
            el.resize()

    def draw(self):
        if not self.settings.wrote:
            if self.settings.name in self.settings.scores[self.settings.levelIndex].keys():
                if self.settings.score < float(self.settings.scores[self.settings.levelIndex][self.settings.name]):
                    print("Vecji score: ",self.settings.score, self.settings.scores[self.settings.levelIndex][self.settings.name])
                    self.settings.scores[self.settings.levelIndex][self.settings.name] = self.settings.score
                    self.settings.writeScore()
            else:
                self.settings.scores[self.settings.levelIndex][self.settings.name] = self.settings.score
                self.settings.writeScore()
            print("Writing complete")
            self.settings.wrote = True
        self.state = "finish_menu"
        self.menu.update(self)
        self.settings.logo.draw(self.display_surface)
        self.menu.draw(self.display_surface)
        if not self.state == "finish_menu":
            self.settings.wrote = False
            self.settings.pause = False
        return self.state