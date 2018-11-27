import random
import json
import os

from pico2d import *
import game_framework
import game_world

from background import FixedBackground as Background
from boy import Boy
from grass import Grass
from enemy import Enemy
from wall import Wall


name = "MainState"

boy = None
background = None
time = 0.0

def enter():

    global boy
    boy = Boy(0,0)
    game_world.add_object(boy, 1)

    global background
    background = Background()
    game_world.add_object(background, 0)

    wall = Wall(100,100,400,400)
    game_world.add_object(wall, 1)

    background.set_center_object(boy)
    boy.set_background(background)

    boy.x=0
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
    for game_object in game_world.all_objects():
        game_object.update()
    global time
    time += game_framework.frame_time
    if time > 2.0:
        enemy = Enemy(50,random.randint(100,600),1.0,5)
        enemy.center_object = boy
        game_world.add_object(enemy, 1)
        time = 0.0
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



def draw():
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()
    update_canvas()