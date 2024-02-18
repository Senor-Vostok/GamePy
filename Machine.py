import pygame
from Tree_class import Tree
from Stone_class import Stone
from Ground_class import Ground
from Characters import MCharacter
from Effects import Effect
import Interface


class World:
    def __init__(self, win, centre, cord, bioms, obj, width):
        self.my_font = pygame.font.SysFont('Futura book C', 30)
        # Effects
        self.effect_break_tree = [pygame.image.load(f'data/effects/tree_effects/break/break{i}.png').convert_alpha() for
                                  i in range(1, 8)]

        # Animations
        self.water_animation = [pygame.image.load(f'data/animations/water_animations/wave{i}.png').convert_alpha() for i
                                in range(1, 5)]
        self.tree_animation = [pygame.image.load(f'data/animations/tree_animations/shake{i}.png').convert_alpha() for i
                               in range(1, 6)]

        # Textures world
        self.land = {'flower': pygame.image.load('data/ground/grass.png').convert_alpha(),
                     'forest': pygame.image.load('data/ground/forest.png').convert_alpha(),
                     'water': pygame.image.load('data/ground/water.png').convert_alpha(),
                     'stone': pygame.image.load('data/ground/stone.png').convert_alpha(),
                     'sand': pygame.image.load('data/ground/sand.png').convert_alpha()}
        self.images = {'tree': pygame.image.load('data/objects/tree.png').convert_alpha(),
                       'stone': pygame.image.load('data/objects/stone.png').convert_alpha()}

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

        self.great_world = pygame.sprite.Group()
        self.land_object = [[None for _ in range(self.sq1)] for _ in range(self.sq2)]
        self.effects = list()

        self.world_cord = cord

        self.character = pygame.sprite.Group(MCharacter((self.centre[0], self.centre[1] - 60)))

        self.interface = Interface.Interface(self.centre).gethotbar()

    def move_scene(self):
        if max(self.now_dr[0], self.start_dr[0]) - min(self.now_dr[0], self.start_dr[0]) > self.gr_main:
            res = self.now_dr[0] > self.start_dr[0]
            self.now_dr[0] = self.now_dr[0] - self.gr_main if res else self.now_dr[0] + self.gr_main
            if res:
                self.world_cord[1] = self.world_cord[1] - 1 if self.world_cord[1] >= 1 else None
                self.create_objects('left')
            else:
                self.world_cord[1] += 1
                self.create_objects('right')
            self.create_ground()
        elif max(self.now_dr[1], self.start_dr[1]) - min(self.now_dr[1], self.start_dr[1]) > self.gr_main:
            res = self.now_dr[1] > self.start_dr[1]
            self.now_dr[1] = self.now_dr[1] - self.gr_main if res else self.now_dr[1] + self.gr_main
            if res:
                self.world_cord[0] = self.world_cord[0] - 1 if self.world_cord[0] >= 1 else None
                self.create_objects('up')
            else:
                self.world_cord[0] += 1
                self.create_objects('down')
            self.create_ground()

    def check_barrier(self, move, point):
        for i in range(self.sq2 // 2 - 1, self.sq2 // 2 + 2):
            for obj in self.land_object[i]:
                if obj:
                    coord = obj.get_cord()
                    col = obj.iscolision()
                    if point[1] - move[1] in range(coord[1] - col[1][0], coord[1] + col[1][1]) and point[0] - \
                            move[0] in range(coord[0] - col[0][0], coord[0] + col[0][1]):
                        return False

            for j in range(self.sq1 // 2 - 1, self.sq1 // 2 + 2):
                res = point[0] - move[0] in range(self.now_dr[0] + j * self.gr_main,
                                                  self.now_dr[0] + j * self.gr_main + self.gr_main) and \
                      point[1] - move[1] in range(self.now_dr[1] + i * self.gr_main,
                                                  self.now_dr[1] + i * self.gr_main + self.gr_main)
                pygame.draw.rect(self.win, (0, 0, 255), (
                self.now_dr[0] + j * self.gr_main, self.now_dr[1] + i * self.gr_main, self.gr_main, self.gr_main), 5)
                if res:
                    if self.bioms[self.world_cord[0] + i][self.world_cord[1] + j] == 'water':
                        return False
        return True

    def draw(self, move=(0, 0), way='stay'):
        flag2 = False

        for character in self.character:
            if character.get_cord()[0] - move[0] not in range(self.global_centre[0] - self.move_barrier[0],
                                                              self.global_centre[0] + self.move_barrier[0]) or \
                    character.get_cord()[1] - move[1] not in range(self.global_centre[1] - self.move_barrier[1],
                                                                   self.global_centre[1] + self.move_barrier[1]):
                self.character.update(way, [0, 0])
                flag2 = True
            self.centre = character.get_cord()

        flag = self.check_barrier(move, self.centre)

        if flag2 and flag:
            self.move_scene()
            self.now_dr[0] += move[0]
            self.now_dr[1] += move[1]
        if not flag and not flag2:
            self.character.update(way, [0, 0])
        if flag and not flag2:
            self.character.update(way, move)

        deleted = list()
        for i in range(len(self.effects)):
            is_playing = self.effects[i].update(move, flag and flag2)
            if not is_playing:
                deleted.append(self.effects[i])
        for d in deleted:
            self.effects.remove(d)

        self.great_world.update(move, flag and flag2)
        self.great_world.draw(self.win)
        self.character.draw(self.win)
        for i in range(len(self.land_object)):
            for j in range(len(self.land_object[i])):
                if self.land_object[i][j]:
                    if self.land_object[i][j].get_hp() == 0:
                        self.land_object[i][j] = None
                        self.obj[self.world_cord[0] + i][self.world_cord[1] + j] = [(0, 0), 'None']
                        continue
                    self.land_object[i][j].update(move, flag and flag2)
                    self.land_object[i][j].draw(self.win)
                    coord = self.land_object[i][j].get_cord()
                    if coord[1] in range(self.centre[1] - 200, self.centre[1]) and coord[0] in range(self.centre[0] - 100, self.centre[0] + 200):
                        self.character.draw(self.win)
        for effect in self.effects:
            effect.draw(self.win)
        sprites = self.my_font.render(f'effects: {len(self.effects)}', False, (255 if len(self.effects) > 50 else 0, 255 if len(self.effects) <= 50 else 0, 0))
        self.interface.draw(self.win)
        self.win.blit(sprites, (20, 160))
        #pygame.draw.rect(self.win, (255, 0, 0), (
        #self.global_centre[0] - self.move_barrier[0], self.global_centre[1] - self.move_barrier[1],
        #self.move_barrier[0] * 2, self.move_barrier[1] * 2), 5)
        #self.check_barrier(move, self.centre)

    def select(self, there):
        for obj_interface in self.interface:
            if obj_interface.rect.colliderect(there[0], there[1], 1, 1) and obj_interface.myname() == 'quit':
                return 'quit'
        for i in range(len(self.land_object) - 1, 0, -1):
            for obj in self.land_object[i]:
                if obj and obj.get_cord()[0] in range(self.centre[0] - self.gr_main - self.gr_main // 2, self.centre[0] + self.gr_main) and \
                        obj.get_cord()[1] in range(self.centre[1] - self.gr_main - self.gr_main // 2, self.centre[1] + self.gr_main):
                    if obj.press(there) and obj.myname() == 'tree':
                        obj.shake_start()
                        self.effects.append(Effect(there, self.effect_break_tree, True))
                        return

    def create_ground(self):
        self.great_world = pygame.sprite.Group()
        for i in range(self.sq2):
            for j in range(self.sq1):
                if self.bioms[self.world_cord[0] + i][self.world_cord[1] + j] == 'water':
                    sprite = Ground(self.land[self.bioms[self.world_cord[0] + i][self.world_cord[1] + j]], (
                        self.now_dr[0] + j * self.gr_main + self.gr_main // 2,
                        self.now_dr[1] + i * self.gr_main + self.gr_main // 2), 'water', self.water_animation)
                else:
                    sprite = Ground(self.land[self.bioms[self.world_cord[0] + i][self.world_cord[1] + j]], (
                        self.now_dr[0] + j * self.gr_main + self.gr_main // 2,
                        self.now_dr[1] + i * self.gr_main + self.gr_main // 2), None)
                self.great_world.add(sprite)

    def add_object(self, i, j, obj, first_block):
        if obj[1] == 'tree':
            self.land_object[i][j] = Tree(first_block, obj, self.tree_animation, self.images[obj[1]])
        elif obj[1] == 'stone':
            self.land_object[i][j] = Stone(first_block, obj, self.tree_animation, self.images[obj[1]])

    def create_objects(self, stor='static'):
        first_block = [self.now_dr[0] - self.world_cord[1] * self.gr_main,
                       self.now_dr[1] - self.world_cord[0] * self.gr_main]
        if stor == 'up':
            self.land_object = self.land_object[:-1]
            self.land_object.insert(0, [None for _ in range(self.sq1)])
            for i in range(self.sq1):
                for obj in self.obj[self.world_cord[0]][self.world_cord[1] + i]:
                    self.add_object(0, i, obj, first_block)
        elif stor == 'down':
            self.land_object = self.land_object[1:]
            self.land_object.insert(self.sq1, [None for _ in range(self.sq1)])
            for i in range(self.sq1):
                for obj in self.obj[self.world_cord[0] + self.sq2 - 1][self.world_cord[1] + i]:
                    self.add_object(self.sq2 - 1, i, obj, first_block)
        elif stor == 'left':
            for i in range(self.sq2):
                self.land_object[i] = self.land_object[i][:-1]
                self.land_object[i].insert(0, None)
            for i in range(self.sq2):
                for obj in self.obj[self.world_cord[0] + i][self.world_cord[1]]:
                    self.add_object(i, 0, obj, first_block)
        elif stor == 'right':
            for i in range(self.sq2):
                self.land_object[i] = self.land_object[i][1:]
                self.land_object[i].insert(self.sq1 - 1, None)
            for i in range(self.sq2):
                for obj in self.obj[self.world_cord[0] + i][self.world_cord[1] + self.sq1 - 1]:
                    self.add_object(i, self.sq1 - 1, obj, first_block)
        else:
            for i in range(self.world_cord[0], self.world_cord[0] + self.sq2):
                for j in range(self.world_cord[1], self.world_cord[1] + self.sq1):
                    for obj in self.obj[i][j]:
                        self.add_object(i - self.world_cord[0], j - self.world_cord[1], obj, first_block)
