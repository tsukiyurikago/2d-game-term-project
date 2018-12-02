import random
import json
import os
import stage1_state
import gameover_state

from pico2d import *
import game_framework
import game_world

from background import FixedBackground as Background
from boy import Boy
from grass import Grass
from enemy import Enemy
from wall import Wall


name = "Stage0State"

boy = None
background = None
maskimg = None
starttime = None
time = 0.0

def enter():
    global maskimg
    maskimg = load_image('resource\img\mask.png')
    global starttime
    starttime = 0.0

    global background
    background = Background('resource\img\stage0.png')
    game_world.add_object(background, 0)

    global boy
    boy = Boy(940,0)
    game_world.add_object(boy, 1)

    wall = Wall(0,0,830,570)
    game_world.add_object(wall, 1)
    wall = Wall(830,360,1050,570)
    game_world.add_object(wall, 1)
    wall = Wall(1050,360,1450,730)
    game_world.add_object(wall, 1)
    wall = Wall(1070,0,1720,170)
    game_world.add_object(wall, 1)
    wall = Wall(1720,0,2048,1010)
    game_world.add_object(wall, 1)
    wall = Wall(1070,1010,2048,1250)
    game_world.add_object(wall, 1)
    wall = Wall(700,1250,2048,1410)
    game_world.add_object(wall, 1)
    wall = Wall(1200,1410,2048,2048)
    game_world.add_object(wall, 1)
    wall = Wall(1050,360,1450,730)
    game_world.add_object(wall, 1)
    wall = Wall(0,570,400,1650)
    game_world.add_object(wall, 1)

    background.set_center_object(boy)
    boy.set_background(background)

    boy.x=940
    boy.y=0

def exit():
    game_world.clear()


def pause():
    pass


def resume():
    pass


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
                game_framework.quit()
        else:
            boy.handle_event(event)


def update():
    global time
    global boy

    time += game_framework.frame_time
    if time > 5.0:
        enemy = Enemy(random.randint(1050,1150),random.randint(850,950),1.0,5, random.randint(0,1))
        enemy.center_object = boy
        game_world.add_object(enemy, 1)
        time = 0.0

    for game_object in game_world.all_objects():
        game_object.update()
    for o in game_world.objects[1]:
        if o.name == 0 or o.name == 2:
            if o.x > 2048:
                o.x = 2048
            if o.x < 0:
                o.x = 0
            if o.y > 2048:
                o.y = 2048
            if o.y < 0:
                o.y =0

    if boy.y >2000 and boy.x>900 and boy.x<1200 and boy.hp>0:
        game_world.clear()
        game_framework.change_state(stage1_state)

    global starttime
    if starttime <2.0:
        starttime += game_framework.frame_time

    if boy.hp == 0:
        starttime += game_framework.frame_time
        if starttime > 4.0:
            game_world.clear()
            game_framework.change_state(gameover_state)




def draw():
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()
    if starttime <1.0:
        maskimg.opacify(1 - starttime)
        maskimg.draw(1024/2, 768/2)
    if starttime > 3.0:
        maskimg.opacify(starttime-3)
        maskimg.draw(1024/2, 768/2)
    update_canvas()