import game_framework
import stage0_state
from pico2d import *


name = "TitleState"
maskimage= None
image = None
startsound =None
changestart = None
changetime = None

def enter():
    global maskimage
    global image
    global startsound
    global changestart
    global changetime
    image = load_image('resource\img\\title.png')
    maskimage = load_image('resource\img\\mask.png')
    startsound = load_wav('resource\se\\title_enter.wav')
    changestart=False
    changetime = 0.0


def exit():
    global image
    global startsound
    del(startsound)
    del(image)


def handle_events():
    global changestart
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                game_framework.quit()
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE) and changestart==False:
                startsound.play()
                changestart=True



def draw():
    global changetime
    global maskimage
    clear_canvas()
    image.draw(1024/2, 768/2)
    maskimage.opacify(changetime*0.33)
    maskimage.draw(1024/2, 768/2)
    update_canvas()







def update():
    global changestart
    global changetime

    if(changestart):
        changetime += game_framework.frame_time
        if(changetime>3.0):
                game_framework.change_state(stage0_state)


def pause():
    pass


def resume():
    pass