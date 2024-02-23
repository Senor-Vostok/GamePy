import random
import pygame
from Sprites_class import Tree, Stone
from Ground_class import Ground
from Characters import MCharacter
from Effects import Effect
from Resources import Resource
import Interface


class World:
    def __init__(self, win, centre, cord, bioms, obj):
        self.import_textures()

        # import crafts
        file = open('data/crafters_crafts/crafts.txt', mode='rt').read().split('\n')
        self.crafts = list()
        for i in file:
            if i:
                self.crafts.append([(i.split('<>'))[0], (i.split('<>'))[1], ((i.split(':'))[1]).split(';')])
        self.craft_number = 0
        self.inventory = dict()

        self.priority = ['sand', 'water', 'flower', 'forest', 'stone', 'snow']  # Приоритеты текстур

        self.obj = obj[0]
        self.sel_obj = obj[1]

        self.bioms = bioms
        self.gr_main = 180
        self.sq1 = centre[0] * 2 // self.gr_main + 3 if centre[0] * 2 // self.gr_main % 2 == 0 else centre[0] * 2 // self.gr_main + 2
        self.sq2 = centre[1] * 2 // self.gr_main + 5 if centre[1] * 2 // self.gr_main % 2 == 0 else centre[1] * 2 // self.gr_main + 4

        self.win = win

        self.centre = centre
        self.global_centre = [centre[0], centre[1]]

        self.start_dr = [self.centre[0] - self.gr_main // 2 - (self.sq1 // 2) * self.gr_main,
                         self.centre[1] - self.gr_main // 2 - (self.sq2 // 2) * self.gr_main]
        self.now_dr = [self.centre[0] - self.gr_main // 2 - (self.sq1 // 2) * self.gr_main,
                       self.centre[1] - self.gr_main // 2 - (self.sq2 // 2) * self.gr_main]
        self.move_barrier = (70, 50)

        self.great_world = [[None for _ in range(self.sq1)] for _ in range(self.sq2)]
        self.land_object = [[None for _ in range(self.sq1)] for _ in range(self.sq2)]

        self.resources_on_world = list()
        self.effects = list()

        self.world_cord = cord

        self.character = MCharacter((self.centre[0], self.centre[1] - 60))

        self.interface = Interface.Interface(self.centre, self.resources, self.inventory)

        self.synchronous = 0  # Синхронизация анимации связных объектов

    def create(self, stor='static'):
        first_block = [self.now_dr[0] - self.world_cord[1] * self.gr_main,
                       self.now_dr[1] - self.world_cord[0] * self.gr_main]
        if stor == 'up':
            self.great_world = self.great_world[:-1]
            self.great_world.insert(0, [None for _ in range(self.sq1)])
            self.land_object = self.land_object[:-1]
            self.land_object.insert(0, [None for _ in range(self.sq1)])
            for i in range(self.sq1):
                self.add_ground(0, i, self.bioms[self.world_cord[0]][self.world_cord[1] + i])
                for obj in self.obj[self.world_cord[0]][self.world_cord[1] + i]:
                    self.add_object(0, i, obj, first_block)
        elif stor == 'down':
            self.great_world = self.great_world[1:]
            self.great_world.insert(self.sq1, [None for _ in range(self.sq1)])
            self.land_object = self.land_object[1:]
            self.land_object.insert(self.sq1, [None for _ in range(self.sq1)])
            for i in range(self.sq1):
                self.add_ground(self.sq2 - 1, i, self.bioms[self.world_cord[0] + self.sq2 - 1][self.world_cord[1] + i])
                for obj in self.obj[self.world_cord[0] + self.sq2 - 1][self.world_cord[1] + i]:
                    self.add_object(self.sq2 - 1, i, obj, first_block)
        elif stor == 'left':
            for i in range(self.sq2):
                self.great_world[i] = self.great_world[i][:-1]
                self.great_world[i].insert(0, None)
                self.land_object[i] = self.land_object[i][:-1]
                self.land_object[i].insert(0, None)
            for i in range(self.sq2):
                self.add_ground(i, 0, self.bioms[self.world_cord[0] + i][self.world_cord[1]])
                for obj in self.obj[self.world_cord[0] + i][self.world_cord[1]]:
                    self.add_object(i, 0, obj, first_block)
        elif stor == 'right':
            for i in range(self.sq2):
                self.great_world[i] = self.great_world[i][1:]
                self.great_world[i].insert(self.sq1 - 1, None)
                self.land_object[i] = self.land_object[i][1:]
                self.land_object[i].insert(self.sq1 - 1, None)
            for i in range(self.sq2):
                self.add_ground(i, self.sq1 - 1, self.bioms[self.world_cord[0] + i][self.world_cord[1] + self.sq1 - 1])
                for obj in self.obj[self.world_cord[0] + i][self.world_cord[1] + self.sq1 - 1]:
                    self.add_object(i, self.sq1 - 1, obj, first_block)
        else:
            for i in range(self.sq2):
                for j in range(self.sq1):
                    self.add_ground(i, j, self.bioms[self.world_cord[0] + i][self.world_cord[1] + j])
            for i in range(self.world_cord[0], self.world_cord[0] + self.sq2):
                for j in range(self.world_cord[1], self.world_cord[1] + self.sq1):
                    for obj in self.obj[i][j]:
                        self.add_object(i - self.world_cord[0], j - self.world_cord[1], obj, first_block)

    def draw(self, move=(0, 0), way='stay', open_some=False):
        flag2 = True
        if self.global_centre[0] - self.move_barrier[0] < self.character.get_cord()[0] - move[0] < self.global_centre[0] + self.move_barrier[0] and \
                self.global_centre[1] - self.move_barrier[1] < self.character.get_cord()[1] - move[1] < self.global_centre[1] + self.move_barrier[1]:
            flag2 = False
        self.centre = self.character.get_cord()
        flag = self.check_barrier(move, self.centre)
        sorted_by_priority = list()
        for i in range(len(self.great_world)):
            for j in range(len(self.great_world[i])):
                self.great_world[i][j].update(self.synchronous, move, flag and flag2 and not open_some)
                sorted_by_priority.append(self.great_world[i][j])
        self.update_object(move, way, flag, flag2, open_some)
        for i in sorted(sorted_by_priority, key=lambda x: self.priority.index(x.name)):
            i.draw(self.win)
        self.synchronous = self.synchronous + 1 if self.synchronous < 1000000 else 0
        list_object = list()
        for i in range(len(self.land_object)):
            for j in range(len(self.land_object[i])):
                if self.land_object[i][j]:
                    if self.check_destroy_object(i, j):
                        continue
                    self.land_object[i][j].update(move, flag and flag2 and not open_some)
                    list_object.append(self.land_object[i][j])
        self.show_object([self.character] + self.effects + list_object + self.resources_on_world)
        sprites = self.my_font.render(f'sprites: {len(self.effects) + len(self.resources_on_world) + len(list_object) + self.sq1 * self.sq2}', False, (255 if len(self.effects) > 50 else 0, 255 if len(self.effects) <= 50 else 0, 0))
        self.interface.interface.draw(self.win)
        if open_some:
            self.interface.show_craftbook(self.win, self.crafts[self.craft_number])
        #self.check_barrier(move, self.centre)
        self.win.blit(sprites, (20, 160))
        #pygame.draw.rect(self.win, (255, 0, 0), (self.global_centre[0] - self.move_barrier[0], self.global_centre[1] - self.move_barrier[1], self.move_barrier[0] * 2, self.move_barrier[1] * 2), 5)

    def import_textures(self):
        self.my_font = pygame.font.SysFont('Futura book C', 30)
        # Effects
        self.effect_break_tree = [pygame.image.load(f'data/effects/tree_effects/break/break{i}.png').convert_alpha() for
                                  i in range(1, 8)]
        self.effect_break_stone = [pygame.image.load(f'data/effects/stone_effects/break/break{i}.png').convert_alpha()
                                   for i in range(1, 8)]
        self.massive_destroy_effects = {'tree': self.effect_break_tree, 'stone': self.effect_break_stone}

        # Animations
        self.water_animation = [pygame.image.load(f'data/animations/water_animations/wave{i}.png').convert_alpha() for i
                                in range(1, 5)]
        self.tree_animation = [pygame.image.load(f'data/animations/tree_animations/shake{i}.png').convert_alpha() for i
                               in range(1, 8)]

        # Resources
        self.resources = {'wood': pygame.image.load('data/resources/wood.png').convert_alpha(),
                          'stone': pygame.image.load('data/resources/stone.png').convert_alpha(),
                          'test': pygame.image.load('data/resources/test.png').convert_alpha()}

        self.transcriptions = {'tree': 'wood', 'stone': 'stone'}

        # Textures world
        self.land = {'flower': pygame.image.load('data/ground/grass.png').convert_alpha(),
                     'forest': pygame.image.load('data/ground/forest.png').convert_alpha(),
                     'water': pygame.image.load('data/ground/water.png').convert_alpha(),
                     'stone': pygame.image.load('data/ground/stone.png').convert_alpha(),
                     'sand': pygame.image.load('data/ground/sand.png').convert_alpha(),
                     'snow': pygame.image.load('data/ground/snow.png').convert_alpha(),
                     'barrier': pygame.image.load('data/ground/barrier.png').convert_alpha(),
                     'grass_sand': pygame.image.load('data/ground/grass_sand.png').convert_alpha()}

        self.images = {'tree': pygame.image.load('data/objects/tree.png').convert_alpha(),
                       'stone': pygame.image.load('data/objects/stone.png').convert_alpha(),
                       'stone_pink': pygame.image.load('data/objects/stone_pink.png').convert_alpha(),
                       'stone_white': pygame.image.load('data/objects/stone_white.png').convert_alpha()}

    def move_scene(self):
        if max(self.now_dr[0], self.start_dr[0]) - min(self.now_dr[0], self.start_dr[0]) > self.gr_main:
            res = self.now_dr[0] > self.start_dr[0]
            self.now_dr[0] = self.now_dr[0] - self.gr_main if res else self.now_dr[0] + self.gr_main
            if res:
                self.world_cord[1] = self.world_cord[1] - 1 if self.world_cord[1] >= 1 else None
                self.create('left')
            else:
                self.world_cord[1] += 1
                self.create('right')
        elif max(self.now_dr[1], self.start_dr[1]) - min(self.now_dr[1], self.start_dr[1]) > self.gr_main:
            res = self.now_dr[1] > self.start_dr[1]
            self.now_dr[1] = self.now_dr[1] - self.gr_main if res else self.now_dr[1] + self.gr_main
            if res:
                self.world_cord[0] = self.world_cord[0] - 1 if self.world_cord[0] >= 1 else None
                self.create('up')
            else:
                self.world_cord[0] += 1
                self.create('down')

    def check_barrier(self, move, point):
        for i in range(self.sq2 // 2 - 1, self.sq2 // 2 + 2):
            for obj in self.land_object[i]:
                if obj:
                    coord = obj.get_cord()
                    col = obj.colision
                    if coord[1] - col[1][0] < point[1] - move[1] < coord[1] + col[1][1] and coord[0] - col[0][0] < point[0] - move[0] < coord[0] + col[0][1]:
                        return False

            for j in range(self.sq1 // 2 - 1, self.sq1 // 2 + 2):
                res = self.now_dr[0] + j * self.gr_main < point[0] - move[0] < self.now_dr[0] + j * self.gr_main + self.gr_main and \
                      self.now_dr[1] + i * self.gr_main < point[1] - move[1] < self.now_dr[1] + i * self.gr_main + self.gr_main
                pygame.draw.rect(self.win, (0, 0, 255), (self.now_dr[0] + j * self.gr_main, self.now_dr[1] + i * self.gr_main, self.gr_main, self.gr_main), 5)
                if res:
                    if self.bioms[self.world_cord[0] + i][self.world_cord[1] + j] == 'water':
                        return False
        return True

    def show_object(self, sprites):
        massive_sprites = list()
        for sprite in sprites:
            if sprite:
                massive_sprites.append(sprite)
        massive_sprites = sorted(massive_sprites, key=lambda x: x.get_cord()[1])
        for obj in massive_sprites:
            obj.draw(self.win)

    def check_destroy_object(self, i, j):
        if self.land_object[i][j].hp == 0:
            coord = self.land_object[i][j].get_cord()
            name_res = self.transcriptions[self.land_object[i][j].name]
            self.resources_on_world += [Resource((coord[0], coord[1] + random.randint(-20, 20)), self.resources[name_res], name_res) for _ in range(random.randint(2, 4))]
            self.land_object[i][j] = None
            self.obj[self.world_cord[0] + i][self.world_cord[1] + j] = [(0, 0), 'None']
            return True
        return False

    def update_object(self, move, way, flag, flag2, open_some):
        if flag and flag2 and not open_some:
            self.now_dr[0] = self.great_world[0][0].rect[0] + 10
            self.now_dr[1] = self.great_world[0][0].rect[1] + 10
            self.move_scene()
        if flag and not flag2 and not open_some:
            self.character.update(way, move)
        else:
            self.character.update(way, [0, 0])

        deleted = list()
        for i in range(len(self.effects)):
            is_playing = self.effects[i].update(move, flag and flag2)
            if not is_playing:
                deleted.append(self.effects[i])
        for d in deleted:
            self.effects.remove(d)

        deleted = list()
        for res in self.resources_on_world:
            result = res.update(move, flag and flag2 and not open_some, self.centre, self.interface.where_is_take(res.name))
            if result:
                self.interface.where_is_take(res.name, True, res.image)
                deleted.append(res)
        for d in deleted:
            self.resources_on_world.remove(d)

    def craft_resource(self):
        buf = self.interface.craft_book[8]
        new_resource = Resource((buf.rect[0] + 40, buf.rect[1] - 130), buf.image, buf.name)
        new_resource.takes = True
        self.resources_on_world.append(new_resource)

    def select(self, there, pressed=False):
        if pressed:
            for u in self.interface.craft_book:
                if u.rect.colliderect(there[0], there[1], 1, 1) and u.name == 'button_craft' and self.interface.can_craft(self.crafts[self.craft_number]):
                    self.interface.decrease_resources(self.crafts[self.craft_number])
                    self.craft_resource()
            for obj_interface in self.interface.interface:
                if obj_interface.rect.colliderect(there[0], there[1], 1, 1):
                    obj_interface.do_some()
                    return obj_interface.name
            for i in range(len(self.land_object) - 1, 0, -1):
                for obj in self.land_object[i]:
                    if obj and obj.get_cord()[0] in range(self.centre[0] - self.gr_main - self.gr_main // 2, self.centre[0] + self.gr_main) and \
                            obj.get_cord()[1] in range(self.centre[1] - self.gr_main - self.gr_main // 2, self.centre[1] + self.gr_main):
                        if obj.press(there):
                            obj.is_shake = True
                            self.effects.append(Effect(there, self.massive_destroy_effects[obj.name], True))
                            return
        else:
            for u in self.interface.craft_book:
                try:
                    u.do_some(u.rect.colliderect(there[0], there[1], 1, 1))
                except Exception:
                    pass

    def add_ground(self, i, j, biom):
        if biom == 'water':
            sprite = Ground(self.land[biom], (
                self.now_dr[0] + j * self.gr_main + self.gr_main // 2,
                self.now_dr[1] + i * self.gr_main + self.gr_main // 2), 'water', self.water_animation)
        else:
            sprite = Ground(self.land[biom], (
                self.now_dr[0] + j * self.gr_main + self.gr_main // 2,
                self.now_dr[1] + i * self.gr_main + self.gr_main // 2), biom)
        self.great_world[i][j] = sprite

    def add_object(self, i, j, obj, first_block):
        if obj[1] == 'tree':
            self.land_object[i][j] = Tree(first_block, obj, self.tree_animation, self.images[obj[1]])
        elif obj[1] == 'stone' or obj[1] == 'stone_pink' or obj[1] == 'stone_white':
            self.land_object[i][j] = Stone(first_block, obj, self.tree_animation, self.images[obj[1]])
