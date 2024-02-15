import pygame
from Machine import World
from Generation import Generation
import sys
from win32api import GetSystemMetrics

width = GetSystemMetrics(0)
height = GetSystemMetrics(1)
centre = (width // 2, height // 2)
fps = 144
pygame.init()
win = pygame.display.set_mode((width, height))

clock = pygame.time.Clock()

win.blit(pygame.image.load('data/loading/loading1.png').convert_alpha(), (centre[0] - 500, centre[1] - 250))

pygame.display.update()
speed = 288 // fps

sp = [('flower') for _ in range(4)] + [('forest') for _ in range(20)] + [('water') for _ in range(1)] + [('stone')]

gen = Generation(sp, 200)
world_pos_x = 20
world_pos_y = 20
gen.generation()
gen.smoof_generation()
gen.smoof_generation(0, False, True, False)
matr_worls = gen.add_barier(15)
gen.smoof_generation(10)
gen.weathering()

obj = gen.xy_objects()
world = World(win, centre, [world_pos_x, world_pos_y], matr_worls, obj, width)
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
    clock.tick(fps)
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            sys.exit()
        elif i.type == pygame.KEYDOWN:
            flag = False
            if i.key == pygame.K_F1:
                speed = speed * 2
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
            flag = world.check_select(i.pos[0], i.pos[1])
        elif i.type == pygame.MOUSEBUTTONUP:
            flag = world.check_select(i.pos[0], i.pos[1])
    world.draw(move, action())
    pygame.display.update()
