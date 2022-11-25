import math
import pygame
from tiles import Tla, Finish
from player import Player
from enemy import Enemy
from background import Background1, Background2


class Level:
    def __init__(self, data, surface, settings):
        self.display_surface = surface
        self.settings = settings
        self.data = data
        self.init_level(data)
        self.move = 0
        self.status = "playing"

    def init_level(self, layout):  # gre čez level in ga naloži
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
                    self.player.add(Player((c_i * self.settings.tile_size, r_i * self.settings.tile_size),self.settings,self.settings.playerFrames))
                if col == 'h':
                    self.enemies.add(Enemy((c_i * self.settings.tile_size, r_i * self.settings.tile_size),self.settings, self.settings.enemyFrames))
                if col == 't1':
                    self.tiles.add(Tla(self.settings.tile_size, c_i * self.settings.tile_size, r_i * self.settings.tile_size, self.settings.tile[col[1]],self.settings))
                if col == 'td':
                    self.topDieTiles.add(Tla(self.settings.tile_size, c_i * self.settings.tile_size, r_i * self.settings.tile_size, self.settings.tile[col[1]],self.settings))
                if col == 'e':
                    self.finish.add(Finish(self.settings.tile_size, c_i * self.settings.tile_size, r_i * self.settings.tile_size, self.settings.finish, self.settings))

        len_x = math.ceil((self.settings.screen_w + self.settings.screen_w / 4) / 1367) + 1
        for i in range(-1, len_x + 1):
            self.space.add(Background1(i * 1367 - self.settings.screen_w / 2, 0,self.settings))
        for i in range(-1, len_x + 1):
            self.stars.add(Background2(i * 1367 - self.settings.screen_w / 2, 0,self.settings))

    def cam(self):  # ce je igralec znotraj 2 in 3 četrtine se kamera ne premika, drugače se
        player = self.player.sprite
        if player.rect.centerx > (3 * self.settings.screen_w / 4) and player.direction.x > 0:
            self.move = -player.speedInfo
            player.speed = 0
        elif player.rect.centerx < (self.settings.screen_w / 4) and player.direction.x < 0:
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
                    player.rect.left = sprite.rect.right+0.005
                elif player.direction.x > 0:
                    if player.jumps > 0 and not player.wall_jumped:
                        player.direction.y = 0
                        player.on_wall = True
                    player.rect.right = sprite.rect.left-0.005
                break

        for sprite in self.finish.sprites():
            if sprite.rect.colliderect(player.rect):
                self.status = "finish"
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

    def h_col_plain(self):  # collisioni za levo/desno in pa logika za držanje stene
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
                    if player.jumps > 0:
                        player.soundDelay = 0
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
                    pygame.mixer.Sound.play(self.settings.hitEnemy)
                    self.enemies.remove(enemy)
                    player.direction.y = player.jumpHeight / 2

    def v_col_plain(self):  # collisioni za gor/dol in pa logika za skok
        self.v_col_player()
        self.v_col_enemy()

    def draw(self, pause):
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

        self.space.draw(self.display_surface)
        self.stars.draw(self.display_surface)
        self.tiles.draw(self.display_surface)
        self.topDieTiles.draw(self.display_surface)
        self.finish.draw(self.display_surface)
        self.cam()
        self.enemies.draw(self.display_surface)
        self.player.draw(self.display_surface)

        return self.status
