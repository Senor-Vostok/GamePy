import pygame


class Resource(pygame.sprite.Sprite):
    def __init__(self, xoy, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.start = xoy
        self.rect = self.image.get_rect(center=xoy)

        self.drop_second = 0
        self.drop_speed = 5
        self.drop_move = 20
        self.drop_delta = 1
        self.animation = True

    def drop_animation(self):
        if self.animation:
            self.drop_second += 1
            if self.drop_speed == self.drop_second:
                self.rect.y -= self.drop_move
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

    def update(self, move, y_n):
        self.drop_animation()
        if y_n:
            self.rect.y += move[1]
            self.rect.x += move[0]