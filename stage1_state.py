import random
import json
import os

from pico2d import *
import game_framework
import game_world
import gameover_state
import end_state

from background import FixedBackground as Background
from boy import Boy
from thyroid import Thyroid
from wall import Wall


name = "Stage1State"

boy = None
background = None
maskimg = None
starttime = None
nextstagetimer = None

def enter():

    global maskimg
    maskimg = load_image('resource\img\mask.png')
    global starttime
    starttime = 0.0
    global nextstagetimer
    nextstagetimer = 0.0

    global background
    background = Background('resource\img\stage1.png')
    game_world.add_object(background, 0)

    global boy
    boy = Boy(0,0)
    game_world.add_object(boy, 1)

    global thyroid
    thyroid = Thyroid(1125,1200)
    thyroid.center_object = boy
    game_world.add_object(thyroid, 1)

    wall = Wall(100,100,400,400)
    game_world.add_object(wall, 1)

    background.set_center_object(boy)
    boy.set_background(background)

    boy.x=1100
    boy.y=700

def exit():
    global maskimg
    del(maskimg)
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
    global starttime
    global nextstagetimer

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

    if thyroid.hp == 0:
        nextstagetimer += game_framework.frame_time
        if nextstagetimer>2.0:
            game_world.clear()
            game_framework.change_state(end_state)

    if boy.hp == 0:
        starttime += game_framework.frame_time
        if starttime > 3.0:
            game_world.clear()
            game_framework.change_state(gameover_state)


def draw():
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()
    if starttime > 0.1:
        maskimg.opacify(starttime*0.33)
        maskimg.draw(1024/2, 768/2)
    update_canvas()