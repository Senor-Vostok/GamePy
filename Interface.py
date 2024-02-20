import pygame


class Classic(pygame.sprite.Sprite):
    def __init__(self, xoy, image, name):
        pygame.sprite.Sprite.__init__(self)
        self.myname_is = str(name)
        self.image = image
        self.rect = self.image.get_rect(center=xoy)

    def do_some(self):
        pass

    def update(self, move=(0, 0)):
        self.rect.x += move[0]
        self.rect.y += move[1]


class Hotbar(Classic):
    def __init__(self, xoy, image, name):
        pygame.sprite.Sprite.__init__(self)
        self.myname_is = name
        self.image = image
        self.rect = self.image.get_rect(center=xoy)
        self.is_free = True
        self.i_have = None
        self.count = 0


class Interface:
    def __init__(self, size_window):
        self.size_window = size_window
        self.image_hotbar = pygame.image.load('data/Interface/hotbar.png').convert_alpha()
        self.image_quit = pygame.image.load('data/Interface/quit.png').convert_alpha()
        self.image_label = pygame.image.load('data/Interface/interface_label.png').convert_alpha()
        self.image_craftbook = pygame.image.load('data/Interface/craft_book.png').convert_alpha()
        self.font = pygame.font.SysFont('Futura book C', 30)

        self.countbar = 12
        self.sizebar = 72
        self.hotbar = pygame.sprite.Group()

        self.sizecraft_book = 272
        self.craft_book = pygame.sprite.Group()

        start = self.size_window[0] - 2 * self.sizecraft_book

        start = self.size_window[0] - ((self.countbar - 1) / 2) * self.sizebar
        for i in range(self.countbar):
            self.hotbar.add(Hotbar((start + i * self.sizebar, self.size_window[1] * 2 - 50), self.image_hotbar, f'hotbar{i}'))
        self.hotbar.add(Classic((50, 50), self.image_quit, 'quit'))

    def show_craftbook(self):
        pass

    def where_is_take(self, name=None, flag=False, image=None):
        for i in self.hotbar:
            if 'hotbar' in i.myname_is:
                if i.is_free or i.i_have == name:
                    if flag and not i.i_have:
                        i.is_free = False
                        i.i_have = name
                        i.count += 1
                        self.hotbar.add(Classic((i.rect[0] + 40, i.rect[1] + 40), image, 'resource'))
                        self.hotbar.add(Classic((i.rect[0] + 40, i.rect[1] + 60), self.font.render(f'{i.count}', False, (255, 255, 255)), i.myname_is[-1]))
                    elif i.i_have and flag:
                        for text in self.hotbar:
                            if text.myname_is in i.myname_is and text.myname_is != i.myname_is:
                                i.count += 1
                                text.image = self.font.render(f'{i.count}', False, (255, 255, 255))
                                break
                    return i.rect[0], i.rect[1]

    def gethotbar(self):
        return self.hotbar
