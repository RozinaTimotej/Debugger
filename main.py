import pygame, sys
from settings import Settings
from level import Level
from mainMenu import MainMenu, PauseMenu
from settingMenu import SettingsMenu
from ChangeName import Changename
from lvlSelect import LevelSelect, HighScoreLevel
from endLevel import DieMenu
from finishMenu import FinishMenu
from highScore import HighScore
from extras import About, License

clock = pygame.time.Clock()
pygame.init()
settings = Settings()
screen = pygame.display.set_mode((settings.screen_w, settings.screen_h),pygame.RESIZABLE)
settings.begin()
settings.startSound()
pygame.display.set_caption('Debugger', "./Assets/player/idle/game/sprite_0.png")
pygame.display.set_icon(settings.playerFrames["front"][0])
settingMenu = SettingsMenu(screen, settings)
changeName = Changename(screen, settings)
startMenu = MainMenu(screen, settings, settingMenu)
pauseMenu = PauseMenu(screen, settings, settingMenu)
dieMenu = DieMenu(screen, settings)
finishMenu = FinishMenu(screen, settings)
levelSelect = LevelSelect(screen, settings)
highScoreLevel = HighScoreLevel(screen, settings)
level = Level(settings.levels[settings.levelIndex], screen, settings)
highScore = HighScore(screen, settings, settings.levelIndex)
about = About(screen, settings)
license = License(screen, settings)

print(pygame.version.ver)

def update_fps():
    fps = str(int(clock.get_fps()))
    fps_text = settings.font.render(fps, True, pygame.Color("coral"))
    return fps_text


while True:
    settings.event = pygame.event.get()
    for event in settings.event:
        if event.type == pygame.QUIT or settings.state == "exit_to_desktop":
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE and (settings.state == "playing" or settings.state == "pause_menu"):
                settings.pause = not settings.pause
                if not settings.pause:
                    level.updateStartTime()
                settings.state = "playing"
            if not level.started:
                level.starts()
        elif event.type == pygame.VIDEORESIZE:
            width, height = event.size
            if 1200 > width or height < 768:
                screen = pygame.display.set_mode((1200, 768), pygame.RESIZABLE)
                settings.screen_mul = 1
                settings.screen_w = 1200
                settings.screen_h = 768
                settings.tile_size = 64
                settings.resize()
                changeName.resize()
                startMenu.resize()
                pauseMenu.resize()
                settingMenu.resize()
                highScore.resize()
                highScoreLevel.resize()
                levelSelect.resize()
                about.resize()
                dieMenu.resize()
                finishMenu.resize()
                license.resize()
                level = Level(settings.levels[settings.levelIndex], screen, settings)
            else:
                screen = pygame.display.set_mode((height*1.5625, height), pygame.RESIZABLE)
                settings.screen_mul = height/768
                settings.screen_w = 1200 * settings.screen_mul
                settings.screen_h = 768 * settings.screen_mul
                settings.tile_size = 64 * settings.screen_mul
                settings.resize()
                changeName.resize()
                startMenu.resize()
                dieMenu.resize()
                pauseMenu.resize()
                settingMenu.resize()
                highScore.resize()
                highScoreLevel.resize()
                levelSelect.resize()
                finishMenu.resize()
                about.resize()
                license.resize()
                level = Level(settings.levels[settings.levelIndex], screen, settings)
    if not pygame.mouse.get_pressed()[0]:
        settings.leftClick = False
    if settings.state == "playing" and not settings.pause:
        settings.state = level.draw()
    elif settings.pause and (settings.state == "pause_menu" or settings.state == "playing"):
        level.draw()
        settings.state = pauseMenu.draw()
        if settings.state == "restart":
            level = Level(settings.levels[settings.levelIndex], screen, settings)
            settings.state = "playing"
            settings.pause = False
        if settings.state == "main_menu":
            settings.pause = False
            level = Level(settings.levels[settings.levelIndex], screen, settings)
        elif settings.state == "playing":
            level.updateStartTime()
        settingMenu.updateState("pause_menu")
    elif settings.state == "name":
        settings.state = changeName.draw()
    elif settings.state == "about":
        settings.state = about.draw()
    elif settings.state == "license":
        settings.state = license.draw()
    elif settings.state == "die_menu":
        level.draw()
        settings.state = dieMenu.draw()
        if settings.state == "restart":
            level = Level(settings.levels[settings.levelIndex], screen, settings)
            settings.state = "playing"
    elif settings.state == "finish_menu":
        level.draw()
        settings.state = finishMenu.draw()
        if settings.state == "restart":
            level = Level(settings.levels[settings.levelIndex], screen, settings)
            settings.state = "playing"
    elif settings.state == "select":
        settings.state = levelSelect.draw()
        if settings.state == "playing":
            level = Level(settings.levels[settings.levelIndex], screen, settings)
    elif settings.state == "highscoreselect":
        settings.state = highScoreLevel.draw()
        if settings.state == "highscore":
            highScore = HighScore(screen, settings, settings.levelIndex)
    elif settings.state == "highscore":
        settings.state = highScore.draw()
    elif settings.state == "main_menu":
        settings.state = startMenu.draw()
        settingMenu.updateState("main_menu")
    elif settings.state == "settings" and not settings.pause:
        settings.state = settingMenu.draw()
    elif settings.state == "settings" and settings.pause:
        level.draw()
        settings.state = settingMenu.draw()
    elif settings.state == "next_level":
        settings.state = "playing"
        settings.levelIndex += 1
        if settings.levelIndex >= len(settings.levels):
            settings.levelIndex = 0
            settings.state = "main_menu"
            settings.gameMusic.stop()
            settings.menuMusic.play(-1, 0, 200)
            print("No more levels, loading main menu")
        else:
            print("Loading next level: (level %s)" % str(int(settings.levelIndex) + 1))
        level = Level(settings.levels[settings.levelIndex], screen, settings)
    screen.blit(update_fps(), (settings.screen_w - 20, 0))
    screen.blit(settings.font.render(settings.name, True, pygame.Color("coral")), (100, 0))
    clock.tick(60)
    pygame.display.update()
