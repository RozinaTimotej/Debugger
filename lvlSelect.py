import pygame
from mainMenu import Button


class LevelButton(pygame.sprite.Sprite):
    def __init__(self, x, y, id, settings,state,personal,high):
        super().__init__()
        self.id = id
        self.settings = settings
        self.w = 90
        self.h = 110
        self.start = x - self.w / 2
        self.x = x
        self.y = y
        self.personal = personal
        self.high = high
        self.setstate = state
        self.image = pygame.Surface((self.w*self.settings.screen_mul, self.h*self.settings.screen_mul))
        self.textSurf1 = self.settings.font.render(str(id+1), 1, "red")
        self.textSurf2 = self.settings.font.render(str(self.high), 1, (255,215,0))
        self.textSurf3 = self.settings.font.render(str(self.personal), 1, "green")
        self.w1, self.h1 = self.settings.font.size(str(self.id))
        self.w2, self.h2 = self.settings.font.size(str(self.high))
        self.w3, self.h3 = self.settings.font.size(str(self.personal))
        self.image.blit(self.textSurf1, [(self.w*self.settings.screen_mul) / 2 - (self.w1) / 2, (self.h*self.settings.screen_mul) / 5 - (self.h1*self.settings.screen_mul) / 2])
        self.image.blit(self.textSurf2,[(self.w * self.settings.screen_mul) / 2 - (self.w2) / 2, (self.h * self.settings.screen_mul) / 2 - (self.h2 * self.settings.screen_mul) / 2])
        self.image.blit(self.textSurf3, [(self.w * self.settings.screen_mul) / 2 - (self.w3) / 2,(self.h * self.settings.screen_mul) / 1.2 - (self.h3 * self.settings.screen_mul) / 2])
        self.rect = self.image.get_rect(topleft=(x*self.settings.screen_mul - (self.w*self.settings.screen_mul) / 2, y*self.settings.screen_mul))

    def resize(self):
        self.image = pygame.Surface((self.w * self.settings.screen_mul, self.h * self.settings.screen_mul))
        self.textSurf1 = self.settings.font.render(str(self.id + 1), 1, "red")
        self.textSurf2 = self.settings.font.render(str(self.high), 1, (255,215,0))
        self.textSurf3 = self.settings.font.render(str(self.personal), 1, "green")
        self.w1, self.h1 = self.settings.font.size(str(self.id))
        self.w2, self.h2 = self.settings.font.size(str(self.high))
        self.w3, self.h3= self.settings.font.size(str(self.personal))
        self.image.blit(self.textSurf1,[(self.w * self.settings.screen_mul) / 2 - (self.w1) / 2,(self.h*self.settings.screen_mul) / 5 - (self.h1 * self.settings.screen_mul) / 2])
        self.image.blit(self.textSurf2,[(self.w * self.settings.screen_mul) / 2 - (self.w2) / 2,(self.h * self.settings.screen_mul) / 2 - (self.h2 * self.settings.screen_mul) / 2])
        self.image.blit(self.textSurf3,[(self.w * self.settings.screen_mul) / 2 - (self.w3) / 2,(self.h * self.settings.screen_mul) / 1.2 - (self.h3 * self.settings.screen_mul) / 2])
        self.rect = self.image.get_rect(topleft=(self.x * self.settings.screen_mul - (self.w * self.settings.screen_mul) / 2, self.y * self.settings.screen_mul))

    def update(self, el):
        self.rect.y += el.y
        mouse = pygame.mouse.get_pos()
        pressed = pygame.mouse.get_pressed()[0]
        if self.rect.collidepoint(mouse) and 4 * self.settings.screen_h / 5 > mouse[1] > 1 * self.settings.screen_h / 5:
            self.image.fill((80, 80, 80))
            self.image.blit(self.textSurf1,[(self.w*self.settings.screen_mul) / 2 -(self.w1) / 2, (self.h*self.settings.screen_mul) / 5 - (self.h1*self.settings.screen_mul) / 2])
            self.image.blit(self.textSurf2, [(self.w * self.settings.screen_mul) / 2 - (self.w2) / 2, (self.h * self.settings.screen_mul) / 2 - (self.h2 * self.settings.screen_mul) / 2])
            self.image.blit(self.textSurf3, [(self.w * self.settings.screen_mul) / 2 - (self.w3) / 2, (self.h * self.settings.screen_mul) / 1.2 - (self.h3 * self.settings.screen_mul) / 2])
            if pressed and not self.settings.leftClick:
                self.settings.leftClick = True
                if not self.setstate == "highscore":
                    self.settings.menuMusic.stop()
                    self.settings.gameMusic.play(-1, 0, 200)
                self.settings.levelIndex = int(self.id)
                el.state = self.setstate
        elif not (self.rect.collidepoint(mouse) and 4 * self.settings.screen_h / 5 > mouse[1] > 1 * self.settings.screen_h / 5):
            self.image.fill((30, 30, 30))
            self.image.blit(self.textSurf1, [(self.w*self.settings.screen_mul) / 2 -(self.w1) / 2, (self.h*self.settings.screen_mul) / 5 - (self.h1*self.settings.screen_mul) / 2])
            self.image.blit(self.textSurf2, [(self.w * self.settings.screen_mul) / 2 - (self.w2) / 2,(self.h * self.settings.screen_mul) / 2 - (self.h2 * self.settings.screen_mul) / 2])
            self.image.blit(self.textSurf3,[(self.w * self.settings.screen_mul) / 2 - (self.w3) / 2,(self.h * self.settings.screen_mul) / 1.2 - (self.h3 * self.settings.screen_mul) / 2])


class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, settings):
        super().__init__()
        self.settings = settings
        self.image = pygame.transform.scale(self.settings.lvlSelect,(self.settings.lvlSelect.get_width()*self.settings.screen_mul,self.settings.lvlSelect.get_height()*self.settings.screen_mul))
        self.x = x
        self.y = y
        self.rect = self.image.get_rect(topleft=(self.x*self.settings.screen_mul, self.y*self.settings.screen_mul))

    def resize(self):
        self.image = pygame.transform.scale(self.settings.lvlSelect,(self.settings.lvlSelect.get_width()*self.settings.screen_mul,self.settings.lvlSelect.get_height()*self.settings.screen_mul))
        self.rect = self.image.get_rect(topleft=(self.x*self.settings.screen_mul, self.y*self.settings.screen_mul))


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
        for i, lvl in enumerate(self.settings.levels):
            curr_lvl = dict(sorted(self.settings.scores[i].items(), key=lambda item: float(item[1]), reverse=False))
            if len(curr_lvl) > 0:
                high = list(curr_lvl.values())[0]
                if self.settings.name in curr_lvl:
                    personal = curr_lvl[self.settings.name]
                else:
                    personal = "/"
            else:
                personal = "/"
                high = "/"
            self.lvls.add(LevelButton((70 + ((self.settings.screen_w-160) / 7 * (i % 7))) + ((self.settings.screen_w / 7) / 2), 50 + (150 * (1 + (i // 7))) , i, self.settings,"playing",personal,high))
        self.buttons.add(Button(self.settings.screen_w / 2 + 150, 700, "lvl", "main_menu", self.settings))
        self.buttons.add(Button(self.settings.screen_w / 2 - 150, 700, "lvl", "exit_to_desktop", self.settings))
        self.ui.add(Block(0, 0, self.settings.screen_w, self.settings.screen_h / 5, self.settings))

    def resize(self):
        for el in self.ui:
            el.resize()
        for el in self.buttons:
            el.resize()
        for el in self.lvls:
            el.resize()

    def draw(self):
        self.state = "select"
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
        self.settings.logo.draw(self.display_surface)
        self.buttons.draw(self.display_surface)
        return self.state

class HighScoreLevel:
    def __init__(self, surface, settings):
        self.buttons = None
        self.settings = settings
        self.state = "highscoreselect"
        self.y = 0
        self.display_surface = surface
        self.init_menu()

    def init_menu(self):
        self.lvls = pygame.sprite.Group()
        self.buttons = pygame.sprite.Group()
        self.ui = pygame.sprite.Group()
        for i, lvl in enumerate(self.settings.levels):
            curr_lvl = dict(sorted(self.settings.scores[i].items(),key=lambda item:float(item[1]),reverse=False))
            if len(curr_lvl) > 0:
                high = list(curr_lvl.values())[0]
                if self.settings.name in curr_lvl:
                    personal = curr_lvl[self.settings.name]
                else:
                    personal = "/"
            else:
                personal = "/"
                high = "/"
            self.lvls.add(LevelButton((70 + ((self.settings.screen_w-160) / 7 * (i % 7))) + ((self.settings.screen_w / 7) / 2), 50 + (150 * (1 + (i // 7))) , i, self.settings,"highscore",personal,high))
        self.buttons.add(Button(self.settings.screen_w / 2 + 150, 700, "lvl", "back", self.settings))
        self.buttons.add(Button(self.settings.screen_w / 2 - 150, 700, "lvl", "exit_to_desktop", self.settings))
        self.ui.add(Block(0, 0, self.settings.screen_w, self.settings.screen_h / 5, self.settings))

    def resize(self):
        for el in self.ui:
            el.resize()
        for el in self.buttons:
            el.resize()
        for el in self.lvls:
            el.resize()
    def draw(self):
        self.state = "highscoreselect"
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
        self.settings.logo.draw(self.display_surface)
        self.buttons.draw(self.display_surface)
        if self.state == "back":
            self.state = "main_menu"
        return self.state