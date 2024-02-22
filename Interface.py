import pygame
from Resources import Resource


class Classic(pygame.sprite.Sprite):
    def __init__(self, xoy, image, name):
        pygame.sprite.Sprite.__init__(self)
        self.name = str(name)
        self.image = image
        self.rect = self.image.get_rect(center=xoy)
        self.rect_cr = (self.rect[0] + 50, self.rect[1] + 50)

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def do_some(self, *args):
        pass

    def update(self, move=(0, 0)):
        self.rect.x += move[0]
        self.rect.y += move[1]


class Hotbar(Classic):
    def __init__(self, xoy, image, name):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.image = image
        self.rect = self.image.get_rect(center=xoy)
        self.is_free = True
        self.i_have = None
        self.count = 0
        self.image_resource = None
        self.text = None


class Buttoncraft(Classic):
    def __init__(self, xoy, image, name, active_passive):
        pygame.sprite.Sprite.__init__(self)
        self.name = str(name)
        self.image = image
        self.rect = self.image.get_rect(center=xoy)
        self.rect_cr = (self.rect[0] + 50, self.rect[1] + 50)
        self.images = active_passive

    def do_some(self, change=False):
        if change:
            self.image = self.images[0]
        else:
            self.image = self.images[1]


class Interface:
    def __init__(self, size_window, image_resources, inventory):
        self.size_window = size_window
        self.inventory = inventory
        self.image_hotbar = pygame.image.load('data/Interface/hotbar.png').convert_alpha()
        self.image_quit = pygame.image.load('data/Interface/quit.png').convert_alpha()

        self.image_crafter = pygame.image.load('data/Interface/crafter.png').convert_alpha()
        self.crafter_close = pygame.image.load('data/Interface/bar_crafter-close.png').convert_alpha()
        self.crafter_open = pygame.image.load('data/Interface/bar_crafter-open.png').convert_alpha()
        self.get_crafte = pygame.image.load('data/Interface/get_craft.png').convert_alpha()
        self.get_crafta = pygame.image.load('data/Interface/get_craft-active.png').convert_alpha()

        self.font = pygame.font.SysFont('Futura book C', 30)
        self.resources = image_resources

        self.countbar = 12
        self.sizebar = 72
        self.interface = pygame.sprite.Group()

        self.craft_book = list()
        self.last_craft = -1

        start = self.size_window[0] - ((self.countbar - 1) / 2) * self.sizebar
        for i in range(self.countbar):
            self.interface.add(Hotbar((start + i * self.sizebar, self.size_window[1] * 2 - 50), self.image_hotbar, f'hotbar{i}'))
        self.interface.add(Classic((50, 50), self.image_quit, 'quit'))

        self.craft_book.append(Classic((400, 540), self.image_crafter, 'crafter_label'))
        for i in range(7):
            if i == 0:
                self.craft_book.append(Classic((400, 240 + i * 100), self.crafter_open, 'crafter_main'))
                continue
            if i == 1:
                self.craft_book.append(Buttoncraft((400, 240 + i * 100), self.get_crafte, 'button_craft', [self.get_crafta, self.get_crafte]))
                continue
            self.craft_book.append(Classic((400, 240 + i * 100), self.crafter_close, 'crafter_component'))

    def update_craft(self, craft):
        c = craft[0].split('_')
        self.craft_book.append(Resource((self.craft_book[1].rect_cr[0], self.craft_book[1].rect_cr[1]), self.resources[c[0]], c[0], False))
        self.craft_book.append(Classic((self.craft_book[1].rect_cr[0], self.craft_book[1].rect_cr[1] + 30), self.font.render(f'{c[1]}', False, (255, 255, 255)), 'count'))
        if craft[1] == 'unlock':
            self.craft_book[1].image = self.crafter_open
        else:
            self.craft_book[1].image = self.crafter_close
        for i in range(len(craft[2])):
            c = craft[2][i].split('_')
            self.craft_book.append(Classic((self.craft_book[3 + i].rect_cr[0], self.craft_book[3 + i].rect_cr[1]), self.resources[c[0]], c[0]))
            self.craft_book.append(Classic((self.craft_book[3 + i].rect_cr[0], self.craft_book[3 + i].rect_cr[1] + 30), self.font.render(f'{c[1]}', False, (255, 255, 255)), 'count'))
            if c[0] in self.inventory and self.inventory[c[0]] >= int(c[1]):
                self.craft_book[3 + i].image = self.crafter_open
            else:
                self.craft_book[3 + i].image = self.crafter_close

    def can_craft(self, craft):
        for i in craft[2]:
            resource = i.split('_')
            if resource[0] in self.inventory and self.inventory[resource[0]] < int(resource[1]):
                return False
            elif resource[0] not in self.inventory:
                return False
        return True

    def decrease_resources(self, craft):
        decrease = {i.split('_')[0]: int(i.split('_')[1]) for i in craft[2]}
        for i in self.interface:
            if 'hotbar' in i.name:
                if i.i_have in decrease:
                    self.inventory[i.i_have] -= decrease[i.i_have]
                    i.count -= decrease[i.i_have]
                    if i.count == 0:
                        i.is_free = True
                        i.i_have = None
                        i.text.kill()
                        i.image_resource.kill()
                    else:
                        i.text.image = self.font.render(f'{i.count}', False, (255, 255, 255))

    def show_craftbook(self, surface, craft):
        self.craft_book = self.craft_book[:8]
        self.update_craft(craft)
        for i in self.craft_book:
            i.draw(surface)

    def where_is_take(self, name=None, flag=False, image=None):
        for i in self.interface:
            if 'hotbar' in i.name:
                if i.is_free or i.i_have == name:
                    if flag and not i.i_have:
                        i.is_free = False
                        i.i_have = name
                        i.count += 1
                        i.text = Classic((i.rect[0] + 40, i.rect[1] + 60), self.font.render(f'{i.count}', False, (255, 255, 255)), i.name[-1])
                        i.image_resource = Classic((i.rect[0] + 40, i.rect[1] + 40), image, 'resource')
                        self.inventory[i.i_have] = 1
                        self.interface.add(i.image_resource)
                        self.interface.add(i.text)
                    elif i.i_have and flag:
                        for text in self.interface:
                            if text.name in i.name and text.name != i.name:
                                i.count += 1
                                self.inventory[i.i_have] += 1
                                text.image = self.font.render(f'{i.count}', False, (255, 255, 255))
                                break
                    return i.rect[0], i.rect[1]
