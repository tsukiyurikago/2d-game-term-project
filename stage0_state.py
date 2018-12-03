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
from enemy import Enemy
from lymph_node import Lymphnode
from wall import Wall


name = "Stage0State"

boy = None
background = None
maskimg = None
starttime = None
stagefont = None
fonttimer = None
time = 0.0

def enter():
    global maskimg
    maskimg = load_image('resource\img\mask.png')
    global starttime
    starttime = 0.0
    global fonttimer
    fonttimer = 0.0

    global stagefont
    stagefont = load_font('ENCR10B.TTF', 72)

    global background
    background = Background('resource\img\stage0.png')
    game_world.add_object(background, 0)

    global boy
    boy = Boy(940,0)
    game_world.add_object(boy, 1)

    enemy = Enemy(1200,300,32,3,0, 300)
    enemy.center_object = boy
    game_world.add_object(enemy, 1)
    enemy1 = Enemy(1150,350,20,2,0,300)
    enemy1.center_object = boy
    game_world.add_object(enemy1, 1)

    global lymphnode
    lymphnode = Lymphnode(550,1320)
    lymphnode.center_object = boy
    game_world.add_object(lymphnode, 1)

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
    global maskimg
    global stagefont
    del(stagefont)
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
    global time
    global boy
    global fonttimer

#    time += game_framework.frame_time
#    if time > 5.0:
#        enemy = Enemy(random.randint(1050,1150),random.randint(850,950),1.0,5, random.randint(0,1))
#        enemy.center_object = boy
#        game_world.add_object(enemy, 1)
#        time = 0.0

    if fonttimer < 1.0 or fonttimer > 2.0:
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
    if starttime <3.0:
        starttime += game_framework.frame_time

    if boy.hp == 0:
        starttime += game_framework.frame_time
        if starttime > 7.0:
            game_world.clear()
            game_framework.change_state(gameover_state)

    if fonttimer < 4.0:
        fonttimer += game_framework.frame_time




def draw():
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()
    if starttime <3.0:
        maskimg.opacify(-starttime*0.33+1)
        maskimg.draw(1024/2, 768/2)
    if starttime > 4.0:
        maskimg.opacify((starttime-4)*0.33)
        maskimg.draw(1024/2, 768/2)
    if fonttimer < 1.0:
        stagefont.draw(fonttimer*650-300, 400, 'The Stomach', (155, 71, 71))
        stagefont.draw(-fonttimer*650+1024, 412, 'The Stomach', (255, 255, 255))
    if fonttimer >= 1.0 and fonttimer <= 2.0:
        stagefont.draw(348, 400, 'The Stomach', (155, 71, 71))
        stagefont.draw(372, 412, 'The Stomach', (255, 255, 255))
    if fonttimer > 2.0:
        stagefont.draw(fonttimer*550-700, 400, 'The Stomach', (155, 71, 71))
        stagefont.draw(-fonttimer*650+1024+600, 412, 'The Stomach', (255, 255, 255))
    update_canvas()