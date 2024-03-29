import pygame

from mainMenu import Button
validChars = "`1234567890-=qwertyuiop[]\\asdfghjkl;'zxcvbnm,./"
class Input(pygame.sprite.Sprite):
    def __init__(self, id,settings):
        super().__init__()
        self.id = id
        self.settings = settings
        self.w = 320*self.settings.screen_mul
        self.h = 30*self.settings.screen_mul
        self.y = 325
        self.x = self.settings.screen_w / 2
        self.start = self.x * self.settings.screen_mul - self.w / 2
        self.typing = False
        self.image = pygame.Surface((self.w, self.h))
        self.image.fill((30, 30, 30))
        self.rect = self.image.get_rect(topleft=(self.x*self.settings.screen_mul - self.w / 2, self.y*self.settings.screen_mul ))

    def resize(self):
        self.w = 320 * self.settings.screen_mul
        self.h = 30 * self.settings.screen_mul
        self.start = self.x * self.settings.screen_mul - self.w / 2
        self.image = pygame.Surface((self.w, self.h))
        self.image.fill((30, 30, 30))
        self.rect = self.image.get_rect(topleft=(self.x*self.settings.screen_mul  - self.w / 2, self.y*self.settings.screen_mul ))
    def update(self, el):
        mouse = pygame.mouse.get_pos()
        pressed = pygame.mouse.get_pressed()[0]
        if self.rect.collidepoint(mouse) and pressed and not self.settings.leftClick:
            self.settings.leftClick = True
            self.typing = True
            self.image.fill((80, 80, 80))
        elif not self.rect.collidepoint(mouse) and pressed and not self.settings.leftClick:
            self.typing = False
            self.image.fill((30, 30, 30))

        if self.typing:
            for event in el.settings.event:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        el.name = el.name[:-1]
                    elif pygame.key.name(event.key) in validChars and len(el.name) < 20:
                        if pygame.key.get_mods() & (pygame.KMOD_CAPS or pygame.KMOD_SHIFT):
                            el.name += pygame.key.name(event.key).upper()
                        else:
                            el.name += pygame.key.name(event.key)
        rect = pygame.Rect((self.start - 1, self.y*self.settings.screen_mul - 1), (self.w + 2, self.h + 2))

        if len(el.name) > 3:
            el.valid = True
            pygame.draw.rect(el.display_surface, "green", rect)
        elif len(el.name) > 0:
            el.valid = False
            pygame.draw.rect(el.display_surface, "red", rect)
        elif self.typing:
            pygame.draw.rect(el.display_surface, "blue", rect)

class Changename:
    def __init__(self, surface, settings):
        self.nameGroup = None
        self.settings = settings
        self.state = "name"
        self.name = ""
        self.valid = False
        self.display_surface = surface
        self.init_menu()

    def init_menu(self):
        self.nameGroup = pygame.sprite.Group()
        self.nameGroup.add(Input("input",self.settings))
        self.nameGroup.add(Button(self.settings.screen_w / 2,85, 400,"name", "main_menu", self.settings))
        self.nameGroup.add(Button(self.settings.screen_w / 2,-85, 400,"name", "exit_to_desktop", self.settings))

    def resize(self):
        for el in self.nameGroup:
            el.resize()

    def draw(self):
        self.state = "name"
        self.settings.background.draw(self.display_surface)
        self.settings.logo.draw(self.display_surface)
        self.nameGroup.update(self)
        self.nameGroup.draw(self.display_surface)
        txt = self.settings.font.render(self.name, True, pygame.Color("coral"))
        self.display_surface.blit(txt, (self.settings.screen_w / 2 - 140, 320 * self.settings.screen_mul - 4 + (30 * self.settings.screen_mul/2)))
        if self.state == "main_menu" and self.valid:
            self.settings.updateName(self.name)
            if self.settings.name in self.settings.readAbout:
                return "main_menu"
            return "about"
        elif not self.state == "main_menu":
            return self.state
        else:
            return "name"