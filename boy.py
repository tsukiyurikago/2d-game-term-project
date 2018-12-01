import game_framework
from pico2d import *
from bullet import Bullet
import math

import game_world

# Boy Run Speed
PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_KMPH = 20.0 #km.hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# Boy Action Speed
# fill expressions correctly
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8



# Boy Event
RIGHT_DOWN, LEFT_DOWN, RIGHT_UP, LEFT_UP, SLEEP_TIMER, SPACE, FORWARD_DOWN, FORWARD_UP, LEFTSIDE_DOWN, LEFTSIDE_UP, RIGHTSIDE_DOWN, RIGHTSIDE_UP = range(12)

key_event_table = {
    (SDL_KEYDOWN, SDLK_RIGHT): RIGHT_DOWN,
    (SDL_KEYDOWN, SDLK_LEFT): LEFT_DOWN,
    (SDL_KEYUP, SDLK_RIGHT): RIGHT_UP,
    (SDL_KEYUP, SDLK_LEFT): LEFT_UP,
    (SDL_KEYDOWN, SDLK_SPACE): SPACE,
    (SDL_KEYDOWN, SDLK_UP): FORWARD_DOWN,
    (SDL_KEYUP, SDLK_UP): FORWARD_UP,
    (SDL_KEYDOWN, SDLK_a): LEFTSIDE_DOWN,
    (SDL_KEYUP, SDLK_a): LEFTSIDE_UP,
    (SDL_KEYDOWN, SDLK_d): RIGHTSIDE_DOWN,
    (SDL_KEYUP, SDLK_d): RIGHTSIDE_UP
}


# Boy States

class IdleState:

    @staticmethod
    def enter(boy, event):
        if event == RIGHT_DOWN:
            boy.Rspin = True
        elif event == LEFT_DOWN:
            boy.Lspin = True
        elif event == RIGHT_UP:
            boy.Rspin = False
        elif event == LEFT_UP:
            boy.Lspin = False
        boy.timer = 0.0

    @staticmethod
    def exit(boy, event):
        if event == SPACE:
            boy.fire_ball()
        pass

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
        boy.timer += game_framework.frame_time
        if boy.timer > 9.6:
            boy.add_event(SLEEP_TIMER)

    @staticmethod
    def draw(boy):
        boy.image.rotate_draw(boy.angle, boy.x, boy.y, boy.size, boy.size)
        boy.headimg.rotate_draw(boy.headangle,boy.x,boy.y,boy.size,boy.size)


class MoveState:

    @staticmethod
    def enter(boy, event):
        if event == RIGHT_DOWN:
            boy.Rspin = True
        elif event == LEFT_DOWN:
            boy.Lspin = True
        elif event == RIGHT_UP:
            boy.Rspin = False
        elif event == LEFT_UP:
            boy.Lspin = False
        elif event == FORWARD_DOWN:
            boy.forward = True
        elif event == FORWARD_UP:
            boy.forward = False
        elif event == LEFTSIDE_DOWN:
            boy.size += 1
            boy.headLspin = True
        elif event == LEFTSIDE_UP:
            boy.headLspin = False
        elif event == RIGHTSIDE_DOWN:
            boy.headRspin = True
        elif event == RIGHTSIDE_UP:
            boy.headRspin = False

    @staticmethod
    def exit(boy, event):
        if event == SPACE:
            if (boy.bulletamount > 0):
                boy.fire_bullet()
                boy.bulletamount -= 1

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8

        if boy.Rspin == True:
            boy.angle -= boy.spinspeed * game_framework.frame_time
        if boy.Lspin == True:
            boy.angle += boy.spinspeed * game_framework.frame_time
        if boy.headRspin == True and boy.headangle > -3.0:
            boy.angle -= boy.headspeed * game_framework.frame_time * 0.2
            boy.headangle -= boy.headspeed * game_framework.frame_time
        if boy.headLspin == True and boy.headangle < 3.0:
            boy.angle += boy.headspeed * game_framework.frame_time * 0.2
            boy.headangle += boy.headspeed * game_framework.frame_time
        if boy.forward == True:
            boy.speed = 100.0
            boy.xspeed = (-math.sin(boy.angle) * boy.speed + boy.xspeed) * game_framework.frame_time
            boy.yspeed = (math.cos(boy.angle) * boy.speed + boy.yspeed) * game_framework.frame_time
        else:
            boy.speed = 0.0
        if boy.headRspin == False and boy.headLspin == False:
            pass

        for bullet in game_world.objects[1]:
            if bullet.name == 1:
                if math.sqrt((bullet.x - boy.x)**2 + (bullet.y - boy.y)**2) <  boy.size*0.5 + 8:
                    game_world.remove_object(bullet)
            if bullet.name == 2:
                if math.sqrt((bullet.x - boy.x)**2 + (bullet.y - boy.y)**2) < (bullet.size*0.5) + (boy.size*0.5):
                    pass

        boy.y += boy.yspeed
        boy.x += boy.xspeed
        boy.xspeed *= 0.95
        boy.yspeed *= 0.95

        boy.bullettimer += game_framework.frame_time
        if(boy.bullettimer > 0.5):
            if(boy.bulletamount < boy.bulletcapacity):
                boy.bulletamount += 1
            boy.bullettimer = 0.0

    @staticmethod
    def draw(boy):
        cx, cy = boy.x - boy.bg.window_left, boy.y - boy.bg.window_bottom
        boy.image.rotate_draw(boy.angle,cx,cy,boy.size,boy.size)
        boy.headimg.rotate_draw(boy.headangle + boy.angle,cx,cy,boy.size,boy.size)

class SleepState:

    @staticmethod
    def enter(boy, event):
        boy.frame = 0

    @staticmethod
    def exit(boy, event):
        pass

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8

    @staticmethod
    def draw(boy):
        boy.image.rotate_draw(boy.angle,boy.x,boy.y,boy.size,boy.size)
        boy.headimg.rotate_draw(boy.headangle,boy.x,boy.y,boy.size,boy.size)


next_state_table = {
    IdleState: {RIGHT_UP: MoveState, LEFT_UP: MoveState, RIGHT_DOWN: MoveState, LEFT_DOWN: MoveState, SLEEP_TIMER: SleepState, SPACE: IdleState},
    MoveState: {RIGHT_UP: MoveState, LEFT_UP: MoveState, LEFT_DOWN: MoveState, RIGHT_DOWN: MoveState, SPACE: MoveState, FORWARD_UP: MoveState, FORWARD_DOWN: MoveState, LEFTSIDE_UP: MoveState, LEFTSIDE_DOWN :MoveState, RIGHTSIDE_UP: MoveState, RIGHTSIDE_DOWN: MoveState, SLEEP_TIMER: SleepState},
    SleepState: {LEFT_DOWN: MoveState, RIGHT_DOWN: MoveState, LEFT_UP: MoveState, RIGHT_UP: MoveState, SPACE: IdleState, SLEEP_TIMER: SleepState}
}

class Boy:

    def __init__(self, a = 0, b = 0):
        self.canvas_width = get_canvas_width()
        self.canvas_height = get_canvas_height()
        self.x, self.y = 1000, 1000
        # Boy is only once created, so instance image loading is fine
        self.image = load_image('resource\img\playerbody.png')
        self.headimg = load_image('resource\img\playerhead.png')
        self.font = load_font('ENCR10B.TTF', 28)
        self.frame = 0
        self.event_que = []
        self.cur_state = MoveState
        self.cur_state.enter(self, None)
        self.size = 64
        self.angle = 0.0
        self.Lspin = False
        self.Rspin = False
        self.spinspeed = 3.0
        self.xspeed = 0.0
        self.yspeed = 0.0
        self.speed = 100.0
        self.headangle = 0.0
        self.headspeed = 3.0
        self.headLspin = False
        self.headRspin = False
        self.forward = False
        self.name = 0
        self.mp = 100
        self.hp = 10
        self.bulletcapacity=5
        self.bulletamount = 5
        self.bullettimer = 0.0


    def fire_bullet(self):
        bullet = Bullet((self.size+16)*0.5*-math.sin(self.angle+self.headangle)+self.x, (self.size+16)*0.5*math.cos(self.angle+self.headangle)+self.y, self.angle + self.headangle, 400.0)
        bullet.center_object = self
        game_world.add_object(bullet, 1)
        #self.size -= 1


    def set_background(self, bg):
        self.bg = bg
        self.x = self.bg.w / 2
        self.y = self.bg.h / 2


    def add_event(self, event):
        self.event_que.insert(0, event)

    def update(self):
        self.cur_state.do(self)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            self.cur_state = next_state_table[self.cur_state][event]
            self.cur_state.enter(self, event)

    def draw(self):
        self.cur_state.draw(self)
        self.font.draw(50, 52, '(hp: %d)' % self.hp, (255, 0, 0))
        self.font.draw(50, 48, '(hp: %d)' % self.hp, (255, 0, 0))
        self.font.draw(52, 50, '(hp: %d)' % self.hp, (255, 0, 0))
        self.font.draw(48, 50, '(hp: %d)' % self.hp, (255, 0, 0))
        self.font.draw(50, 50, '(hp: %d)' % self.hp, (0, 0, 0))
        for i in range(self.bulletamount):
            self.font.draw(-25*i - 50 + 1024, 50, '0', (255, 0, 0))

    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)

