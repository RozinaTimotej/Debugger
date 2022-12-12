import pygame, sys

import settings
from settings import *
from level import Level
from pygame.locals import *
from mainMenu import MainMenu, PauseMenu
from settingMenu import SettingsMenu

clock = pygame.time.Clock()
pygame.init()
screen = pygame.display.set_mode((settings.screen_w, settings.screen_h))
settings = Settings()
settingMenu = SettingsMenu(screen, settings)
startMenu = MainMenu(screen, settings,settingMenu)
pauseMenu = PauseMenu(screen, settings,settingMenu)
level = Level(settings.levels[settings.levelIndex], screen, settings)
font = pygame.font.SysFont("Arial", 18)

def update_fps():
    fps = str(int(clock.get_fps()))
    fps_text = font.render(fps, True, pygame.Color("coral"))
    return fps_text


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or settings.state == "exit_to_desktop":
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE and (settings.state == "playing" or settings.state == "pause_menu"):
                settings.pause = not settings.pause
    if settings.state == "playing" or settings.state == "pause_menu":
        settings.state = level.draw()
        if settings.pause:
            settings.state = pauseMenu.draw()
            settingMenu.updateState("pause_menu")
            pauseMenu.state = "pause_menu"
    elif settings.state == "main_menu":
        settings.state = startMenu.draw()
        settingMenu.updateState("main_menu")
        startMenu.state = "main_menu"
    elif settings.state == "settings" and not settings.pause:
        screen.fill("black")
        settings.state = settingMenu.draw()
        settingMenu.state = "settings"
    elif settings.state == "settings" and settings.pause:
        settings.state = level.draw()
        settings.state = settingMenu.draw()
        settingMenu.state = "settings"
    elif settings.state == "finish":
        settings.state = "playing"
        settings.levelIndex += 1
        if settings.levelIndex >= len(settings.levels):
            settings.levelIndex = 0
            settings.state = "main_menu"
            settings.gameMusic.stop()
            settings.menuMusic.play(-1, 0, 2000)
            print("No more levels, loading main menu")
        else:
            print("Loading next level: (level %s)" % str(int(settings.levelIndex)+1))
        level = Level(settings.levels[settings.levelIndex], screen, settings)
    screen.blit(update_fps(), (10, 0))
    clock.tick(60)
    pygame.display.update()
