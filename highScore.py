import pygame
from mainMenu import Button

class PlayerScore(pygame.sprite.Sprite):
    def __init__(self, x, y, name ,score, settings,state):
        super().__init__()
        self.id = id
        self.settings = settings
        self.w = 200
        self.h = 30
        self.start = x - self.w / 2
        self.y = y
        self.setstate = state
        self.same = False
        if settings.name == str(name).strip():
            self.same = True
        self.image = pygame.Surface((self.w, self.h))
        self.textSurf = self.settings.font.render(str(name).strip()+" "+str(score).strip(), 1, "red")
        self.w1, self.h1 = self.settings.font.size(str(id))
        self.image.blit(self.textSurf, [self.w / 2 - self.w1 / 2, self.h / 2 - self.h1 / 2])
        self.rect = self.image.get_rect(topleft=(x - self.w / 2, y))

    def update(self, el):
        self.rect.y += el.y
        if self.same:
            self.image.fill((80, 80, 80))
            self.image.blit(self.textSurf, [self.w / 2 - self.w1 / 2, self.h / 2 - self.h1 / 2])
        elif not self.same:
            self.image.fill((30, 30, 30))
            self.image.blit(self.textSurf, [self.w / 2 - self.w1 / 2, self.h / 2 - self.h1 / 2])


class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, settings):
        super().__init__()
        self.image = pygame.Surface((w, h))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.image.fill((100, 0, 0))


class HighScore:
    def __init__(self, surface, settings,level):
        self.buttons = None
        self.settings = settings
        self.state = "highscore"
        self.y = 0
        self.display_surface = surface
        self.scores = dict(sorted(settings.scores[level].items(),key=lambda item:float(item[1]),reverse=True))
        self.init_menu()

    def init_menu(self):
        self.lvls = pygame.sprite.Group()
        self.buttons = pygame.sprite.Group()
        self.ui = pygame.sprite.Group()
        for i,x in enumerate(self.scores.items()):
            self.lvls.add(PlayerScore(self.settings.screen_w / 2, 200+50*i,x[0], x[1], self.settings,"playing"))
        self.buttons.add(Button(self.settings.screen_w / 2 + 150, 700, "lvl", "main_menu", self.settings))
        self.buttons.add(Button(self.settings.screen_w / 2 - 150, 700, "lvl", "exit_to_desktop", self.settings))
        self.ui.add(Block(0, 0, self.settings.screen_w, self.settings.screen_h / 5, self.settings))
        self.ui.add(
            Block(0, 4 * self.settings.screen_h / 5, self.settings.screen_w, self.settings.screen_h / 5, self.settings))

    def draw(self):
        self.state = "highscore"
        if self.y > 0:
            self.y -= 1
        elif self.y < 0:
            self.y += 1
        scroll_lckup = False
        scroll_lckdown = False
        if self.lvls.sprites()[-1].rect.y < (4 * self.settings.screen_h / 5) - 100:
            scroll_lckup = True
            if self.y < 0:
                self.y = 0
        if self.lvls.sprites()[0].rect.y > (self.settings.screen_h / 5) + 35:
            scroll_lckdown = True
            if self.y > 0:
                self.y = 0
        for event in self.settings.event:
            if event.type == pygame.MOUSEWHEEL:
                if event.y > 0 and not scroll_lckdown:
                    self.y += event.y * 2
                elif event.y < 0 and not scroll_lckup:
                    self.y += event.y * 2
        self.settings.background.draw(self.display_surface)
        self.lvls.update(self)
        self.buttons.update(self)
        self.lvls.draw(self.display_surface)
        self.ui.draw(self.display_surface)
        self.buttons.draw(self.display_surface)
        return self.state