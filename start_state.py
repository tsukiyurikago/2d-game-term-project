import game_framework
import title_state
from pico2d import *

name = "StartState"
image = None
logo_time = 0.0


def enter():
    global image
    image = load_image('resource\img\start.png')


def exit():
    global image
    del(image)


def update():
    global logo_time

    if(logo_time > 3.0):
        logo_time = 0
        #game_framework.quit()
        game_framework.change_state(title_state)
    logo_time += game_framework.frame_time


def draw():
    global image
    clear_canvas()
    image.draw(1024/2, 768/2)
    draw_rectangle(1024/2-500,50,1024/2-500+(logo_time*300),51)
    update_canvas()




def handle_events():
    events = get_events()
    pass


def pause(): pass


def resume(): pass