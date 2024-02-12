import pygame


class MCharacter(pygame.sprite.Sprite):  # поверить работу!
    def __init__(self, xoy):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('data/character/stay.png').convert_alpha()
        self.rect = self.image.get_rect(center=(900, 540))

    def update(self, action):
        self.image = pygame.image.load(f'data/character/{action}.png').convert_alpha()
        self.rect = self.image.get_rect(center=(900, 540))

