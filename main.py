import pygame, sys

import settings
from settings import *
from level import Level
from pygame.locals import *
from mainMenu import MainMenu
from settingMenu import SettingsMenu

clock = pygame.time.Clock()
pygame.init()
screen = pygame.display.set_mode((settings.screen_w, settings.screen_h))
settings = Settings()
startMenu = MainMenu(screen, settings)
settingMenu = SettingsMenu(screen, settings)
level = Level(settings.levels[settings.levelIndex], screen, settings)
font = pygame.font.SysFont("Arial", 18)
pause = False
state = "main_menu"

def update_fps():
    fps = str(int(clock.get_fps()))
    fps_text = font.render(fps, True, pygame.Color("coral"))
    return fps_text


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or state == "exit_to_desktop":
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE and state == "playing":
                pause = not pause
    if state == "playing":
        state = level.draw(pause)
    elif state == "main_menu":
        state = startMenu.draw()
        startMenu.state = "main_menu"
    elif state == "settings":
        state = settingMenu.draw()
        settingMenu.state = "settings"
    elif state == "finish":
        state = "playing"
        settings.levelIndex += 1
        if settings.levelIndex >= len(settings.levels):
            settings.levelIndex = 0
            state = "main_menu"
            settings.gameMusic.stop()
            settings.menuMusic.play(-1, 0, 2000)
            print("No more levels, loading main menu")
        else:
            print("Loading next level: (level %s)" % str(int(settings.levelIndex)+1))
        level = Level(settings.levels[settings.levelIndex], screen, settings)
    screen.blit(update_fps(), (10, 0))
    clock.tick(60)
    pygame.display.update()
