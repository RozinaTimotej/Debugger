import pygame
from mainMenu import Button

class LevelButton(pygame.sprite.Sprite):
    def __init__(self, x, y, id,settings):
        super().__init__()
        self.id = id
        self.settings = settings
        self.w = 64
        self.h = 64
        self.start = x - self.w / 2
        self.y = y
        self.image = pygame.Surface((self.w, self.h))
        self.textSurf = self.settings.font.render(str(id), 1, "red")
        self.w1,self.h1  = self.settings.font.size(str(id))
        self.image.blit(self.textSurf, [self.w / 2 - self.w1/2, self.h / 2 - self.h1/2])
        self.rect = self.image.get_rect(topleft=(x - self.w / 2, y))

    def update(self, el):
        self.rect.y += el.y
        mouse = pygame.mouse.get_pos()
        pressed = pygame.mouse.get_pressed()[0]
        if self.rect.collidepoint(mouse) and mouse[1] < 4*self.settings.screen_h/5:
            self.image.fill((80, 80, 80))
            self.image.blit(self.textSurf, [self.w / 2 - self.w1/2, self.h / 2 - self.h1/2])
            if pressed:
                self.settings.levelIndex = int(self.id)
                el.state = "playing"
        elif not (self.rect.collidepoint(mouse) and mouse[1] < 4*self.settings.screen_h/5):
            self.image.fill((30, 30, 30))
            self.image.blit(self.textSurf, [self.w / 2 - self.w1/2, self.h / 2 - self.h1/2])

class Block(pygame.sprite.Sprite):
    def __init__(self, x,y,w,h, settings):
        super().__init__()
        self.image = pygame.Surface((w, h))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.image.fill((0, 0, 0))

class LevelSelect:
    def __init__(self, surface, settings):
        self.buttons = None
        self.settings = settings
        self.state = "select"
        self.y = 0
        self.display_surface = surface
        self.init_menu()

    def init_menu(self):
        self.lvls = pygame.sprite.Group()
        self.buttons = pygame.sprite.Group()
        self.ui = pygame.sprite.Group()
        for i,lvl in enumerate(self.settings.levels):
            self.lvls.add(LevelButton((self.settings.screen_w / 5 * (i % 5))+((self.settings.screen_w / 5) /2), 200 * (1+(i // 5)), i,self.settings))
        self.buttons.add(Button(self.settings.screen_w / 2+150, 700, "main_menu", self.settings))
        self.buttons.add(Button(self.settings.screen_w / 2-150, 700, "exit_to_desktop", self.settings))
        self.ui.add(Block(0, 4*self.settings.screen_h/5, self.settings.screen_w, self.settings.screen_h/5, self.settings))

    def draw(self):
        self.state = "select"
        if self.y > 0:
            self.y -= 1
        elif self.y < 0:
            self.y += 1
        for event in self.settings.event:
            if event.type == pygame.MOUSEWHEEL:
                self.y += event.y*2
        self.lvls.update(self)
        self.buttons.update(self)
        self.lvls.draw(self.display_surface)
        self.ui.draw(self.display_surface)
        self.buttons.draw(self.display_surface)
        return self.state