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

class Start(pygame.sprite.Sprite):
    def __init__(self, x, y, surface):
        super().__init__()
        self.image = surface
        offset_y = y + self.image.get_height()
        self.rect = self.image.get_rect(bottomleft=(x, offset_y))

class Coin(pygame.sprite.Sprite):
    def __init__(self, x,y, frames, settings):
        super().__init__()
        self.settings = settings
        self.frames = frames
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(topleft=(x+(64-20)/2,y+(64-20)/2))
        self.animMult = 6

    def update(self, move):
        self.rect.x += move

        self.frame_index += 0.02 * self.animMult
        if self.frame_index >= len(self.frames):
            self.frame_index = 0

        self.image = self.frames[int(self.frame_index)]
