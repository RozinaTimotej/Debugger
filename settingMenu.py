import copy
import pygame
from mainMenu import Button
validChars = "1234567890-.,qwertyuiopasdfghjklzxcvbnm"
class Slider(pygame.sprite.Sprite):

    def __init__(self, x, y,folder, id, settings):
        super().__init__()
        self.id = id
        self.settings = settings
        self.w = 300
        self.x = x
        self.y = y
        self.start = (x*self.settings.screen_mul) - (self.w*self.settings.screen_mul) / 2
        self.surf = pygame.image.load('./Assets/menu/' + folder + '/slider_' + str(id) + ".png").convert_alpha()
        self.image = pygame.transform.scale(self.surf, (self.surf.get_width()*self.settings.screen_mul, self.surf.get_height()*self.settings.screen_mul))
        self.rect = self.image.get_rect(topleft=((x*self.settings.screen_mul) - (self.w*self.settings.screen_mul) / 2, (y*self.settings.screen_mul)))

    def resize(self):
        self.start = (self.x * self.settings.screen_mul) - (self.w * self.settings.screen_mul) / 2
        self.image = pygame.transform.scale(self.surf, (self.surf.get_width() * self.settings.screen_mul, self.surf.get_height() * self.settings.screen_mul))
        self.rect = self.image.get_rect(topleft=((self.x * self.settings.screen_mul) - (self.w*self.settings.screen_mul) / 2, (self.y * self.settings.screen_mul)))

    def update(self, el):
        mouse = pygame.mouse.get_pos()
        pressed = pygame.mouse.get_pressed()[0]
        if self.rect.collidepoint(mouse) and pressed:
            self.settings.leftClick = True
            el.settings.vol[self.id] = (mouse[0] - self.start) / (self.w*self.settings.screen_mul)

class Txt(pygame.sprite.Sprite):

    def __init__(self, x, y,dir,settings,txt,surface):
        super().__init__()
        self.display_surface = surface
        self.settings = settings
        self.id = dir
        self.txt = txt
        self.firstx = x
        self.firsty = y
        self.x = x
        self.y = y

    def update(self):
        if not(self.settings.buttons[self.id] == "right" or self.settings.buttons[self.id] == "up" or self.settings.buttons[self.id] == "down" or self.settings.buttons[self.id] == "left"):
            self.txt = self.settings.buttons[self.id]
        else:
            self.txt = ""

        txt = self.settings.font.render(self.txt.upper(), True, pygame.Color("black"))
        self.display_surface.blit(txt, (self.x+20, self.y+10))

    def resize(self):
        self.x = self.firstx*self.settings.screen_mul
        self.y =  self.firsty*self.settings.screen_mul
class Key(pygame.sprite.Sprite):

    def __init__(self, x, y, dir,settings,txt):
        super().__init__()
        self.settings = settings
        self.id = dir
        self.x = x
        self.y = y
        if not (txt == "right" or txt == "up" or txt == "down" or txt == "left"):
            self.image = settings.keys["uni"]
        else:
            self.image = settings.keys[self.id]
        self.txt = self.settings.buttons[self.id]
        self.rect = self.image.get_rect(topleft=(x*self.settings.screen_mul, y*self.settings.screen_mul))
        self.pressed = False

    def resize(self):
        if not (self.txt == "right" or self.txt == "up" or self.txt == "down" or self.txt == "left"):
            self.image = self.settings.keys["uni"]
        else:
            self.image = self.settings.keys[self.id]
        self.image = pygame.transform.scale(self.image, (self.image.get_width() * self.settings.screen_mul, self.image.get_height() * self.settings.screen_mul))
        self.rect = self.image.get_rect(topleft=(self.x * self.settings.screen_mul, self.y * self.settings.screen_mul))

    def update(self):
        self.txt = self.settings.buttons[self.id]
        if not (self.txt == "right" or self.txt == "up" or self.txt == "down" or self.txt == "left") and not self.pressed:
            self.image = self.settings.keys["uni"]
        elif not self.pressed:
            self.image = self.settings.keys[self.id]
        mouse = pygame.mouse.get_pos()
        pressed = pygame.mouse.get_pressed()[0]
        if self.rect.collidepoint(mouse) and pressed and not self.settings.leftClick:
            self.settings.leftClick = True
            self.pressed = True
            self.image = self.settings.keysPressed["uni"]
        elif pressed and not self.settings.leftClick:
            self.settings.leftClick = True
            if not (self.settings.buttons[self.id] == "left" or self.settings.buttons[self.id] == "right" or
                    self.settings.buttons[self.id] == "up" or self.settings.buttons[self.id] == "down"):
                self.image = self.settings.keys["uni"]
                self.pressed = False
                self.settings.leftClick = False
            else:
                self.image = self.settings.keys[self.settings.buttons[self.id]]
                self.pressed = False
                self.settings.leftClick = False
        if self.pressed and not self.settings.leftClick:
            self.settings.leftClick = True
            for event in self.settings.event:
                if event.type == pygame.KEYUP and (pygame.key.name(event.key) in validChars or pygame.key.name(event.key) == "left" or pygame.key.name(
                            event.key) == "right" or pygame.key.name(event.key) == "up" or pygame.key.name(
                            event.key) == "down"):
                    self.settings.buttons[self.id] = pygame.key.name(event.key)
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

    def checkButton(self):
        if not (self.settings.buttons[self.id] == "left" or self.settings.buttons[self.id] == "right" or self.settings.buttons[self.id] == "up" or self.settings.buttons[self.id] == "down"):
            self.image = self.settings.keys["uni"]
            self.pressed = False
        else:
            self.image = self.settings.keys[self.settings.buttons[self.id]]
            self.pressed = False

class SliderMovable(pygame.sprite.Sprite):
    def __init__(self, x, y, id, settings, folder):
        super().__init__()
        self.id = id
        self.settings = settings
        self.x = x
        self.y = y
        self.w = 275
        self.start = (x*self.settings.screen_mul) - (self.w*self.settings.screen_mul) / 2
        self.end = self.start + self.w*self.settings.screen_mul
        img_size = (50*self.settings.screen_mul, 50*self.settings.screen_mul)
        self.imgNormal = pygame.transform.scale(pygame.image.load('./Assets/menu/' + folder + "/tile.png").convert_alpha(), img_size)
        self.imgHover = pygame.transform.scale(pygame.image.load('./Assets/menu/' + folder + "/tile_hover.png").convert_alpha(), img_size)
        self.imageHover =self.imgHover
        self.imageNormal = self.imgNormal
        self.image = self.imageNormal
        self.rect = self.image.get_rect(center=(self.start + (self.settings.vol[id] * self.w), y+20))

    def resize(self):
        self.start = (self.x * self.settings.screen_mul) - (self.w * self.settings.screen_mul) / 2
        self.end = self.start + self.w * self.settings.screen_mul
        img_size = (50 * self.settings.screen_mul, 50 * self.settings.screen_mul)
        self.imageNormal = pygame.transform.scale(self.imgNormal, img_size)
        self.imageHover = pygame.transform.scale(self.imgHover, img_size)
        self.image = self.imageNormal
        self.rect = self.image.get_rect(center=(self.start + (self.settings.vol[self.id] * self.w * self.settings.screen_mul), (self.y * self.settings.screen_mul) + 20))
    def update(self, el):
        self.settings.updateSound()
        self.rect.x = self.start + (el.settings.vol[self.id] * self.w * self.settings.screen_mul) - 20



class SettingsMenu:
    def __init__(self, surface, settings):
        self.groupText = None
        self.groupButtons = None
        self.groupSound = None
        self.settings = settings
        self.prevSound = copy.deepcopy(settings.vol)
        self.prevButtons = copy.deepcopy(settings.buttons)
        self.state = "settings"
        self.prevState = settings.state
        self.display_surface = surface
        self.init_menu()

    def init_menu(self):
        self.groupSound = pygame.sprite.Group()
        self.groupButtons = pygame.sprite.Group()
        self.groupText = pygame.sprite.Group()
        self.groupSound.add(Slider(self.settings.screen_w / 2, 200, "settings",0,self.settings))
        self.groupSound.add(SliderMovable(self.settings.screen_w / 2, 200, 0, self.settings, "settings"))
        self.groupSound.add(Slider(self.settings.screen_w / 2, 275, "settings", 1,self.settings))
        self.groupSound.add(SliderMovable(self.settings.screen_w / 2, 275, 1, self.settings, "settings"))
        self.groupSound.add(Button(self.settings.screen_w / 2+150, 500,"settings", "main_menu", self.settings))
        self.groupSound.add(Button(self.settings.screen_w / 2-150, 500,"settings", "back", self.settings))
        self.groupButtons.add(Key(self.settings.screen_w / 2-25,360,"up",self.settings,self.settings.jump))
        self.groupButtons.add(Key(self.settings.screen_w / 2-25, 430,"down",self.settings,self.settings.down))
        self.groupButtons.add(Key(self.settings.screen_w / 2-25+65, 430,"right",self.settings,self.settings.right))
        self.groupButtons.add(Key(self.settings.screen_w / 2-25-65, 430,"left",self.settings,self.settings.left))
        self.groupText.add(Txt(self.settings.screen_w / 2-25, 360, "up", self.settings, self.settings.jump,self.display_surface))
        self.groupText.add(Txt(self.settings.screen_w / 2-25, 430, "down", self.settings, self.settings.down,self.display_surface))
        self.groupText.add(Txt(self.settings.screen_w / 2-25 + 65, 430, "right", self.settings, self.settings.right,self.display_surface))
        self.groupText.add(Txt(self.settings.screen_w / 2-25 - 65, 430, "left", self.settings, self.settings.left,self.display_surface))

    def resize(self):
        for el in self.groupButtons:
            el.resize()
        for el in self.groupText:
            el.resize()
        for el in self.groupSound:
            el.resize()
    def updateState(self, state):
        self.prevState = state

    def updatePrevSound(self):
        self.prevSound = copy.deepcopy(self.settings.vol)
        self.prevButtons = copy.deepcopy(self.settings.buttons)

    def draw(self):
        self.state = "settings"
        if not self.settings.pause:
            self.settings.background.draw(self.display_surface)
        self.settings.logo.draw(self.display_surface)
        self.groupSound.update(self)
        self.groupButtons.update()
        self.settings.sfx.draw(self.display_surface)
        self.settings.music.draw(self.display_surface)
        self.groupSound.draw(self.display_surface)
        self.groupButtons.draw(self.display_surface)
        self.groupText.update()
        if self.state == "back":
            self.state = "main_menu"
            self.settings.vol = self.prevSound
            self.settings.buttons = self.prevButtons
            for b in self.groupButtons.sprites():
                b.checkButton()
            self.settings.updateSound()
            return self.prevState
        elif self.state == "main_menu":
            self.settings.writeSettings()
            return self.prevState
        else:
            return self.state

