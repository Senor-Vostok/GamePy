import random

import pygame
from datetime import datetime
from Machine import World
from Generation import Generation
import sys
from win32api import GetSystemMetrics

width = GetSystemMetrics(0)
height = GetSystemMetrics(1)
centre = (width // 2, height // 2)
pygame.init()
win = pygame.display.set_mode((width, height))
my_font = pygame.font.SysFont('Futura book C', 30)

clock = pygame.time.Clock()

win.blit(pygame.image.load('data/loading/loading1.png').convert_alpha(), (centre[0] - 500, centre[1] - 250))

pygame.display.update()
normal_fps = 144
speed = 3
const_for_speed = normal_fps * speed

size_world = 200
gen = Generation(size_world)
world_pos_x = random.randint(0, size_world)
world_pos_y = random.randint(0, size_world)
gen.generation()
matr_worls = gen.add_barier(15)

obj = gen.xy_objects()
world = World(win, centre, [world_pos_x, world_pos_y], matr_worls, obj)
world.create_ground()
world.create_objects()

count_x = 0
count_y = 0
flag = False

move = [0, 0]

way = 'stay'


def action():
    if move[1] < 0:
        return 'back'
    elif move[1] > 0:
        return 'forward'
    elif move[0] < 0:
        return 'right'
    elif move[0] > 0:
        return 'left'
    else:
        return 'stay'


while True:
    a = datetime.now().microsecond
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            sys.exit()
        elif i.type == pygame.KEYDOWN:
            flag = False
            if i.key == pygame.K_F1:
                speed = speed * 2
            if i.key == pygame.K_F2:
                speed = speed // 2
            if i.key == pygame.K_w:
                move[1] = speed
            if i.key == pygame.K_s:
                move[1] = -speed
            if i.key == pygame.K_a:
                move[0] = speed
            if i.key == pygame.K_d:
                move[0] = -speed
        elif i.type == pygame.KEYUP:
            if i.key == pygame.K_w or i.key == pygame.K_s:
                move[1] = 0
            if i.key == pygame.K_a or i.key == pygame.K_d:
                move[0] = 0
        elif i.type == pygame.MOUSEBUTTONDOWN:
            flag = world.select((i.pos[0], i.pos[1]))
        elif i.type == pygame.MOUSEBUTTONUP:
            pass
    world.draw(move, action())
    true_fps = 1000000 // (datetime.now().microsecond - a)
    if speed != const_for_speed // true_fps and true_fps > 0:
        speed = const_for_speed // true_fps
        if move[0]: move[0] = const_for_speed // true_fps * (abs(move[0]) // move[0])
        if move[1]: move[1] = const_for_speed // true_fps * (abs(move[1]) // move[1])
    fpstxt = my_font.render(f'fps: {true_fps}', False, (255 if true_fps < 100 else 0, 255 if true_fps >= 100 else 0, 0))
    speedtxt = my_font.render(f'speed: {speed}', False, (255 if speed > 10 else 0, 255 if speed <= 10 else 0, 0))
    win.blit(fpstxt, (20, 100))
    win.blit(speedtxt, (20, 130))

    pygame.display.update()
    if flag == 'quit':
        pygame.display.quit()
        print('Good bye!')
        break
