import pygame
from tiles import Tla,Finish
from settings import tile_size
from player import Player

class Level:
    def __init__(self, data, surface):
        self.display_surface = surface
        self.init_level(data)
        self.move = 0

    def init_level(self, layout):
        self.tiles = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()

        for r_i, row in enumerate(layout):
            for c_i, col in enumerate(row):
                if col == 'p':
                    self.player.add(Player((c_i*tile_size, r_i * tile_size)))
                if col == 'f1':
                    self.tiles.add(Tla(tile_size, c_i * tile_size, r_i * tile_size, "1"))
                if col == 'f0':
                    self.tiles.add(Tla(tile_size, c_i * tile_size, r_i * tile_size,"0"))
                if col == 'e':
                    self.tiles.add(Finish(tile_size, c_i * tile_size, r_i * tile_size, "0"))

    def draw(self):
        self.tiles.update(self.move)
        self.player.update()
        self.player.draw(self.display_surface)
        self.tiles.draw(self.display_surface)
