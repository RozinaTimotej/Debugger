import math
import pygame
from tiles import Tla, Finish,Tile, Coin
from player import Player
from enemy import Enemy, FlyingEnemy, KamikazeEnemy
from background import Background1, Background2
from math import atan2, degrees, pi,sqrt
from bullet import Bullet
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
        self.flyingEnemies= pygame.sprite.Group()
        self.kamikazeEnemy = pygame.sprite.Group()
        self.finish = pygame.sprite.GroupSingle()
        self.space = pygame.sprite.Group()
        self.stars = pygame.sprite.Group()
        self.enemyBlocks = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()
        for r_i, row in enumerate(layout):
            for c_i, col in enumerate(row):
                col_split = col.split("_")
                for char in col_split:
                    if char == 'p':
                        self.player.add(Player((c_i * self.settings.tile_size, r_i * self.settings.tile_size),self.settings,self.settings.playerFrames))
                    if char == 'h1':
                        self.enemies.add(Enemy((c_i * self.settings.tile_size, r_i * self.settings.tile_size),self.settings, self.settings.enemyFrames))
                    if char == 't1':
                        self.tiles.add(Tla(self.settings.tile_size, c_i * self.settings.tile_size, r_i * self.settings.tile_size, self.settings.tile[char[1]],self.settings))
                    if char == 'td':
                        self.topDieTiles.add(Tla(self.settings.tile_size, c_i * self.settings.tile_size, r_i * self.settings.tile_size, self.settings.tile[char[1]],self.settings))
                    if char == 'e':
                        self.finish.add(Finish(self.settings.tile_size, c_i * self.settings.tile_size, r_i * self.settings.tile_size, self.settings.finish, self.settings))
                    if char == 'iw':
                        self.enemyBlocks.add(Tile(self.settings.tile_size, c_i * self.settings.tile_size, r_i * self.settings.tile_size, self.settings))
                    if char == 'h2':
                        self.flyingEnemies.add(FlyingEnemy((c_i * self.settings.tile_size, r_i * self.settings.tile_size), self.settings,self.settings.enemyFlyFrames))
                    if char == 'h3':
                        self.kamikazeEnemy.add(KamikazeEnemy((c_i * self.settings.tile_size+16, r_i * self.settings.tile_size+32), self.settings,self.settings.kamikazeEnemyFrames))
                    if char == 'c':
                        self.coins.add(Coin(c_i * self.settings.tile_size, r_i * self.settings.tile_size, self.settings.coin, self.settings))

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
            if enemy.rect.colliderect(player.rect) and enemy.state == "alive":
                if enemy.direction.x < 0 or enemy.direction.x > 0:
                    self.init_level(self.data)
                break
            for sprite in self.enemyBlocks.sprites():
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

    def h_col_flyingEnemy(self):
        player = self.player.sprite
        for enemy in self.flyingEnemies.sprites():
            enemy.rect.x += enemy.direction.x * enemy.speed

        for enemy in self.flyingEnemies.sprites():
            if enemy.rect.colliderect(player.rect) and enemy.state == "alive":
                if enemy.direction.x < 0 or enemy.direction.x > 0:
                    self.init_level(self.data)
                break
            for sprite in self.enemyBlocks.sprites():
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
        self.h_col_flyingEnemy()
        self.h_col_kamikaze()

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
            if enemy.rect.colliderect(self.player.sprite.rect) and enemy.state == "alive":
                if self.player.sprite.direction.y > 0:
                    pygame.mixer.Sound.play(self.settings.hitEnemy)
                    enemy.death()
                    player.direction.y = player.jumpHeight / 2

    def v_col_flyingEnemy(self):
        player = self.player.sprite
        for enemy in self.flyingEnemies.sprites():
            if enemy.rect.colliderect(self.player.sprite.rect) and enemy.state == "alive":
                if self.player.sprite.direction.y > 0:
                    pygame.mixer.Sound.play(self.settings.hitEnemy)
                    enemy.death()
                    player.direction.y = player.jumpHeight / 2

    def h_col_kamikaze(self):
        player = self.player.sprite
        for enemy in self.kamikazeEnemy.sprites():
            if not enemy.state == "super_dead":
                enemy.h_move()
                if enemy.rect.colliderect(player.rect) and enemy.state == "attack":
                    enemy.death("super_dead")
                    self.init_level(self.data)
                    break
                for sprite in self.tiles.sprites():
                    if enemy.state == "dead":
                        enemy.rect.y += 1
                        if sprite.rect.colliderect(enemy.rect):
                            enemy.rect.bottom = sprite.rect.top
                            enemy.state = "super_dead"
                    if sprite.rect.colliderect(enemy.rect) and enemy.state == "attack":
                        enemy.death("dead")

    def v_col_plain(self):  # collisioni za gor/dol in pa logika za skok
        self.v_col_player()
        self.v_col_enemy()
        self.v_col_flyingEnemy()
        self.v_col_kamikaze()


    def check_Enemies(self):
        for enemy in self.enemies.sprites():
            if enemy.state == "dead":
                self.enemies.remove(enemy)

    def check_FlyingEnemies(self):
        for enemy in self.flyingEnemies.sprites():
            if enemy.state == "dead":
                self.flyingEnemies.remove(enemy)
            if enemy.dir_i == "fly":
                dx = self.player.sprite.rect.x+20 - enemy.rect.x
                dy = self.player.sprite.rect.y+32 - enemy.rect.y
                dist = (dx ** 2 + dy ** 2) ** .5
                rads = atan2(-dy, dx)
                rads %= 2 * pi
                degs = degrees(rads)
                if enemy.facing_right and 300 < degs < 360 and dist < 250:
                    self.bullets.add(Bullet((enemy.rect.x+64,enemy.rect.y+32), self.settings,self.settings.bulletFrames,enemy.facing_right, pygame.time.get_ticks()))
                    enemy.shoot()
                elif (not enemy.facing_right) and 180 < degs < 240 and dist < 250:
                    self.bullets.add(Bullet((enemy.rect.x-32, enemy.rect.y+32), self.settings, self.settings.bulletFrames,enemy.facing_right,pygame.time.get_ticks()))
                    enemy.shoot()

    def check_KamikazeEnemies(self):
        player = self.player.sprite.rect
        for enemy in self.kamikazeEnemy.sprites():
            if enemy.state == "remove":
                self.kamikazeEnemy.remove(enemy)
            if enemy.dir_i == "stand":
                dx = self.player.sprite.rect.x + 20 - enemy.rect.x
                dy = self.player.sprite.rect.y + 32 - enemy.rect.y
                dist = (dx ** 2 + dy ** 2) ** .5
                if dist < 150:
                    enemy.shoot()
                elif dist < 150:
                    enemy.shoot()
            if enemy.state == "locate_enemy":
                enemy.kamikaze(player.x+player.width/2, player.y+player.height/2)

    def bullets_update(self):
        for bullet in self.bullets.sprites():
            if bullet.state == "dead":
                self.bullets.remove(bullet)
            bullet.updateDest(self.player.sprite.rect.x, self.player.sprite.rect.y)

    def bullet_Col(self):
        player = self.player.sprite
        for bullet in self.bullets.sprites():
            dx = player.rect.x+20 - bullet.rect.x
            dy = player.rect.y+32 - bullet.rect.y
            dist = (dx ** 2 + dy ** 2) ** .5
            if not dist == 0:
                dx /= dist
                dy /= dist
            move_distx = min(self.player.sprite.speed * 1.1, int(dist))
            move_disty = min(self.player.sprite.speed*0.8, int(dist))
            bullet.rect.x += move_distx * dx
            bullet.rect.y += move_disty * dy
            for sprite in self.tiles.sprites():
                if sprite.rect.colliderect(bullet.rect) and bullet.state == "alive":
                    bullet.death()
            if bullet.rect.colliderect(player.rect) and bullet.state == "alive":
                bullet.death()
                self.init_level(self.data)

    def v_col_kamikaze(self):
        player = self.player.sprite
        for enemy in self.kamikazeEnemy.sprites():
            if not enemy.state == "super_dead":
                enemy.v_move()
                if enemy.rect.colliderect(player.rect) and enemy.state == "attack":
                    enemy.death("super_dead")
                    self.init_level(self.data)
                    break
                for sprite in self.tiles.sprites():
                    if sprite.rect.colliderect(enemy.rect) and enemy.state == "attack":
                        enemy.death("super_dead")
    def draw(self):
        if not self.settings.pause:
            self.h_col_plain()
            self.v_col_plain()
            self.check_Enemies()
            self.check_FlyingEnemies()
            self.check_KamikazeEnemies()
            self.bullets_update()
            self.bullet_Col()
            self.space.update(self.move)
            self.stars.update(self.move)
            self.tiles.update(self.move)
            self.enemyBlocks.update(self.move)
            self.topDieTiles.update(self.move)
            self.finish.update(self.move)
            self.bullets.update(self.move)
            self.enemies.update(self.move)
            self.flyingEnemies.update(self.move)
            self.kamikazeEnemy.update(self.move)
            self.coins.update(self.move)
            self.player.update()

        self.cam()
        self.space.draw(self.display_surface)
        self.stars.draw(self.display_surface)
        self.enemies.draw(self.display_surface)
        self.flyingEnemies.draw(self.display_surface)
        self.kamikazeEnemy.draw(self.display_surface)
        self.tiles.draw(self.display_surface)
        self.topDieTiles.draw(self.display_surface)
        self.finish.draw(self.display_surface)
        self.coins.draw(self.display_surface)
        self.bullets.draw(self.display_surface)
        self.player.draw(self.display_surface)

        return self.status
