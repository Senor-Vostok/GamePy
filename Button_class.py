import pygame


class Button(pygame.sprite.Sprite):
    def __init__(self, xoy, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect(center=xoy)

    def update(self):
        pass
