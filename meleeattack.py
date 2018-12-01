from pico2d import *
import game_world
import game_framework

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 5

class Fist:
    img = [None,None,None,None,None]

    def __init__(self, x = 400, y = 300, angle = 0.0):
        if Fist.img[0] == None:
            Fist.img[0] = load_image('resource\img\\attackframe1.png')
        if Fist.img[1] == None:
            Fist.img[1] = load_image('resource\img\\attackframe2.png')
        if Fist.img[2] == None:
            Fist.img[2] = load_image('resource\img\\attackframe3.png')
        if Fist.img[3] == None:
            Fist.img[3] = load_image('resource\img\\attackframe4.png')
        if Fist.img[4] == None:
            Fist.img[4] = load_image('resource\img\\attackframe5.png')
        self.x = x
        self.y = y
        self.angle = angle
        self.name = 3
        self.cx = 0.0
        self.cy = 0.0
        self.time = 0.0
        self.frame = 0

    def draw(self):

        self.img[int(self.frame)].rotate_draw(self.angle, self.cx, self.cy, 64, 64)

    def set_center_object(self, boy):
        self.center_object = boy

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 5
        self.cx, self.cy = self.x - self.center_object.bg.window_left, self.y - self.center_object.bg.window_bottom
        self.time += game_framework.frame_time

        if self.time>0.5:
            game_world.remove_object(self)

        for o in game_world.objects[1]:
            if o.name == 2:
                if math.sqrt((o.x-self.x)**2+(o.y-self.y)**2) < o.size*0.5 + 32:
                    if o.nucked == False:
                        o.nucked = True
                        o.nucktime = 1.0
                        o.hp -=1
            elif o.name == 0:
                self.x = o.x-(math.sin(o.angle+o.headangle)*30)
                self.y = o.y+(math.cos(o.angle+o.headangle)*30)
                self.angle = o.angle + o.headangle

