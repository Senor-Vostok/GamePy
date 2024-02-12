import pygame


class Tree(pygame.sprite.Sprite):
    def __init__(self, first_block, obj):
        pygame.sprite.Sprite.__init__(self)
        self.sel = False
        self.image = pygame.image.load('data/objects/tree.png').convert_alpha()
        self.xoy = (first_block[0] + obj[0][0], first_block[1] + obj[0][1] - 100)
        self.rect = self.image.get_rect(center=self.xoy)

    def get_cord(self):
        return (self.rect.x + 90, self.rect.y + 140)

    def select(self):
        print(self.get_cord())
        if not self.sel:
            self.image = pygame.image.load('data/objects/tree_select.png').convert_alpha()
            self.sel = True
        else:
            self.image = pygame.image.load('data/objects/tree.png').convert_alpha()
            self.sel = False

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def update(self, move, y_n):
        if not y_n:
            self.rect.y += move[1]
            self.rect.x += move[0]
