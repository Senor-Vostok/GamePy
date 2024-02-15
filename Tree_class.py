import random

import pygame


class Tree(pygame.sprite.Sprite):
    def __init__(self, first_block, obj, animation):
        pygame.sprite.Sprite.__init__(self)
        self.sel = False
        self.image = pygame.image.load('data/objects/tree.png').convert_alpha()
        self.xoy = (first_block[0] + obj[0][0], first_block[1] + obj[0][1] - 100)
        self.colision = [(30, 50), (0, 20)]  # относительное смещение по x и по y для проверки пересечения в точке
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
        return self.rect.x + 90, self.rect.y + 140

    def select(self):
        if not self.sel:
            self.image = pygame.image.load('data/objects/tree_select.png').convert_alpha()
            self.sel = True
        else:
            self.image = pygame.image.load('data/objects/tree.png').convert_alpha()
            self.sel = False

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def update(self, move, y_n):
        if not self.is_animated:
            self.is_animated = random.randint(1, 10000) == 1
        else:
            self.second_animation += 1
            stadia = self.second_animation // self.speed_animation + 1
            if stadia <= len(self.animation):
                self.self_animation(stadia)
            else:
                self.second_animation = 0
                self.is_animated = False

        if y_n:
            self.rect.y += move[1]
            self.rect.x += move[0]
