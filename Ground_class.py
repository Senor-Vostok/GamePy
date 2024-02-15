import pygame


class Ground(pygame.sprite.Sprite):
    def __init__(self, image, xoy, name, animation=None):
        pygame.sprite.Sprite.__init__(self)
        if name == 'water':
            self.water_animation = animation
        self.name = name
        self.image = image
        self.rect = self.image.get_rect(center=xoy)

        self.second_animation = 0
        self.speed_animation = 80

    def self_animation(self, stadia):
        self.image = self.water_animation[stadia - 1]

    def update(self, move, y_n):
        if self.name == 'water':
            self.second_animation += 1
            stadia = self.second_animation // self.speed_animation + 1
            if stadia > len(self.water_animation):
                self.second_animation = 0
                stadia = 1
            self.self_animation(stadia)

        if y_n:
            self.rect.y += move[1]
            self.rect.x += move[0]
