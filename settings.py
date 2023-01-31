import os
import pygame
from logo import Logo

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


def tiles(path):  # nalaganje vseh *.png datotek
    arr = {}
    for filename in os.listdir(path):
        if not filename.endswith('.png'):
            continue
        id = filename.split(".")[0].split("_")[1]
        arr[id] = pygame.image.load(path+filename).convert_alpha()
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
    def __init__(self, x, y, surface):
        super().__init__()
        self.image = surface
        self.rect = self.image.get_rect(topleft=(x, y))

class Settings():
    def __init__(self):
        pygame.mixer.init()
        global music_volume, effects_volume, tile_size, screen_w, screen_h
        self.levelIndex = 0
        self.levels = map
        self.scores = scores
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.tile_size = tile_size
        self.inGame = False
        self.wrote = False
        self.pause = False
        self.score = 0
        self.state = "name"
        self.event = pygame.event.get()
        self.font = pygame.font.SysFont("Courier", 18)
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
        self.background = pygame.sprite.Group()
        self.leftClick = False
        self.lvlSelect = pygame.image.load("./Assets/background/bg_hol.png")
        self.background.add(Background(0,0,pygame.image.load("./Assets/background/bg_hole.png")))
        self.deathSound = pygame.mixer.Sound("./Assets/sounds/death.mp3")
        self.coinSound = pygame.mixer.Sound("./Assets/sounds/coin.mp3")
        self.playerJump = pygame.mixer.Sound("./Assets/sounds/jump_02.wav")
        self.menuMusic = pygame.mixer.Sound("./Assets/sounds/menumusic.mp3")
        self.gameMusic = pygame.mixer.Sound("./Assets/sounds/gameMusic.mp3")
        self.hitEnemy = pygame.mixer.Sound("./Assets/sounds/hit_enemy.wav")
        self.HoverSound = pygame.mixer.Sound("./Assets/sounds/hover.wav")
        self.ClickSound = pygame.mixer.Sound("./Assets/sounds/test.wav")
        self.playerWalk = sound("./Assets/sounds/walk/", self.vol[1])
        self.tile = tiles("./Assets/tla/")
        self.finish = pygame.image.load("./Assets/finish/e.png").convert_alpha()
        self.coin = import_folder("./Assets/coin/game/", (20,20))
        self.start = pygame.image.load("./Assets/start/start.png").convert_alpha()
        self.logo = pygame.sprite.GroupSingle()
        self.logo.add(Logo(380,80,self))
        self.enemyFrames = {"run": import_folder("./Assets/enemy/run/game/", (64,64))}
        self.spikeFrames = {"spike": import_folder("./Assets/spike/game/", (32,29))}
        self.enemyFlyFrames = {
            "fly": import_folder("./Assets/flyingenemy/fly/game/", (64,64)),
            "die": import_folder("./Assets/flyingenemy/death/game/", (64,64)),
            "shoot": import_folder("./Assets/flyingenemy/attack/game/", (64,64)),
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
            "fly": import_folder("./Assets/enemybird/fly/game/", (32, 32)),
            "die": import_folder("./Assets/enemybird/death/game/", (32, 32)),
            "ready": import_folder("./Assets/enemybird/blink/game/", (32, 32)),
            "attack": import_folder("./Assets/enemybird/attack/game/", (32, 32)),
            "stand": import_folder("./Assets/enemybird/stand/game/", (32, 32)),
        }
        self.bulletFrames = {
            "fly": import_folder("./Assets/bullet/fly/game/", (25,4)),
            "die": import_folder("./Assets/bullet/hit/game/", (64, 64)),
        }
        self.playerFrames = {
           "front": import_folder("./Assets/player/idle/game/", (40,60)),
           "run": import_folder("./Assets/player/run/game/", (40,60)),
           "jump": import_folder("./Assets/player/jump/game/", (40,60)),
           "holdWall": import_folder("./Assets/player/hold/game/", (40,60))
        }
        self.updateSound()
        self.menuMusic.play(-1, 0, 200)

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
