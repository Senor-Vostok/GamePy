import pygame


class Ground(pygame.sprite.Sprite):
    def __init__(self, image, xoy):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect(center=xoy)

    def update(self, move, y_n):
        if y_n:
            self.rect.y += move[1]
            self.rect.x += move[0]
