import os
import pygame

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

for filename in os.listdir("./levels"):
    arr = []
    if not filename.endswith('.txt'):
        continue
    with open("./levels/" + filename, 'r') as f:  # nalaganje levela iz datoteke
        for line in f.readlines():
            arr.append(line.strip().split(','))
    map.append(arr)

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
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.tile_size = tile_size
        self.inGame = False
        self.pause = False
        self.state = "name"
        self.event = pygame.event.get()
        self.font = pygame.font.SysFont("Arial", 18)
        self.name = ""
        self.jump = "up"
        self.left = "left"
        self.down = "down"
        self.right = "right"
        self.vol = [music_volume, effects_volume]
        self.background = pygame.sprite.Group()
        self.background.add(Background(0,0,pygame.image.load("./Assets/background/bg1.png")))
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
        self.enemyFrames = {"run": import_folder("./Assets/enemy/run/game/", (64,64))}
        self.spikeFrames = {"spike": import_folder("./Assets/spike/game/", (32,29))}
        self.enemyFlyFrames = {
            "fly": import_folder("./Assets/flyingenemy/fly/game/", (64,64)),
            "die": import_folder("./Assets/flyingenemy/death/game/", (64,64)),
            "shoot": import_folder("./Assets/flyingenemy/attack/game/", (64,64)),
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
        self.menuMusic.play(-1, 0, 2000)

    def updateName(self, name):
        self.name = name
    def updateSound(self):
        pygame.mixer.Sound.set_volume(self.playerJump, self.vol[1]/3)
        pygame.mixer.Sound.set_volume(self.menuMusic, self.vol[0]/3)
        pygame.mixer.Sound.set_volume(self.gameMusic, self.vol[0]/3)
        pygame.mixer.Sound.set_volume(self.hitEnemy, self.vol[1]/3)
        pygame.mixer.Sound.set_volume(self.HoverSound, self.vol[1]/3)
        pygame.mixer.Sound.set_volume(self.ClickSound, self.vol[1]/3)
        for x in self.playerWalk:
            pygame.mixer.Sound.set_volume(x, self.vol[1])
