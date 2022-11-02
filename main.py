import pygame, sys
from settings import *
from level import Level

pygame.init()
screen = pygame.display.set_mode((screen_w, screen_h))
clock = pygame.time.Clock()
level = Level(map, screen)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill('blue')
    level.draw()
    pygame.display.update()
    clock.tick(60)
