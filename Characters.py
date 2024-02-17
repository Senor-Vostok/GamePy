import pygame


class MCharacter(pygame.sprite.Sprite):  # поверить работу!
    def __init__(self, xoy):
        pygame.sprite.Sprite.__init__(self)
        self.animation_left_move = [pygame.image.load(f'data/character/move/move_left{i}.png').convert_alpha() for i in range(1, 5)]
        self.animation_right_move = [pygame.image.load(f'data/character/move/move_right{i}.png').convert_alpha() for i in range(1, 5)]
        self.animation_forward_move = [pygame.image.load(f'data/character/move/move_forward{i}.png').convert_alpha() for i in range(1, 5)]
        self.animation_stay = pygame.image.load('data/character/stay.png').convert_alpha()
        self.animation_stay_right = pygame.image.load('data/character/stay_right.png').convert_alpha()
        self.image = self.animation_stay
        self.rect = self.image.get_rect(center=xoy)

        self.action = 'stay'
        self.second_animation = 0
        self.speed_animation = 15

    def animation(self, action):
        if action != self.action:
            self.second_animation = 0

        self.second_animation += 1
        stadia = self.second_animation // self.speed_animation
        if stadia > 3:
            self.second_animation = 0
            stadia = 0

        if action == 'left':
            self.image = self.animation_left_move[stadia]
            self.action = action
        elif action == 'right':
            self.image = self.animation_right_move[stadia]
            self.action = action
        elif action == 'back':
            self.image = self.animation_forward_move[stadia]
            self.action = action
        else:
            if self.action == 'right' or self.action == 'back':
                self.image = self.animation_stay_right
            else:
                self.image = self.animation_stay

    def get_cord(self):
        return [self.rect.x + 45, self.rect.y + 190]

    def update(self, action, move):
        self.animation(action)
        self.rect.y -= move[1]
        self.rect.x -= move[0]

