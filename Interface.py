import pygame


class Hotbar(pygame.sprite.Sprite):
    def __init__(self, xoy, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('data/Interface/hotbar.png').convert_alpha()
        self.rect = self.image.get_rect(center=xoy)

    def update(self, move=(0, 0)):
        self.rect.x += move[0]
        self.rect.y += move[1]


class Quit(pygame.sprite.Sprite):
    def __init__(self, xoy, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect(center=xoy)

    def update(self, move=(0, 0)):
        self.rect.x += move[0]
        self.rect.y += move[1]


class Interface:
    def __init__(self, size_window):
        self.size_window = size_window
        self.image_hotbar = pygame.image.load('data/Interface/hotbar.png').convert_alpha()
        self.image_quit = pygame.image.load('data/Interface/quit.png').convert_alpha()
        self.countbar = 12
        self.sizebar = 72
        self.interface = pygame.sprite.Group()
        start = self.size_window[0] - ((self.countbar - 1) / 2) * self.sizebar
        for i in range(self.countbar):
            self.interface.add(Hotbar((start + i * self.sizebar, self.size_window[1] * 2 - 50), self.image_hotbar))
        self.interface.add(Quit((50, 50), self.image_quit))

    def gethotbar(self):
        return self.interface
