import pygame


class Character(pygame.sprite.Sprite):  # поверить работу!
    def __init__(self, xoy):
        pygame.sprite.Sprite.__init__(self)
        self.animation_move = {'left': [pygame.image.load(f'data/character/move/move_left{i}.png').convert_alpha() for i in range(1, 5)],
                               'right': [pygame.image.load(f'data/character/move/move_right{i}.png').convert_alpha() for i in range(1, 5)],
                               'back': [pygame.image.load(f'data/character/move/move_forward{i}.png').convert_alpha() for i in range(1, 5)],
                               'forward': [pygame.image.load(f'data/character/move/move_back{i}.png').convert_alpha() for i in range(1, 5)]}
        self.animation_stay = pygame.image.load('data/character/stay.png').convert_alpha()
        self.animation_stay_right = pygame.image.load('data/character/stay_right.png').convert_alpha()
        self.image = self.animation_stay
        self.rect = self.image.get_rect(center=xoy)

        self.action = 'stay'
        self.second_animation = 0
        self.speed_animation = 15

    def event(self, move, speed, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                move[1] = speed
            if event.key == pygame.K_s:
                move[1] = -speed
            if event.key == pygame.K_a:
                move[0] = speed
            if event.key == pygame.K_d:
                move[0] = -speed
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_w or event.key == pygame.K_s:
                move[1] = 0
            if event.key == pygame.K_a or event.key == pygame.K_d:
                move[0] = 0
        return move

    def animation(self, action):
        if action != self.action:
            self.second_animation = 0

        self.second_animation += 1
        stadia = self.second_animation // self.speed_animation
        if stadia > 3:
            self.second_animation = 0
            stadia = 0

        if action in self.animation_move:
            self.image = self.animation_move[action][stadia]
            self.action = action
        else:
            if self.action == 'right' or self.action == 'forward':
                self.image = self.animation_stay_right
            else:
                self.image = self.animation_stay

    def get_cord(self):
        return self.rect.x + 45, self.rect.y + 190

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def update(self, action, move):
        self.animation(action)
        self.rect.y -= move[1]
        self.rect.x -= move[0]

