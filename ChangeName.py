import copy

import pygame

from settingMenu import Button
validChars = "`1234567890-=qwertyuiop[]\\asdfghjkl;'zxcvbnm,./"
shiftChars = '~!@#$%^&*()_+QWERTYUIOP{}|ASDFGHJKL:"ZXCVBNM<>?'
class Input(pygame.sprite.Sprite):
    def __init__(self, x, y, id):
        super().__init__()
        self.id = id
        self.w = 300
        self.h = 30
        self.typing = False
        self.start = x - self.w / 2
        self.y = y
        self.image = pygame.Surface((self.w, self.h))
        self.image.fill((30, 30, 30))
        self.rect = self.image.get_rect(topleft=(x - self.w / 2, y))

    def update(self, el):
        mouse = pygame.mouse.get_pos()
        pressed = pygame.mouse.get_pressed()[0]
        if self.rect.collidepoint(mouse) and pressed:
            self.typing = True
            self.image.fill((80, 80, 80))
        elif not self.rect.collidepoint(mouse) and pressed:
            self.typing = False
            self.image.fill((30, 30, 30))

        if self.typing:
            for event in el.settings.event:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        el.name = el.name[:-1]
                    elif pygame.key.name(event.key) in validChars:
                        if pygame.key.get_mods() & pygame.KMOD_CAPS:
                            el.name += pygame.key.name(event.key).upper()
                        else:
                            el.name += pygame.key.name(event.key)
        rect = pygame.Rect((self.start - 1, self.y - 1), (self.w + 2, self.h + 2))

        if len(el.name) > 3:
            el.valid = True
            pygame.draw.rect(el.display_surface, "green", rect)
        elif len(el.name) > 0:
            pygame.draw.rect(el.display_surface, "red", rect)
        elif self.typing:
            pygame.draw.rect(el.display_surface, "blue", rect)

class Changename:
    def __init__(self, surface, settings):
        self.groupSound = None
        self.settings = settings
        self.state = "name"
        self.name = ""
        self.valid = False
        self.display_surface = surface
        self.init_menu()

    def init_menu(self):
        self.groupSound = pygame.sprite.Group()
        self.groupSound.add(Input(self.settings.screen_w / 2, 350, "input"))
        self.groupSound.add(Button(self.settings.screen_w / 2+150, 500, "main_menu", self.settings))
        self.groupSound.add(Button(self.settings.screen_w / 2-150, 500, "exit_to_desktop", self.settings))

    def draw(self):
        self.state = "name"
        self.groupSound.update(self)
        self.groupSound.draw(self.display_surface)
        txt = self.settings.font.render(self.name, True, pygame.Color("coral"))
        self.display_surface.blit(txt, (self.settings.screen_w / 2 - 140, 350+4))
        if self.state == "main_menu" and self.valid:
            self.settings.updateName(self.name)
            return self.state
        elif not self.state == "main_menu":
            return self.state