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

class Txt(pygame.sprite.Sprite):

    def __init__(self, x, y,dir,settings,txt,surface):
        super().__init__()
        self.display_surface = surface
        self.settings = settings
        self.id = dir
        self.txt = txt
        self.x = x
        self.y = y

    def update(self):
        if self.id == "up":
            if not(self.settings.jump == "right" or self.settings.jump == "up" or self.settings.jump == "down" or self.settings.jump == "left"):
                self.txt = self.settings.jump
            else:
                self.txt = ""
        if self.id == "down":
            if not(self.settings.down == "right" or self.settings.down == "up" or self.settings.down == "down" or self.settings.down == "left"):
                self.txt = self.settings.down
            else:
                self.txt = ""
        if self.id == "left":
            if not(self.settings.left == "right" or self.settings.left == "up" or self.settings.left == "down" or self.settings.left == "left"):
                self.txt = self.settings.left
            else:
                self.txt = ""
        if self.id == "right":
            if not(self.settings.right == "right" or self.settings.right == "up" or self.settings.right == "down" or self.settings.right == "left"):
                self.txt = self.settings.right
            else:
                self.txt = ""

        txt = self.settings.font.render(self.txt.upper(), True, pygame.Color("black"))
        self.display_surface.blit(txt, (self.x+20, self.y+10))

class Key(pygame.sprite.Sprite):

    def __init__(self, x, y,dir,settings,txt):
        super().__init__()
        self.settings = settings
        self.id = dir
        if not (txt == "right" or txt == "up" or txt == "down" or txt == "left"):
            self.image = settings.keys["uni"]
        else:
            self.image = settings.keys[dir]
        self.txt = txt
        self.rect = self.image.get_rect(topleft=(x, y))
        self.pressed = False

    def update(self):
        mouse = pygame.mouse.get_pos()
        pressed = pygame.mouse.get_pressed()[0]
        if self.rect.collidepoint(mouse) and pressed:
            self.pressed = True
            self.image = self.settings.keys["uni"]
        if self.pressed:
            for event in self.settings.event:
                if event.type == pygame.KEYUP:
                    if self.id == "up":
                        self.settings.jump = pygame.key.name(event.key)
                    if self.id == "down":
                        self.settings.down = pygame.key.name(event.key)
                    if self.id == "left":
                        self.settings.left = pygame.key.name(event.key)
                    if self.id == "right":
                        self.settings.right = pygame.key.name(event.key)
                    if not (pygame.key.name(event.key) == "left" or pygame.key.name(
                            event.key) == "right" or pygame.key.name(event.key) == "up" or pygame.key.name(
                            event.key) == "down"):
                        self.image = self.settings.keys["uni"]
                        self.pressed = False
                    else:
                        self.image = self.settings.keys[pygame.key.name(event.key)]
                        self.pressed = False
                    if event.key == pygame.K_ESCAPE or event.type == pygame.QUIT:
                        self.pressed = False


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
        self.groupButtons = pygame.sprite.Group()
        self.groupText = pygame.sprite.Group()
        self.groupSound.add(Slider(self.settings.screen_w / 2, 100, "settings",0))
        self.groupSound.add(SliderMovable(self.settings.screen_w / 2, 100, 0, self.settings, "settings"))
        self.groupSound.add(Slider(self.settings.screen_w / 2, 200, "settings", 1))
        self.groupSound.add(SliderMovable(self.settings.screen_w / 2, 200, 1, self.settings, "settings"))
        self.groupSound.add(Button(self.settings.screen_w / 2+150, 500,"settings", "main_menu", self.settings))
        self.groupSound.add(Button(self.settings.screen_w / 2-150, 500,"settings", "back", self.settings))
        self.groupButtons.add(Key(self.settings.screen_w / 2,600,"up",self.settings,self.settings.jump))
        self.groupButtons.add(Key(self.settings.screen_w / 2, 700,"down",self.settings,self.settings.down))
        self.groupButtons.add(Key(self.settings.screen_w / 2+65, 700,"right",self.settings,self.settings.right))
        self.groupButtons.add(Key(self.settings.screen_w / 2-65, 700,"left",self.settings,self.settings.left))
        self.groupText.add(Txt(self.settings.screen_w / 2, 600, "up", self.settings, self.settings.jump,self.display_surface))
        self.groupText.add(Txt(self.settings.screen_w / 2, 700, "down", self.settings, self.settings.down,self.display_surface))
        self.groupText.add(Txt(self.settings.screen_w / 2 + 65, 700, "right", self.settings, self.settings.right,self.display_surface))
        self.groupText.add(Txt(self.settings.screen_w / 2 - 65, 700, "left", self.settings, self.settings.left,self.display_surface))

    def updateState(self, state):
        self.prevState = state

    def updatePrevSound(self):
        self.prevSound = copy.deepcopy(self.settings.vol)

    def draw(self):
        self.state = "settings"
        if not self.settings.pause:
            self.settings.background.draw(self.display_surface)
        self.groupSound.update(self)
        self.groupButtons.update()
        self.groupSound.draw(self.display_surface)
        self.groupButtons.draw(self.display_surface)
        self.groupText.update()
        if self.state == "back":
            self.state = "main_menu"
            self.settings.vol = self.prevSound
            self.settings.updateSound()
            return self.prevState
        elif self.state == "main_menu":
            return self.prevState
        else:
            return self.state

