import pygame, sys
from settings import *
from level import Level

pygame.init()
screen = pygame.display.set_mode((screen_w, screen_h))
clock = pygame.time.Clock()
level = Level(map, screen)
font = pygame.font.SysFont("Arial", 18)


def update_fps():
    fps = str(int(clock.get_fps()))
    fps_text = font.render(fps, 1, pygame.Color("coral"))
    return fps_text


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill('blue')
    level.draw()
    screen.blit(update_fps(), (10, 0))
    clock.tick(60)
    pygame.display.update()
