import pygame


class Tile(pygame.sprite.Sprite):
    def __init__(self, size, x, y):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self, move):
        self.rect.x += move


class StaticTile(Tile):
    def __init__(self, size, x, y, surface):
        super().__init__(size, x, y)
        self.image = surface


class Tla(StaticTile):
    def __init__(self, size, x, y, id):
        super().__init__(size, x, y, pygame.image.load('../Assets/tla/sprite_' + id + '.png').convert_alpha())
        offset_y = y + size
        self.rect = self.image.get_rect(bottomleft=(x, offset_y))


class Finish(StaticTile):
    def __init__(self, size, x, y, id):
        super().__init__(size, x, y, pygame.image.load('../Assets/finish/sprite_' + id + '.png').convert_alpha())
        offset_y = y + size
        self.rect = self.image.get_rect(bottomleft=(x, offset_y))
