import game_framework
from pico2d import *
from ball import Ball
from ghost import Ghost
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
SLEEP_TIMER, = range(1)

key_event_table = {

}


# Boy States

class IdleState:

    @staticmethod
    def enter(enemy, event):
        pass

    @staticmethod
    def exit(enemy, event):
        pass

    @staticmethod
    def do(enemy):
        enemy.frame = (enemy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
        enemy.timer += game_framework.frame_time
        if enemy.timer > 9.6:
            enemy.add_event(SLEEP_TIMER)

    @staticmethod
    def draw(enemy):
        enemy.image.rotate_draw(enemy.angle, enemy.x, enemy.y, enemy.size, enemy.size)


class MoveState:

    @staticmethod
    def enter(enemy, event):
        pass

    @staticmethod
    def exit(enemy, event):
        pass

    @staticmethod
    def do(enemy):
        #if enemy.angle < math.atan2(-game_framework.stack[0].boy.y + enemy.y, -game_framework.stack[0].boy.x + enemy.x) + (90*3.14/180):
        #    enemy.angle += enemy.spinspeed * game_framework.frame_time
        #else:
        #    enemy.angle -= enemy.spinspeed * game_framework.frame_time
        enemy.angle = math.atan2(-game_framework.stack[0].boy.y + enemy.y, -game_framework.stack[0].boy.x + enemy.x) + (90 * 3.14 / 180)

        enemy.y += math.cos(enemy.angle) * enemy.speed * game_framework.frame_time
        enemy.x += -math.sin(enemy.angle) * enemy.speed * game_framework.frame_time
        enemy.frame = (enemy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8

    @staticmethod
    def draw(enemy):
        enemy.image.rotate_draw(enemy.angle,enemy.x,enemy.y,enemy.size,enemy.size)


class SleepState:

    @staticmethod
    def enter(enemy, event):
        enemy.frame = 0

    @staticmethod
    def exit(enemy, event):
        pass

    @staticmethod
    def do(enemy):
        enemy.frame = (enemy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8

    @staticmethod
    def draw(enemy):
        enemy.image.rotate_draw(enemy.angle,enemy.x,enemy.y,enemy.size,enemy.size)






next_state_table = {
    IdleState: {SLEEP_TIMER: SleepState},
    MoveState: {},
    SleepState: {}
}

class Enemy:

    image = None

    def __init__(self, x = 0, y = 0, spinspeed = 1.0):
        self.x, self.y = x, y
        if Enemy.image == None:
            Enemy.image = load_image('testimg.png')
        self.font = load_font('ENCR10B.TTF', 16)
        self.frame = 0
        self.event_que = []
        self.cur_state = MoveState
        self.cur_state.enter(self, None)
        self.size = 128
        self.angle = 0.0
        self.spinspeed = spinspeed
        self.speed = 50.0
        self.forward = False


    def fire_ball(self):
        pass


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