import pygame
from Tree_class import Tree
from Ground_class import Ground
from Characters import MCharacter


class World:
    def __init__(self, win, centre, cord, bioms, obj, width):
        self.land = {'🟨': pygame.image.load('data/ground/grass.png').convert_alpha(),
                     '🟩': pygame.image.load('data/ground/forest.png').convert_alpha(),
                     '🟦': pygame.image.load('data/ground/water.png').convert_alpha(),
                     '⬛': pygame.image.load('data/ground/stone.png').convert_alpha()}
        self.obj = obj[0]
        self.sel_obj = obj[1]
        self.bioms = bioms
        self.gr_main = 180
        self.sq = width // self.gr_main + 5
        self.win = win
        self.centre = centre
        self.start_dr = [self.centre[0] - self.gr_main // 2 - (self.sq // 2) * self.gr_main,
                         self.centre[1] - self.gr_main // 2 - (self.sq // 2) * self.gr_main]
        self.now_dr = [self.centre[0] - self.gr_main // 2 - (self.sq // 2) * self.gr_main,
                       self.centre[1] - self.gr_main // 2 - (self.sq // 2) * self.gr_main]
        self.great_world = pygame.sprite.Group()
        self.trees_list = [[pygame.sprite.Group() for _ in range(self.sq)] for _ in range(self.sq)]
        self.world_cord = cord

    def move_scene(self):
        if max(self.now_dr[0], self.start_dr[0]) - min(self.now_dr[0], self.start_dr[0]) >= self.gr_main:
            res = self.now_dr[0] > self.start_dr[0]
            self.now_dr[0] = self.now_dr[0] - self.gr_main if res else self.now_dr[0] + self.gr_main
            if res:
                self.world_cord[1] = self.world_cord[1] - 1 if self.world_cord[1] >= 1 else None
                self.create_objects('left')
            else:
                self.world_cord[1] += 1
                self.create_objects('right')
            self.create_ground()
        elif max(self.now_dr[1], self.start_dr[1]) - min(self.now_dr[1], self.start_dr[1]) >= self.gr_main:
            res = self.now_dr[1] > self.start_dr[1]
            self.now_dr[1] = self.now_dr[1] - self.gr_main if res else self.now_dr[1] + self.gr_main
            if res:
                self.world_cord[0] = self.world_cord[0] - 1 if self.world_cord[0] >= 1 else None
                self.create_objects('up')
            else:
                self.world_cord[0] += 1
                self.create_objects('down')
            self.create_ground()

    def check_barrier(self, move):
        for i in range(self.sq):
            for j in range(self.sq):
                res = self.now_dr[0] + j * self.gr_main in range(self.centre[0] - self.gr_main, self.centre[0]) and \
                      self.now_dr[1] + i * self.gr_main in range(self.centre[1] - self.gr_main, self.centre[1])
                if res:
                    if self.bioms[self.world_cord[0] + i][self.world_cord[1] + j] == '🟦':
                        self.now_dr[0] -= move[0]
                        self.now_dr[1] -= move[1]
                        return True
        return False

    def draw(self, move=(0, 0)):
        self.win.fill((0, 0, 0))
        self.now_dr[0] += move[0]
        self.now_dr[1] += move[1]

        self.move_scene()

        flag = self.check_barrier(move)
        self.great_world.draw(self.win)
        self.great_world.update(move, flag)
        for objs in self.trees_list:
            for obj in objs:
                obj.draw(self.win)
                obj.update(move, flag)

    def update_character(self, way='stay'):
        self.win.blit(pygame.image.load(f'data/character/{way}.png').convert_alpha(), (915, 430))  # временно

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
                for tree in self.trees_list[i - self.world_cord[0]][j - self.world_cord[1]]:
                    tree.select()
                break
        return propusk

    def create_ground(self):
        self.great_world = pygame.sprite.Group()
        for i in range(self.sq):
            for j in range(self.sq):
                sprite = Ground(self.land[self.bioms[self.world_cord[0] + i][self.world_cord[1] + j]], (self.now_dr[0] + j * self.gr_main + self.gr_main // 2, self.now_dr[1] + i * self.gr_main + self.gr_main // 2))
                self.great_world.add(sprite)

    def create_objects(self, stor='static'):
        first_block = [self.now_dr[0] - self.world_cord[1] * self.gr_main,
                       self.now_dr[1] - self.world_cord[0] * self.gr_main]
        if stor == 'up':
            self.trees_list = self.trees_list[:-1]
            self.trees_list.insert(0, [pygame.sprite.Group() for _ in range(self.sq)])
            for i in range(self.sq):
                for obj in self.obj[self.world_cord[0]][self.world_cord[1] + i]:
                    if obj[1] == 'tree':
                        self.trees_list[0][i].add(Tree(first_block, obj))
        elif stor == 'down':
            self.trees_list = self.trees_list[1:]
            self.trees_list.insert(self.sq, [pygame.sprite.Group() for _ in range(self.sq)])
            for i in range(self.sq):
                for obj in self.obj[self.world_cord[0] + self.sq - 1][self.world_cord[1] + i]:
                    if obj[1] == 'tree':
                        self.trees_list[self.sq - 1][i].add(Tree(first_block, obj))
        elif stor == 'left':
            for i in range(self.sq):
                self.trees_list[i] = self.trees_list[i][:-1]
                self.trees_list[i].insert(0, pygame.sprite.Group())
            for i in range(self.sq):
                for obj in self.obj[self.world_cord[0] + i][self.world_cord[1]]:
                    if obj[1] == 'tree':
                        self.trees_list[i][0].add(Tree(first_block, obj))
        elif stor == 'right':
            for i in range(self.sq):
                self.trees_list[i] = self.trees_list[i][1:]
                self.trees_list[i].insert(self.sq - 1, pygame.sprite.Group())
            for i in range(self.sq):
                for obj in self.obj[self.world_cord[0] + i][self.world_cord[1] + self.sq - 1]:
                    if obj[1] == 'tree':
                        self.trees_list[i][self.sq - 1].add(Tree(first_block, obj))
        else:
            for i in range(self.world_cord[0], self.world_cord[0] + self.sq):
                for j in range(self.world_cord[1], self.world_cord[1] + self.sq):
                    for obj in self.obj[i][j]:
                        if obj[1] == 'tree':
                            self.trees_list[i - self.world_cord[0]][j - self.world_cord[1]].add(Tree(first_block, obj))
