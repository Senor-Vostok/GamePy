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

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def update(self, synchronous, move, y_n):
        if self.name == 'water':
            stadia = (synchronous // self.speed_animation + 1) % len(self.water_animation)
            self.self_animation(stadia)

        if y_n:
            self.rect.y += move[1]
            self.rect.x += move[0]
