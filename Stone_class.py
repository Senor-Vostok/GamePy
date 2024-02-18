import pygame


class Stone(pygame.sprite.Sprite):
    def __init__(self, first_block, obj, animation, image):
        pygame.sprite.Sprite.__init__(self)
        self.sel = False
        self.image = image
        self.xoy = (first_block[0] + obj[0][0], first_block[1] + obj[0][1] - 20)
        self.colision = [(90, 80), (20, 25)]  # относительное смещение по x и по y для проверки пересечения в точке
        self.rect = self.image.get_rect(center=self.xoy)
        self.hp = 10

        self.name = 'stone'
        self.is_shake = False
        self.shake_second = 0
        self.shake_speed = 10
        self.shake_temp = 1

        self.is_animated = False
        self.animation = animation
        self.second_animation = 0
        self.speed_animation = 30

    def get_hp(self):
        return self.hp

    def shake_start(self):
        self.is_shake = True

    def shake(self):
        if self.is_shake:
            self.shake_second += self.shake_temp
            if self.shake_second == self.shake_speed:
                self.shake_temp = -1
                self.rect.x += 10
            elif self.shake_second == -self.shake_speed:
                self.shake_temp = 1
                self.rect.x -= 20
            elif self.shake_second == 0 and self.shake_temp == 1:
                self.shake_temp = 1
                self.rect.x += 10
                self.is_shake = False

    def press(self, there):
        return self.rect.colliderect(there[0], there[1], 1, 1)

    def myname(self):
        return self.name

    def self_animation(self, stadia):
        self.image = self.animation[stadia - 1]

    def iscolision(self):
        return self.colision

    def get_cord(self):
        return self.rect.x + 90, self.rect.y + 140

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def update(self, move, y_n):
        if y_n:
            self.rect.y += move[1]
            self.rect.x += move[0]
