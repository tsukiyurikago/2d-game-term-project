import game_framework
import title_state
from pico2d import *


name = "GameoverState"
image = None

maskimg = None
starttime = None

def enter():
    global image
    image = load_image('resource\img\gameover.png')

    global maskimg
    maskimg = load_image('resource\img\mask.png')
    global starttime
    starttime = 0.0


def exit():
    global image
    del(image)


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                game_framework.quit()
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
                game_framework.change_state(title_state)


def draw():
    clear_canvas()
    image.draw(1024/2, 768/2)
    if starttime <5.0:
        maskimg.opacify( -starttime*0.2 + 1)
        maskimg.draw(1024/2, 768/2)
    update_canvas()







def update():

    global starttime
    if starttime <5.0:
        starttime += game_framework.frame_time


def pause():
    pass


def resume():
    pass