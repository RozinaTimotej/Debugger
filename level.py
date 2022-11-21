import copy
import math
import random
import sys

import pygame
from tiles import Tla, Finish
from settings import tile_size, screen_w
from player import Player
from enemy import Enemy
from background import Background1, Background2

class Level:
    def __init__(self, data, surface):
        self.display_surface = surface
        self.data = data
        self.init_level(data)
        self.move = 0
        self.hitEnemy = pygame.mixer.Sound("./Assets/sounds/hit_enemy.wav")
        pygame.mixer.Sound.set_volume(self.hitEnemy, 0.1)

    def init_level(self, layout): #gre čez level in ga naloži
        self.tiles = pygame.sprite.Group()
        self.topDieTiles = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        self.enemies = pygame.sprite.Group()
        self.finish = pygame.sprite.GroupSingle()
        self.space = pygame.sprite.Group()
        self.stars = pygame.sprite.Group()

        for r_i, row in enumerate(layout):
            for c_i, col in enumerate(row):
                if col == 'p':
                    self.player.add(Player((c_i * tile_size, r_i * tile_size)))
                    player_x = c_i
                if col == 'h':
                    self.enemies.add(Enemy((c_i * tile_size, r_i * tile_size)))
                if col == 'f':
                    self.tiles.add(Tla(tile_size, c_i * tile_size, r_i * tile_size, "2"))
                if col == 'f1':
                    self.topDieTiles.add(Tla(tile_size, c_i * tile_size, r_i * tile_size, "2"))
                if col == 'e':
                    self.finish.add(Finish(tile_size, c_i * tile_size, r_i * tile_size, "0"))

        len_x = math.ceil((screen_w+screen_w/4)/1367)+1
        for i in range(-1,len_x+1):
            self.space.add(Background1(i*1367-screen_w/2,0))
        for i in range(-1, len_x+1):
            self.stars.add(Background2(i * 1367 - screen_w / 2, 0))

    def cam(self): #ce je igralec znotraj 2 in 3 četrtine se kamera ne premika, drugače se
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

    def h_col_player(self):
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
                break

        for sprite in self.topDieTiles.sprites():
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
                break

    def h_col_enemy(self):
        player = self.player.sprite
        for enemy in self.enemies.sprites():
            enemy.rect.x += enemy.direction.x * enemy.speed

        for enemy in self.enemies.sprites():
            if enemy.rect.colliderect(player.rect):
                if enemy.direction.x < 0 or enemy.direction.x > 0:
                    self.init_level(self.data)
                break
            for sprite in self.tiles.sprites():
                if sprite.rect.colliderect(enemy.rect):
                    if enemy.direction.x < 0:
                        enemy.rect.left = sprite.rect.right
                        enemy.direction.x = 1
                        enemy.facing_right = True
                    elif enemy.direction.x > 0:
                        enemy.direction.x = -1
                        enemy.facing_right = False
                        enemy.rect.right = sprite.rect.left
                    break
    def h_col_plain(self): #collisioni za levo/desno in pa logika za držanje stene
       self.h_col_player()
       self.h_col_enemy()

    def v_col_player(self):
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
                break

        for sprite in self.topDieTiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.jumps = 0
                    player.on_wall = False
                    player.wall_jumped = False
                    self.init_level(self.data)
                elif player.direction.y < 0:
                    player.direction.y = 0
                    player.rect.top = sprite.rect.bottom
                break

    def v_col_enemy(self):
        player = self.player.sprite
        for enemy in self.enemies.sprites():
            if enemy.rect.colliderect(self.player.sprite.rect):
                if self.player.sprite.direction.y > 0:
                    pygame.mixer.Sound.play(self.hitEnemy)
                    self.enemies.remove(enemy)
                    player.direction.y = player.jumpHeight/2

    def v_col_plain(self): #collisioni za gor/dol in pa logika za skok
        self.v_col_player()
        self.v_col_enemy()

    def draw(self,pause):
        self.space.draw(self.display_surface)
        self.stars.draw(self.display_surface)
        self.tiles.draw(self.display_surface)
        self.topDieTiles.draw(self.display_surface)
        self.finish.draw(self.display_surface)
        self.cam()
        self.enemies.draw(self.display_surface)
        self.player.draw(self.display_surface)
        if not pause:
            self.h_col_plain()
            self.v_col_plain()
            self.space.update(self.move)
            self.stars.update(self.move)
            self.tiles.update(self.move)
            self.topDieTiles.update(self.move)
            self.finish.update(self.move)
            self.enemies.update(self.move)
            self.player.update()

