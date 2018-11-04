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
            boy.fire_bullet()

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8

        if boy.Rspin == True:
            boy.angle -= boy.spinspeed * game_framework.frame_time
        if boy.Lspin == True:
            boy.angle += boy.spinspeed * game_framework.frame_time
        if boy.headRspin == True and boy.headangle > -2.0:
            boy.angle -= boy.headspeed * game_framework.frame_time * 0.2
            boy.headangle -= boy.headspeed * game_framework.frame_time
        if boy.headLspin == True and boy.headangle < 2.0:
            boy.angle += boy.headspeed * game_framework.frame_time * 0.2
            boy.headangle += boy.headspeed * game_framework.frame_time
        if boy.forward == True:
            boy.y += math.cos(boy.angle) * boy.speed * game_framework.frame_time
            boy.x += -math.sin(boy.angle) * boy.speed * game_framework.frame_time
        if boy.headRspin == False and boy.headLspin == False:
            pass

    @staticmethod
    def draw(boy):
        boy.image.rotate_draw(boy.angle,boy.x,boy.y,boy.size,boy.size)
        boy.headimg.rotate_draw(boy.headangle + boy.angle,boy.x,boy.y,boy.size,boy.size)


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
    MoveState: {RIGHT_UP: MoveState, LEFT_UP: MoveState, LEFT_DOWN: MoveState, RIGHT_DOWN: MoveState, SPACE: MoveState, FORWARD_UP: MoveState, FORWARD_DOWN: MoveState, LEFTSIDE_UP: MoveState, LEFTSIDE_DOWN :MoveState, RIGHTSIDE_UP: MoveState, RIGHTSIDE_DOWN: MoveState},
    SleepState: {LEFT_DOWN: MoveState, RIGHT_DOWN: MoveState, LEFT_UP: MoveState, RIGHT_UP: MoveState, SPACE: IdleState}
}

class Boy:

    def __init__(self):
        self.x, self.y = 1600 // 2, 90
        # Boy is only once created, so instance image loading is fine
        self.image = load_image('testimg.png')
        self.headimg = load_image('testimghead.png')
        self.font = load_font('ENCR10B.TTF', 16)
        self.frame = 0
        self.event_que = []
        self.cur_state = MoveState
        self.cur_state.enter(self, None)
        self.size = 128
        self.angle = 0.0
        self.Lspin = False
        self.Rspin = False
        self.spinspeed = 3.0
        self.speed = 100.0
        self.headangle = 0.0
        self.headspeed = 3.0
        self.headLspin = False
        self.headRspin = False
        self.forward = False
        self.name = 0


    def fire_bullet(self):
        bullet = Bullet(self.size*0.5*-math.sin(self.angle+self.headangle)+self.x, self.size*0.5*math.cos(self.angle+self.headangle)+self.y, self.angle + self.headangle, 400.0)
        game_world.add_object(bullet, 1)


    def fire_ghost(self):
        pass

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
        self.font.draw(self.x - 60, self.y + 50, '(Time: %3.2f)' % get_time(), (255, 255, 0))

    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)

