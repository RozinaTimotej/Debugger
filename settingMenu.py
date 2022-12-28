import copy

import pygame
from mainMenu import Button

class Slider(pygame.sprite.Sprite):

    def __init__(self, x, y,folder, id):
        super().__init__()
        self.id = id
        self.w = 300
        self.start = x - self.w / 2
        self.image = pygame.image.load('./Assets/menu/' + folder + '/slider_' +  str(id) + ".png").convert_alpha()
        self.rect = self.image.get_rect(topleft=(x - self.w / 2, y))

    def update(self, el):
        mouse = pygame.mouse.get_pos()
        pressed = pygame.mouse.get_pressed()[0]
        if self.rect.collidepoint(mouse) and pressed:
            el.settings.vol[self.id] = (mouse[0] - self.start) / self.w


class SliderMovable(pygame.sprite.Sprite):
    def __init__(self, x, y, id, settings, folder):
        super().__init__()
        self.id = id
        self.settings = settings
        self.y = y
        self.w = 275
        self.start = x - self.w / 2
        self.end = self.start + self.w
        img_size = (50, 50)
        self.imageNormal = pygame.transform.scale(pygame.image.load('./Assets/menu/' + folder + "/tile.png").convert_alpha(), img_size)
        self.imageHover = pygame.transform.scale(pygame.image.load('./Assets/menu/' + folder + "/tile_hover.png").convert_alpha(), img_size)
        self.image = self.imageNormal
        self.rect = self.image.get_rect(center=(self.start + (self.settings.vol[id] * self.w), y+20))

    def update(self, el):
        self.settings.updateSound()
        self.rect.x = self.start + (el.settings.vol[self.id] * self.w) - 20



class SettingsMenu:
    def __init__(self, surface, settings):
        self.groupSound = None
        self.settings = settings
        self.prevSound = copy.deepcopy(settings.vol)
        self.state = "settings"
        self.prevState = settings.state
        self.display_surface = surface
        self.init_menu()

    def init_menu(self):
        self.groupSound = pygame.sprite.Group()
        self.groupSound.add(Slider(self.settings.screen_w / 2, 100, "settings",0))
        self.groupSound.add(SliderMovable(self.settings.screen_w / 2, 100, 0, self.settings, "settings"))
        self.groupSound.add(Slider(self.settings.screen_w / 2, 200, "settings", 1))
        self.groupSound.add(SliderMovable(self.settings.screen_w / 2, 200, 1, self.settings, "settings"))
        self.groupSound.add(Button(self.settings.screen_w / 2+150, 500,"settings", "main_menu", self.settings))
        self.groupSound.add(Button(self.settings.screen_w / 2-150, 500,"settings", "back", self.settings))

    def updateState(self, state):
        self.prevState = state

    def updatePrevSound(self):
        self.prevSound = copy.deepcopy(self.settings.vol)

    def draw(self):
        self.state = "settings"
        if not self.settings.pause:
            self.settings.background.draw(self.display_surface)
        self.groupSound.update(self)
        self.groupSound.draw(self.display_surface)
        if self.state == "back":
            self.state = "main_menu"
            self.settings.vol = self.prevSound
            self.settings.updateSound()
            return self.prevState
        elif self.state == "main_menu":
            return self.prevState
        else:
            return self.state

