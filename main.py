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
normal_fps = 60
speed = 6
const_for_speed = normal_fps * speed  # не использовать 300!!!!

size_world = 200
gen = Generation(size_world)
world_pos_x = size_world // 2
world_pos_y = size_world // 2
gen.generation()
matr_worls = gen.add_barier(15)
obj = gen.xy_objects()
world = World(win, centre, [world_pos_x, world_pos_y], matr_worls, obj)
world.create()

count_x = 0
count_y = 0
flag = False
open_crafter = False

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


start = datetime.now().microsecond
fpstxt = my_font.render(f'fps: {normal_fps}', False, (255 if normal_fps < 100 else 0, 255 if normal_fps >= 100 else 0, 0))
speedtxt = my_font.render(f'speed: {speed}', False, (255 if speed > 10 else 0, 255 if speed <= 10 else 0, 0))

while True:
    a = datetime.now().microsecond
    world.draw(move, action(), open_crafter)
    for i in pygame.event.get():
        move = world.character.event(move, speed, i)
        if i.type == pygame.QUIT:
            sys.exit()
        elif i.type == pygame.KEYDOWN:
            if i.key == pygame.K_e:
                open_crafter = True if not open_crafter else False
        elif i.type == pygame.MOUSEBUTTONDOWN:
            flag = world.select((i.pos[0], i.pos[1]), True)
        elif i.type == pygame.MOUSEBUTTONUP:
            pass
        elif i.type == pygame.MOUSEMOTION:
            world.select((i.pos[0], i.pos[1]))

    true_fps = 1000000 // (datetime.now().microsecond - a)
    if speed != const_for_speed // true_fps and true_fps > 0:
        speed = speed if 1.48 <= const_for_speed / true_fps <= 1.52 else const_for_speed / true_fps
        if move[0]: move[0] = speed * (abs(move[0]) // move[0])
        if move[1]: move[1] = speed * (abs(move[1]) // move[1])

    end = datetime.now().microsecond
    if abs(end - start) >= 500000 and true_fps > 0:
        fpstxt = my_font.render(f'fps: {true_fps}', False, (255 if true_fps < 100 else 0, 255 if true_fps >= 100 else 0, 0))
        speedtxt = my_font.render(f'speed: {int(speed * 100)/100}', False, (255 if speed > 10 else 0, 255 if speed <= 10 else 0, 0))
        start = datetime.now().microsecond
    win.blit(fpstxt, (20, 100))
    win.blit(speedtxt, (20, 130))

    pygame.display.update()
    if flag == 'quit':
        pygame.display.quit()
        print('Good bye!')
        break
