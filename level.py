import copy
import random
import pygame
from tiles import Tla, Finish
from settings import tile_size, screen_w
from player import Player


class Level:
    def __init__(self, data, surface):
        self.display_surface = surface
        self.init_level(data)
        self.move = 0

    def init_level(self, layout):
        self.tiles = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        self.finish = pygame.sprite.GroupSingle()
        for r_i, row in enumerate(layout):
            for c_i, col in enumerate(row):
                if col == 'p':
                    self.player.add(Player((c_i * tile_size, r_i * tile_size)))
                if col == 'f':
                    self.tiles.add(Tla(tile_size, c_i * tile_size, r_i * tile_size, str(random.randint(0, 4))))
                if col == 'e':
                    self.finish.add(Finish(tile_size, c_i * tile_size, r_i * tile_size, "0"))

    def cam(self):
        player = self.player.sprite
        if player.rect.centerx > (3 * screen_w / 4) and player.direction.x > 0:
            self.move = -player.speedInfo
            player.speed = 0
        elif player.rect.centerx < (screen_w / 4) and player.direction.x < 0:
            self.move = player.speedInfo
            player.speed = 0
        else:
            self.move = 0
            player.speed = player.speedInfo

    def h_col(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    if player.jumps > 0 and not player.wall_jumped:
                        player.direction.y = 0
                        player.on_wall = True
                    player.rect.left = sprite.rect.right
                elif player.direction.x > 0:
                    if player.jumps > 0 and not player.wall_jumped:
                        player.direction.y = 0
                        player.on_wall = True
                    player.rect.right = sprite.rect.left

    def v_col(self):
        player = self.player.sprite
        player.set_gravity()
        if player.rect.y <= 0:
            player.direction.y = 0
            player.rect.top = 0

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.jumps = 0
                    player.on_wall = False
                    player.wall_jumped = False
                elif player.direction.y < 0:
                    player.direction.y = 0
                    player.rect.top = sprite.rect.bottom

    def draw(self):
        self.tiles.update(self.move)
        self.finish.update(self.move)
        self.tiles.draw(self.display_surface)
        self.finish.draw(self.display_surface)
        self.cam()

        self.player.update()
        self.h_col()
        self.v_col()
        self.player.draw(self.display_surface)
