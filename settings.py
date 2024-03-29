import os
import pygame
from logo import Logo
from extras import Icon
d = 'levels'

def import_folder(path,size):  # nalaganje vseh *.png datotek
    arr = []
    for filename in os.listdir(path):
        if not filename.endswith('.png'):
            continue
        arr.append(pygame.transform.scale(pygame.image.load(path + filename).convert_alpha(), size))
    return arr
def sound(path, volume):  # nalaganje vseh *.png datotek
    arr = []
    for filename in os.listdir(path):
        if not filename.endswith('.ogg'):
            continue
        x = pygame.mixer.Sound(path + filename)
        pygame.mixer.Sound.set_volume(x, volume)
        arr.append(x)
    return arr


def tiles(path,size):  # nalaganje vseh *.png datotek
    arr = {}
    for filename in os.listdir(path):
        if not filename.endswith('.png'):
            continue
        id = filename.split(".")[0].split("_")[1]
        arr[id] = pygame.transform.scale(pygame.image.load(path+filename).convert_alpha(),size)
    return arr

map = []
scores = []
for i,filename in enumerate(sorted(os.listdir("./levels"),key=lambda x:int(x.split(".")[0]))):
    arr = []
    f = open("./highScores/"+str(i+1)+".txt", "a")
    f.close()
    if not filename.endswith('.csv'):
        continue
    with open("./levels/" + filename, 'r') as f:  # nalaganje levela iz datoteke
        for line in f.readlines():
            arr.append(line.strip().split(';'))
    map.append(arr)

for filename in sorted(os.listdir("./highScores"),key=lambda x:int(x.split(".")[0])):
    arr2 = {}
    if not filename.endswith('.txt'):
        continue
    with open("./highscores/" + filename, 'r') as f:  # nalaganje levela iz datoteke
        for line in f.readlines():
            line = line.strip()
            arr2[line.split(";")[0]] = line.split(";")[1]
    scores.append(arr2)

tile_size = 64
screen_w = 1200
screen_h = 768
music_volume = 0.1
effects_volume = 0.1

class Background(pygame.sprite.Sprite):
    def __init__(self, x, y, surface,settings):
        super().__init__()
        self.settings = settings
        self.surf = surface
        self.image = self.surf
        self.rect = self.image.get_rect(topleft=(x, y))

    def resize(self):
        self.image = pygame.transform.scale(self.surf,(self.surf.get_width()*self.settings.screen_mul,self.surf.get_height()*self.settings.screen_mul))

class Settings():
    def __init__(self):
        pygame.mixer.init()
        global music_volume, effects_volume, tile_size, screen_w, screen_h
        self.levelIndex = 0
        self.levels = map
        self.scores = scores
        self.screen_mul = 1
        self.screen_w = screen_w*self.screen_mul
        self.screen_h = screen_h*self.screen_mul
        self.tile_size = tile_size*self.screen_mul
        self.inGame = False
        self.wrote = False
        self.pause = False
        self.score = 0
        self.state = "name"
        self.event = pygame.event.get()
        self.font = pygame.font.SysFont("Courier", 18)
        self.readAbout = []
        self.name = ""
        self.buttons = {
            "up": "up",
            "down": "down",
            "left": "left",
            "right": "right"
        }
        self.jump = "up"
        self.left = "left"
        self.down = "down"
        self.right = "right"
        self.vol = [music_volume, effects_volume]
        self.loadSettings()
        self.leftClick = False

    def resize(self):
        self.background.sprite.resize()
        self.logo.sprite.resize()
    def begin(self):
        self.background = pygame.sprite.GroupSingle()
        self.sfx = pygame.sprite.GroupSingle()
        self.music = pygame.sprite.GroupSingle()
        self.sfx.add(Icon(360,270,"sfx.png",self))
        self.music.add(Icon(360,200,"music.png",self))
        self.lvlSelect = pygame.transform.scale(pygame.image.load("./Assets/background/bg_hol.png"),
                                                (1200 * self.screen_mul, 768 * self.screen_mul))
        self.license = pygame.transform.scale(pygame.image.load("./Assets/background/about.png"),
                                              (1000 * self.screen_mul, 1000 * self.screen_mul))
        self.about = pygame.transform.scale(pygame.image.load("./Assets/background/story.png"),
                                            (1000 * self.screen_mul, 1000 * self.screen_mul))
        self.background.add(Background(0, 0,
                                       pygame.transform.scale(pygame.image.load("./Assets/background/bg_hole.png"),
                                                              (1200 * self.screen_mul, 768 * self.screen_mul)),self))
        self.tile = tiles("./Assets/tla/", (64 * self.screen_mul, 64 * self.screen_mul))
        self.finish = pygame.transform.scale(pygame.image.load("./Assets/finish/e.png").convert_alpha(),
                                             (64 * self.screen_mul, 64 * self.screen_mul))
        self.coin = import_folder("./Assets/coin/game/", (20 * self.screen_mul, 20 * self.screen_mul))
        self.start = pygame.transform.scale(pygame.image.load("./Assets/start/start.png").convert_alpha(),
                                            (300 * self.screen_mul, 20 * self.screen_mul))
        self.logo = pygame.sprite.GroupSingle()
        self.logo.add(Logo(self))
        self.enemyFrames = {
            "run": import_folder("./Assets/enemy/run/game/", (64 * self.screen_mul, 64 * self.screen_mul))}
        self.spikeFrames = {
            "spike": import_folder("./Assets/spike/game/", (32 * self.screen_mul, 29 * self.screen_mul))}
        self.enemyFlyFrames = {
            "fly": import_folder("./Assets/flyingenemy/fly/game/", (64 * self.screen_mul, 64 * self.screen_mul)),
            "die": import_folder("./Assets/flyingenemy/death/game/", (64 * self.screen_mul, 64 * self.screen_mul)),
            "shoot": import_folder("./Assets/flyingenemy/attack/game/", (64 * self.screen_mul, 64 * self.screen_mul)),
        }
        self.keys = {
            "up": pygame.image.load("./Assets/menu/keys/KeyboardButtonsDir_up.png"),
            "down": pygame.image.load("./Assets/menu/keys/KeyboardButtonsDir_down.png"),
            "left": pygame.image.load("./Assets/menu/keys/KeyboardButtonsDir_left.png"),
            "right": pygame.image.load("./Assets/menu/keys/KeyboardButtonsDir_right.png"),
            "uni": pygame.image.load("./Assets/menu/keys/KeyboardButtons_Base.png")
        }
        self.keysPressed = {
            "up": pygame.image.load("./Assets/menu/keys/KeyboardButtonsDir_up0.png"),
            "down": pygame.image.load("./Assets/menu/keys/KeyboardButtonsDir_down0.png"),
            "left": pygame.image.load("./Assets/menu/keys/KeyboardButtonsDir_left0.png"),
            "right": pygame.image.load("./Assets/menu/keys/KeyboardButtonsDir_right0.png"),
            "uni": pygame.image.load("./Assets/menu/keys/KeyboardButtons_Base0.png")
        }
        self.kamikazeEnemyFrames = {
            "fly": import_folder("./Assets/enemybird/fly/game/", (32 * self.screen_mul, 32 * self.screen_mul)),
            "die": import_folder("./Assets/enemybird/death/game/", (32 * self.screen_mul, 32 * self.screen_mul)),
            "ready": import_folder("./Assets/enemybird/blink/game/", (32 * self.screen_mul, 32 * self.screen_mul)),
            "attack": import_folder("./Assets/enemybird/attack/game/", (32 * self.screen_mul, 32 * self.screen_mul)),
            "stand": import_folder("./Assets/enemybird/stand/game/", (32 * self.screen_mul, 32 * self.screen_mul)),
        }
        self.bulletFrames = {
            "fly": import_folder("./Assets/bullet/fly/game/", (25 * self.screen_mul, 4 * self.screen_mul)),
            "die": import_folder("./Assets/bullet/hit/game/", (64 * self.screen_mul, 64 * self.screen_mul)),
        }
        self.playerFrames = {
            "front": import_folder("./Assets/player/idle/game/", (40 * self.screen_mul, 60 * self.screen_mul)),
            "run": import_folder("./Assets/player/run/game/", (40 * self.screen_mul, 60 * self.screen_mul)),
            "jump": import_folder("./Assets/player/jump/game/", (40 * self.screen_mul, 60 * self.screen_mul)),
            "holdWall": import_folder("./Assets/player/hold/game/", (40 * self.screen_mul, 60 * self.screen_mul))
        }


    def startSound(self):
        self.deathSound = pygame.mixer.Sound("./Assets/sounds/death.mp3")
        self.coinSound = pygame.mixer.Sound("./Assets/sounds/coin.mp3")
        self.playerJump = pygame.mixer.Sound("./Assets/sounds/jump_02.wav")
        self.menuMusic = pygame.mixer.Sound("./Assets/sounds/menumusic.mp3")
        self.gameMusic = pygame.mixer.Sound("./Assets/sounds/gameMusic.mp3")
        self.hitEnemy = pygame.mixer.Sound("./Assets/sounds/hit_enemy.wav")
        self.HoverSound = pygame.mixer.Sound("./Assets/sounds/hover.wav")
        self.ClickSound = pygame.mixer.Sound("./Assets/sounds/test.wav")
        self.playerWalk = sound("./Assets/sounds/walk/", self.vol[1])
        self.updateSound()
        self.loadAbout()
        self.menuMusic.play(-1, 0, 200)

    def loadAbout(self):
        with open("./settings/name.txt", 'r') as f:
            for line in f.readlines():
                line = line.strip()
                self.readAbout.append(line)

    def updateReadAbout(self):
        self.readAbout.append(self.name)
        with open("./settings/name.txt", 'a') as f:
            f.write(self.name+"\n")
    def updateName(self, name):
        self.name = name
    def updateSound(self):
        pygame.mixer.Sound.set_volume(self.playerJump, self.vol[1]/3)
        pygame.mixer.Sound.set_volume(self.menuMusic, self.vol[0]/3)
        pygame.mixer.Sound.set_volume(self.gameMusic, self.vol[0]/3)
        pygame.mixer.Sound.set_volume(self.hitEnemy, self.vol[1]/3)
        pygame.mixer.Sound.set_volume(self.HoverSound, self.vol[1]/3)
        pygame.mixer.Sound.set_volume(self.ClickSound, self.vol[1]/3)
        pygame.mixer.Sound.set_volume(self.coinSound, self.vol[1])
        pygame.mixer.Sound.set_volume(self.deathSound, self.vol[1])
        for x in self.playerWalk:
            pygame.mixer.Sound.set_volume(x, self.vol[1])

    def loadSettings(self):
        f = open("./settings/settings.txt", 'r')
        lines = f.readlines()
        if len(lines) == 6:
            self.vol[0] = float(lines[0].strip())
            self.vol[1] = float(lines[1].strip())
            self.buttons["up"] = lines[2].strip()
            self.buttons["down"] = lines[3].strip()
            self.buttons["left"] = lines[4].strip()
            self.buttons["right"] = lines[5].strip()
        f.close()
    def writeSettings(self):
        f = open("./settings/settings.txt", "w")
        string = str(self.vol[0]) +"\n"
        string += str(self.vol[1]) +"\n"
        string += str(self.buttons["up"]) + "\n"
        string += str(self.buttons["down"]) + "\n"
        string += str(self.buttons["left"]) + "\n"
        string += str(self.buttons["right"]) + "\n"
        f.write(string)
        f.close()
    def writeScore(self):
        for i,level in enumerate(self.scores):
            f = open("./highScores/"+str(i+1)+".txt", "w")
            string = ""
            for score in level.items():
                string += str(score[0])+";"+str(score[1])+"\n"
            f.write(string)
            f.close()
