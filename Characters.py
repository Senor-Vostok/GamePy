import pygame


class MCharacter(pygame.sprite.Sprite):  # поверить работу!
    def __init__(self, xoy):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('data/character/stay.png').convert_alpha()
        self.rect = self.image.get_rect(center=xoy)

    def get_cord(self):
        return [self.rect.x + 45, self.rect.y + 120]

    def update(self, action, move):
        self.image = pygame.image.load(f'data/character/{action}.png').convert_alpha()
        self.rect.y -= move[1]
        self.rect.x -= move[0]

