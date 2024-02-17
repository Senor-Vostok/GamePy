import random
import pygame


class Stone(pygame.sprite.Sprite):
    def __init__(self, first_block, obj, animation):
        pygame.sprite.Sprite.__init__(self)
        self.sel = False
        self.image = pygame.image.load('data/objects/stone.png').convert_alpha()
        self.xoy = (first_block[0] + obj[0][0], first_block[1] + obj[0][1] - 20)
        self.colision = [(80, 80), (40, 20)]  # относительное смещение по x и по y для проверки пересечения в точке
        self.rect = self.image.get_rect(center=self.xoy)

        self.is_animated = False
        self.animation = animation
        self.second_animation = 0
        self.speed_animation = 30

    def self_animation(self, stadia):
        self.image = self.animation[stadia - 1]

    def iscolision(self):
        return self.colision

    def get_cord(self):
        return self.rect.x + 90, self.rect.y + 120

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def update(self, move, y_n):
        if y_n:
            self.rect.y += move[1]
            self.rect.x += move[0]
