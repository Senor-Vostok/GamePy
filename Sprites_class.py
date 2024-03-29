import random
import pygame


class ClassicClass(pygame.sprite.Sprite):
    def __init__(self, first_block, obj, animation, image):
        pygame.sprite.Sprite.__init__(self)
        self.sel = False

        self.classic_image = image
        self.image = image
        self.xoy = (first_block[0] + obj[0][0], first_block[1] + obj[0][1])
        self.colision = [(0, 0), (0, 0)]
        self.rect = self.image.get_rect(center=self.xoy)
        self.hp = 1

        self.random_start_animation = 10000

        self.name = 'sprite'

        self.is_shake = False
        self.shake_second = 0
        self.shake_speed = 5
        self.shake_temp = 1

        self.is_animated = False
        self.animation = animation
        self.second_animation = 0
        self.speed_animation = 40

    def shake(self):
        if self.is_shake:
            self.shake_second += self.shake_temp
            if self.shake_second == self.shake_speed:
                self.shake_temp = -1
                self.rect.x += 8
            elif self.shake_second == -self.shake_speed:
                self.shake_temp = 1
                self.rect.x -= 16
            elif self.shake_second == 0 and self.shake_temp == 1:
                self.hp -= 1
                self.shake_temp = 1
                self.rect.x += 8
                self.is_shake = False

    def press(self, there):
        return self.rect.colliderect(there[0], there[1], 1, 1)

    def self_animation(self, stadia):
        self.image = self.animation[stadia - 1]

    def get_cord(self):
        return self.rect.x, self.rect.y

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def update(self, move, y_n):
        self.shake()

        if not self.is_animated:
            self.is_animated = random.randint(1, self.random_start_animation) == 1
        else:
            self.second_animation += 1
            stadia = self.second_animation // self.speed_animation + 1
            if stadia <= len(self.animation):
                self.self_animation(stadia)
            else:
                self.image = self.classic_image
                self.second_animation = 0
                self.is_animated = False

        if y_n:
            self.rect.y += move[1]
            self.rect.x += move[0]


class Tree(ClassicClass):
    def __init__(self, first_block, obj, animation, image):
        pygame.sprite.Sprite.__init__(self)
        self.sel = False
        self.classic_image = image
        self.image = image
        self.xoy = (first_block[0] + obj[0][0], first_block[1] + obj[0][1] - 160)
        self.colision = [(50, 40), (0, 10)]  # относительное смещение по x и по y для проверки пересечения в точке
        self.rect = self.image.get_rect(center=self.xoy)
        self.hp = 10
        self.random_start_animation = 10000
        self.name = 'tree'
        self.is_shake = False
        self.shake_second = 0
        self.shake_speed = 10
        self.shake_temp = 1
        self.is_animated = False
        self.animation = animation
        self.second_animation = 0
        self.speed_animation = 40

    def get_cord(self):
        return self.rect.x + 90, self.rect.y + 320


class Stone(ClassicClass):
    def __init__(self, first_block, obj, animation, image):
        pygame.sprite.Sprite.__init__(self)
        self.sel = False
        self.classic_image = image
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

    def get_cord(self):
        return self.rect.x + 90, self.rect.y + 140

    def update(self, move, y_n):
        self.shake()
        if y_n:
            self.rect.y += move[1]
            self.rect.x += move[0]

