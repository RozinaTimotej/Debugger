import pygame

class Tile(pygame.sprite.Sprite):
    def __init__(self, size, x, y,settings):
        super().__init__()
        self.settings = settings
        self.image = pygame.Surface((size, size))
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self, move):
        self.rect.x += move


class StaticTile(Tile):
    def __init__(self, size, x, y, surface,settings):
        super().__init__(size, x, y,settings)
        self.image = surface


class Tla(StaticTile):
    def __init__(self, size, x, y, surface, settings):
        super().__init__(size, x, y, surface, settings)
        offset_y = y + size
        self.rect = self.image.get_rect(bottomleft=(x, offset_y))


class Finish(StaticTile):
    def __init__(self, size, x, y, surface, settings):
        super().__init__(size, x, y, surface, settings)
        offset_y = y + size
        self.rect = self.image.get_rect(bottomleft=(x, offset_y))
