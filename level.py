import math
import pygame
from tiles import Tla, Finish,Tile, Coin, Start
from player import Player
from enemy import Enemy, FlyingEnemy, KamikazeEnemy
from background import Background1, Background2
from math import atan2, degrees, pi,ceil
from bullet import Bullet
from spike import Spike
class Level:
    def __init__(self, data, surface, settings):
        self.display_surface = surface
        self.settings = settings
        self.data = data
        self.init_level(data)
        self.uniTime = 0
        self.time = 0
        self.startTime = 0
        self.move = 0
        self.started = False
        self.status = "playing"

    def updateTime(self):
        self.time = (pygame.time.get_ticks() - self.startTime)/1000
    def drawTime(self):
        return self.settings.font.render("{:0.2f}".format(self.time+self.uniTime), True, pygame.Color("coral"))

    def starts(self):
        self.started = True
        self.startTime = pygame.time.get_ticks()
        self.uniTime = 0
        self.time = 0
        pygame.sprite.Group.empty(self.start)
    def updateStartTime(self):
        self.uniTime += self.time
        self.startTime = pygame.time.get_ticks()
    def init_level(self, layout):  # gre čez level in ga naloži
        self.tiles = pygame.sprite.Group()
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
        self.spikes = pygame.sprite.Group()
        self.start = pygame.sprite.GroupSingle()

        self.start.add(Start(self.settings.screen_w/2 - self.settings.start.get_width()/2,self.settings.screen_h - self.settings.screen_h/3,self.settings.start))

        x_offset = self.settings.screen_w / 3 - 20
        for r_i, row in enumerate(layout):
            for c_i, col in enumerate(row):
                col_split = col.split("_")
                for char in col_split:
                    if char == 'p':
                        x_offset -= c_i * self.settings.tile_size
                        break
        for r_i, row in enumerate(layout):
            for c_i, col in enumerate(row):
                col_split = col.split("_")
                for char in col_split:
                    if char == 'p':
                        self.player.add(Player((c_i * self.settings.tile_size + x_offset, r_i * self.settings.tile_size),self.settings,self.settings.playerFrames))
                    if char == 'h1':
                        self.enemies.add(Enemy((c_i * self.settings.tile_size + x_offset, r_i * self.settings.tile_size),self.settings, self.settings.enemyFrames))
                    if char == 't1':
                        self.tiles.add(Tla(ceil(self.settings.tile_size), ceil(c_i * self.settings.tile_size) + x_offset, ceil(r_i * self.settings.tile_size), self.settings.tile[char[1]],self.settings))
                    if char == 'e':
                        self.finish.add(Finish(self.settings.tile_size, c_i * self.settings.tile_size + x_offset, r_i * self.settings.tile_size, self.settings.finish, self.settings))
                    if char == 'iw':
                        self.enemyBlocks.add(Tile(self.settings.tile_size, c_i * self.settings.tile_size + x_offset, r_i * self.settings.tile_size, self.settings))
                    if char == 'h2':
                        self.flyingEnemies.add(FlyingEnemy((c_i * self.settings.tile_size + x_offset, r_i * self.settings.tile_size), self.settings,self.settings.enemyFlyFrames))
                    if char == 'h3':
                        self.kamikazeEnemy.add(KamikazeEnemy((c_i * self.settings.tile_size+(16*self.settings.screen_mul) + x_offset, r_i * self.settings.tile_size+(32*self.settings.screen_mul)), self.settings,self.settings.kamikazeEnemyFrames))
                    if char == 'c':
                        self.coins.add(Coin(c_i * self.settings.tile_size + x_offset, r_i * self.settings.tile_size, self.settings.coin, self.settings))
                    if char == 's':
                        if r_i < len(layout)-1 and "t1" in layout[r_i+1][c_i].split("_"):
                            self.spikes.add(Spike((c_i * self.settings.tile_size + (16*self.settings.screen_mul) + x_offset, r_i * self.settings.tile_size + (40*self.settings.screen_mul)), self.settings, self.settings.spikeFrames,0))
                        elif c_i < len(row)-1 and "t1" in layout[r_i][c_i+1].split("_"):
                            self.spikes.add(Spike((c_i * self.settings.tile_size + (40*self.settings.screen_mul) + x_offset, r_i * self.settings.tile_size + (20*self.settings.screen_mul)),self.settings, self.settings.spikeFrames,90))
                        elif c_i > 0 and "t1" in layout[r_i][c_i-1].split("_"):
                            self.spikes.add(Spike((c_i * self.settings.tile_size + 0 + x_offset, r_i * self.settings.tile_size + (20*self.settings.screen_mul)),self.settings, self.settings.spikeFrames,270))
                        elif r_i > 0 and "t1" in layout[r_i-1][c_i].split("_"):
                            self.spikes.add(
                                Spike((c_i * self.settings.tile_size + (16*self.settings.screen_mul) + x_offset, r_i * self.settings.tile_size + 0),self.settings, self.settings.spikeFrames, 180))

        self.space.add(Background1(0, 0,self.settings))
        self.space.add(Background2(0, 0, self.settings))

        self.startTime = pygame.time.get_ticks()

    def cam(self):  # ce je igralec znotraj 2 in 3 četrtine se kamera ne premika, drugače se
        player = self.player.sprite
        if player.rect.right > (3 * self.settings.screen_w / 4) and player.direction.x > 0:
            self.move = -player.speedInfo
            player.speed = 0
        elif player.rect.left < (self.settings.screen_w / 4) and player.direction.x < 0:
            self.move = player.speedInfo
            player.speed = 0
        else:
            self.move = 0
            player.speed = player.speedInfo

    def h_col_player(self):
        player = self.player.sprite
        dist = 0
        if self.move == 0:
            player.rect.x += player.direction.x * player.speed
            for sprite in self.tiles.sprites():
                if player.rect.colliderect(sprite.rect):
                    if player.direction.x < 0:
                        if player.jumps > 0 and not player.wall_jumped:
                            dist = player.rect.top - sprite.rect.top
                        player.rect.left = sprite.rect.right+1
                    elif player.direction.x > 0:
                        if player.jumps > 0 and not player.wall_jumped:
                            dist = player.rect.top - sprite.rect.top
                        player.rect.right = sprite.rect.left-1
                    break
        else:
            for sprite in self.tiles.sprites():
                sprite.rect.x += self.move
                if player.rect.colliderect(sprite.rect):
                    if player.direction.x < 0:
                        player.rect.left = sprite.rect.right + 1
                    elif player.direction.x > 0:
                        player.rect.right = sprite.rect.left - 1


        if dist > 0:
            player.direction.y = 0
            player.on_wall = True
        for sprite in self.finish.sprites():
            if pygame.sprite.collide_mask(player,sprite):
                self.status = "finish_menu"
                self.settings.pause = True
                self.settings.score = self.time+self.uniTime
                break

        for coin in self.coins.sprites():
            if pygame.sprite.collide_mask(player,coin):
                self.coins.remove(coin)
                self.uniTime -= 2.5
                pygame.mixer.Sound.play(self.settings.coinSound, 0)

    def h_col_enemy(self):
        player = self.player.sprite
        for enemy in self.enemies.sprites():
            enemy.x += enemy.direction.x * enemy.speed
            enemy.rect.x = enemy.x

        for enemy in self.enemies.sprites():
            if pygame.sprite.collide_mask(player,enemy) and enemy.state == "alive":
                if enemy.direction.x < 0 or enemy.direction.x > 0:
                    self.die()
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
            enemy.x += enemy.direction.x * enemy.speed
            enemy.rect.x = enemy.x

        for enemy in self.flyingEnemies.sprites():
            if pygame.sprite.collide_mask(player,enemy) and enemy.state == "alive":
                if enemy.direction.x < 0 or enemy.direction.x > 0:
                    self.die()
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
            return

        if player.rect.y > self.settings.screen_h*1.2:
            self.die()
            return

        for sprite in self.tiles.sprites():
            if player.rect.colliderect(sprite.rect):
                if player.direction.y > 0:
                    player.direction.y = 0
                    if player.jumps > 0:
                        player.soundDelay = 0
                    player.jumps = 0
                    player.on_wall = False
                    player.wall_jumped = False
                    if sprite.rect.top - player.rect.bottom < 15:
                        player.rect.bottom = sprite.rect.top
                elif player.direction.y < 0:
                    player.direction.y = 0
                    if sprite.rect.bottom - player.rect.top < 15:
                        player.rect.top = sprite.rect.bottom

    def v_col_enemy(self):
        player = self.player.sprite
        for enemy in self.enemies.sprites():
            if enemy.rect.colliderect(self.player.sprite.rect) and enemy.state == "alive":
                if self.player.sprite.direction.y > 0:
                    pygame.mixer.Sound.play(self.settings.hitEnemy)
                    enemy.death()
                    player.direction.y = player.jumpHeight / 2
                    break

    def v_col_flyingEnemy(self):
        player = self.player.sprite
        for enemy in self.flyingEnemies.sprites():
            if enemy.rect.colliderect(self.player.sprite.rect) and enemy.state == "alive":
                if self.player.sprite.direction.y > 0:
                    pygame.mixer.Sound.play(self.settings.hitEnemy)
                    enemy.death()
                    player.direction.y = player.jumpHeight / 2
                    break

    def h_col_kamikaze(self):
        player = self.player.sprite
        for enemy in self.kamikazeEnemy.sprites():
            if not enemy.state == "super_dead":
                enemy.h_move()
                if pygame.sprite.collide_mask(player,enemy) and enemy.state == "attack":
                    enemy.death("super_dead")
                    self.die()
                    break
                for sprite in self.tiles.sprites():
                    if enemy.state == "dead":
                        enemy.rect.y += 1
                        if sprite.rect.colliderect(enemy.rect):
                            enemy.rect.bottom = sprite.rect.top
                            enemy.state = "super_dead"
                            break
                    if sprite.rect.colliderect(enemy.rect) and enemy.state == "attack":
                        if enemy.dx > 0:
                            enemy.rect.right = sprite.rect.left
                        else:
                            enemy.rect.left = sprite.rect.right
                        enemy.death("dead")
                        break

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
            if enemy.state == "super_dead" and pygame.time.get_ticks() - enemy.tod > 5000:
                enemy.state = "alive"
                enemy.dir_i = "stand"
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
            dx = (player.rect.x+(player.rect.width/2)) - bullet.rect.x
            dy = (player.rect.y+(player.rect.height/2)) - bullet.rect.y
            dist = (dx ** 2 + dy ** 2) ** .5
            if not dist == 0:
                dx /= dist
                dy /= dist
            move_distx = self.player.sprite.speedInfo*1.2
            move_disty = self.player.sprite.speedInfo*1.2
            bullet.rect.x += move_distx * dx
            bullet.rect.y += move_disty * dy
            for sprite in self.tiles.sprites():
                if sprite.rect.colliderect(bullet.rect) and bullet.state == "alive":
                    bullet.death()
                    break
            if pygame.sprite.collide_mask(player,bullet) and bullet.state == "alive":
                bullet.death()
                self.die()

    def v_col_kamikaze(self):
        player = self.player.sprite
        for enemy in self.kamikazeEnemy.sprites():
            if not enemy.state == "super_dead":
                enemy.v_move()
                if pygame.sprite.collide_mask(player,enemy) and enemy.state == "attack":
                    enemy.death("super_dead")
                    self.die()
                    break
                for sprite in self.tiles.sprites():
                    if sprite.rect.colliderect(enemy.rect) and enemy.state == "attack":
                        enemy.death("super_dead")
                        break
    def col(self):
        player = self.player.sprite
        for sprite in self.spikes.sprites():
            if pygame.sprite.collide_mask(player,sprite) and sprite.deadly:
                self.die()
                break
    def die(self):
        self.status = "die_menu"
        self.settings.pause = True
        pygame.mixer.Sound.play(self.settings.deathSound,0)
    def draw(self):
        if not self.settings.pause and self.started:
            self.updateTime()
            self.h_col_plain()
            self.v_col_plain()
            self.col()
            self.check_Enemies()
            self.check_FlyingEnemies()
            self.check_KamikazeEnemies()
            self.bullets_update()
            self.bullet_Col()
            self.space.update(self.move)
            self.stars.update(self.move)
            self.tiles.update(0)
            self.enemyBlocks.update(self.move)
            self.finish.update(self.move)
            self.bullets.update(self.move)
            self.enemies.update(self.move)
            self.flyingEnemies.update(self.move)
            self.kamikazeEnemy.update(self.move)
            self.spikes.update(self.move)
            self.coins.update(self.move)
            self.player.update()
            self.cam()

        self.space.draw(self.display_surface)
        self.stars.draw(self.display_surface)
        self.enemies.draw(self.display_surface)
        self.flyingEnemies.draw(self.display_surface)
        self.kamikazeEnemy.draw(self.display_surface)
        self.tiles.draw(self.display_surface)
        self.finish.draw(self.display_surface)
        self.coins.draw(self.display_surface)
        self.spikes.draw(self.display_surface)
        self.bullets.draw(self.display_surface)
        self.player.draw(self.display_surface)
        self.display_surface.blit(self.drawTime(), (10, 0))
        self.start.draw(self.display_surface)
        return self.status
