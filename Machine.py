import pygame
from Tree_class import Tree
from Ground_class import Ground
from Characters import MCharacter


class World:
    def __init__(self, win, centre, cord, bioms, obj, width):
        self.water_animation = [pygame.image.load(f'data/animations/water_animations/wave{i}.png').convert_alpha() for i
                                in range(1, 5)]
        self.tree_animation = [pygame.image.load(f'data/animations/tree_animations/shake{i}.png').convert_alpha() for i
                               in range(1, 6)]
        self.land = {'flower': pygame.image.load('data/ground/grass.png').convert_alpha(),
                     'forest': pygame.image.load('data/ground/forest.png').convert_alpha(),
                     'water': pygame.image.load('data/ground/water.png').convert_alpha(),
                     'stone': pygame.image.load('data/ground/stone.png').convert_alpha(),
                     'sand': pygame.image.load('data/ground/sand.png').convert_alpha()}

        self.obj = obj[0]
        self.sel_obj = obj[1]

        self.bioms = bioms
        self.gr_main = 180
        self.sq = width // self.gr_main + 3

        self.win = win

        self.centre = centre
        self.global_centre = [centre[0], centre[1]]

        self.start_dr = [self.centre[0] - self.gr_main // 2 - (self.sq // 2) * self.gr_main,
                         self.centre[1] - self.gr_main // 2 - (self.sq // 2) * self.gr_main]
        self.now_dr = [self.centre[0] - self.gr_main // 2 - (self.sq // 2) * self.gr_main,
                       self.centre[1] - self.gr_main // 2 - (self.sq // 2) * self.gr_main]
        self.move_barrier = (70, 50)

        self.great_world = pygame.sprite.Group()
        self.trees_list = [[None for _ in range(self.sq)] for _ in range(self.sq)]

        self.world_cord = cord

        self.character = pygame.sprite.Group(MCharacter((self.centre[0], self.centre[1] - 60)))

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
        square = self.sq // 2
        for i in range(square - 1, square + 2):
            for obj in self.trees_list[i]:
                if obj:
                    coord = obj.get_cord()
                    col = obj.iscolision()
                    if coord[1] + 100 + move[1] in range(point[1] - col[1][0], point[1] + col[1][1]) and coord[0] + \
                            move[0] in range(point[0] - col[0][0], point[0] + col[0][1]):
                        return False

            for j in range(square - 1, square + 2):
                res = point[0] - move[0] in range(self.now_dr[0] + i * self.gr_main,
                                                  self.now_dr[0] + i * self.gr_main + self.gr_main) and \
                      point[1] - move[1] in range(self.now_dr[1] + j * self.gr_main,
                                                  self.now_dr[1] + j * self.gr_main + self.gr_main)
                pygame.draw.rect(self.win, (0, 0, 255), (
                self.now_dr[0] + i * self.gr_main, self.now_dr[1] + j * self.gr_main, self.gr_main, self.gr_main), 5)
                if res:
                    if self.bioms[self.world_cord[0] + j][self.world_cord[1] + i] == 'water':
                        return False
        return True

    def draw(self, move=(0, 0), way='stay'):
        self.win.fill((0, 0, 0))
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
        if not flag:
            self.character.update(way, [0, 0])
        if flag and not flag2:
            self.character.update(way, move)

        self.great_world.update(move, flag and flag2)
        self.great_world.draw(self.win)
        self.character.draw(self.win)
        for objs in self.trees_list:
            for obj in objs:
                if obj:
                    obj.update(move, flag and flag2)
                    obj.draw(self.win)
                    coord = obj.get_cord()
                    if coord[1] + 100 <= self.centre[1] and coord[0] in range(self.centre[0] - 90, self.centre[0] + 90):
                        self.character.draw(self.win)
        #pygame.draw.rect(self.win, (255, 0, 0), (
        #self.global_centre[0] - self.move_barrier[0], self.global_centre[1] - self.move_barrier[1],
        #self.move_barrier[0] * 2, self.move_barrier[1] * 2), 5)
        #self.check_barrier(move, self.centre)

    def check_select(self, mouse_x, mouse_y):
        flag = False
        propusk = True
        minus_x = self.world_cord[1] * self.gr_main - self.now_dr[0]
        minus_y = self.world_cord[0] * self.gr_main - self.now_dr[1]
        j = 0
        for i in range(self.world_cord[0], self.world_cord[0] + self.sq):
            for j in range(self.world_cord[1], self.world_cord[1] + self.sq):
                if self.sel_obj[i][j][0][1] == 'tree':
                    cx = self.sel_obj[i][j][0][0][0] - minus_x
                    cy = self.sel_obj[i][j][0][0][1] - minus_y
                    if mouse_x in range(cx, cx + 100) and mouse_y in range(cy, cy + 150):
                        flag = True
                        break
            if flag:
                propusk = False
                self.trees_list[i - self.world_cord[0]][j - self.world_cord[1]].select()
                break
        return propusk

    def create_ground(self):
        self.great_world = pygame.sprite.Group()
        for i in range(self.sq):
            for j in range(self.sq):
                if self.bioms[self.world_cord[0] + i][self.world_cord[1] + j] == 'water':
                    sprite = Ground(self.land[self.bioms[self.world_cord[0] + i][self.world_cord[1] + j]], (
                        self.now_dr[0] + j * self.gr_main + self.gr_main // 2,
                        self.now_dr[1] + i * self.gr_main + self.gr_main // 2), 'water', self.water_animation)
                else:
                    sprite = Ground(self.land[self.bioms[self.world_cord[0] + i][self.world_cord[1] + j]], (
                        self.now_dr[0] + j * self.gr_main + self.gr_main // 2,
                        self.now_dr[1] + i * self.gr_main + self.gr_main // 2), None)
                self.great_world.add(sprite)

    def create_objects(self, stor='static'):
        first_block = [self.now_dr[0] - self.world_cord[1] * self.gr_main,
                       self.now_dr[1] - self.world_cord[0] * self.gr_main]
        if stor == 'up':
            self.trees_list = self.trees_list[:-1]
            self.trees_list.insert(0, [None for _ in range(self.sq)])
            for i in range(self.sq):
                for obj in self.obj[self.world_cord[0]][self.world_cord[1] + i]:
                    if obj[1] == 'tree':
                        self.trees_list[0][i] = Tree(first_block, obj, self.tree_animation)
        elif stor == 'down':
            self.trees_list = self.trees_list[1:]
            self.trees_list.insert(self.sq, [None for _ in range(self.sq)])
            for i in range(self.sq):
                for obj in self.obj[self.world_cord[0] + self.sq - 1][self.world_cord[1] + i]:
                    if obj[1] == 'tree':
                        self.trees_list[self.sq - 1][i] = Tree(first_block, obj, self.tree_animation)
        elif stor == 'left':
            for i in range(self.sq):
                self.trees_list[i] = self.trees_list[i][:-1]
                self.trees_list[i].insert(0, None)
            for i in range(self.sq):
                for obj in self.obj[self.world_cord[0] + i][self.world_cord[1]]:
                    if obj[1] == 'tree':
                        self.trees_list[i][0] = Tree(first_block, obj, self.tree_animation)
        elif stor == 'right':
            for i in range(self.sq):
                self.trees_list[i] = self.trees_list[i][1:]
                self.trees_list[i].insert(self.sq - 1, None)
            for i in range(self.sq):
                for obj in self.obj[self.world_cord[0] + i][self.world_cord[1] + self.sq - 1]:
                    if obj[1] == 'tree':
                        self.trees_list[i][self.sq - 1] = Tree(first_block, obj, self.tree_animation)
        else:
            for i in range(self.world_cord[0], self.world_cord[0] + self.sq):
                for j in range(self.world_cord[1], self.world_cord[1] + self.sq):
                    for obj in self.obj[i][j]:
                        if obj[1] == 'tree':
                            self.trees_list[i - self.world_cord[0]][j - self.world_cord[1]] = Tree(first_block, obj, self.tree_animation)
