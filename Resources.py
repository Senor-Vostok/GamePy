import random
import pygame


class Resource(pygame.sprite.Sprite):
    def __init__(self, xoy, image, name, flag=True):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.name = name
        self.start = xoy
        self.rect = self.image.get_rect(center=xoy)

        self.drop_second = 0
        self.drop_speed = 3
        self.drop_move = 25
        self.drop_delta = 1
        self.animation = flag

        self.take_cake = 20
        self.takes = False
        self.deviation = random.randint(-10, 11)

    def take(self, move):
        if not self.animation and self.take_cake != 0:
            vector = ((move[0] - self.rect.x) / self.take_cake, (move[1] - self.rect.y) / self.take_cake)
            self.rect.x += vector[0]
            self.rect.y += vector[1]
            self.take_cake -= 1
            return False
        if self.take_cake == 0:
            return True
        return False

    def drop_animation(self):
        if self.animation:
            self.drop_second += 1
            if self.drop_speed == self.drop_second:
                self.rect.y -= self.drop_move
                self.rect.x -= self.deviation
                self.drop_move -= self.drop_delta
                self.drop_delta += 1
                self.drop_second = 0
            if self.rect.y > self.start[1]:
                self.rect.y += self.drop_move
                self.animation = False

    def get_cord(self):
        return self.rect

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def update(self, move, y_n, character_cord, move_there=None):
        res = False
        self.drop_animation()
        if move_there and (self.rect.colliderect(character_cord[0], character_cord[1], 1, 1) or self.takes):
            self.takes = True
            res = self.take(move_there)
        if y_n:
            self.rect.y += move[1]
            self.rect.x += move[0]
        return res
