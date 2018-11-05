import random
import json
import os

from pico2d import *
import game_framework
import game_world

from boy import Boy
from grass import Grass
from enemy import Enemy
from wall import Wall


name = "MainState"

boy = None
enemys = []
time = 0.0

def enter():
    global boy
    boy = Boy()
    grass = Grass()
    game_world.add_object(grass, 0)
    game_world.add_object(boy, 1)
    #wall = Wall(0,768,1024,768,1)
    #game_world.add_object(wall, 1)


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
        enemy = Enemy(500,500,1.0,5)
        game_world.add_object(enemy, 1)
        time = 0.0
    for o in game_world.objects[1]:
        if o.name == 0 or o.name == 2:
            if o.x > 1024:
                o.x = 1023
            if o.x < 0:
                o.x = 0
            if o.y > 768:
                o.y = 767
            if o.y < 0:
                o.y =0



def draw():
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()
    update_canvas()