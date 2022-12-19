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
        self.image.blit(self.textSurf, [self.w / 2, self.h / 2])
        self.rect = self.image.get_rect(topleft=(x - self.w / 2, y))

    def update(self, el):
        mouse = pygame.mouse.get_pos()
        pressed = pygame.mouse.get_pressed()[0]
        if self.rect.collidepoint(mouse):
            self.image.fill((80, 80, 80))
            self.image.blit(self.textSurf, [self.w / 2, self.h / 2])
            if pressed:
                self.settings.levelIndex = int(self.id)
                el.state = "playing"
        elif not self.rect.collidepoint(mouse):
            self.image.fill((30, 30, 30))
            self.image.blit(self.textSurf, [self.w / 2, self.h / 2])

        rect = pygame.Rect((self.start - 1, self.y - 1), (self.w + 2, self.h + 2))


class LevelSelect:
    def __init__(self, surface, settings):
        self.groupSound = None
        self.settings = settings
        self.state = "select"
        self.valid = False
        self.display_surface = surface
        self.init_menu()

    def init_menu(self):
        self.groupSound = pygame.sprite.Group()
        for i,lvl in enumerate(self.settings.levels):
            self.groupSound.add(LevelButton((self.settings.screen_w / 3 * (i % 3))+((self.settings.screen_w / 3) /2), 200 * (1+(i // 3)), i,self.settings))
        self.groupSound.add(Button(self.settings.screen_w / 2+150, 500, "main_menu", self.settings))
        self.groupSound.add(Button(self.settings.screen_w / 2-150, 500, "exit_to_desktop", self.settings))

    def draw(self):
        self.state = "select"
        self.groupSound.update(self)
        self.groupSound.draw(self.display_surface)
        return self.state