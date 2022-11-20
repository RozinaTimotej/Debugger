import pygame, sys
from settings import *
from level import Level
from pygame.locals import *
pygame.init()
screen = pygame.display.set_mode((screen_w, screen_h))
clock = pygame.time.Clock()
level = Level(map, screen)
font = pygame.font.SysFont("Arial", 18)
pause = False
state = "main_menu"

def update_fps():
    fps = str(int(clock.get_fps()))
    fps_text = font.render(fps, 1, pygame.Color("coral"))
    return fps_text

state = "playing"

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE and state == "playing":
                pause = not pause

    screen.fill('blue')
    level.draw(pause)
    screen.blit(update_fps(), (10, 0))
    clock.tick(60)
    pygame.display.update()
