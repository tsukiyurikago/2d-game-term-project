import game_framework
from pico2d import *
import math
import random

import game_world
from bullet import Bullet
from enemy import Enemy

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
SLEEP_TIMER = range(1)

key_event_table = {

}


# Boy States

class MoveState:

    @staticmethod
    def enter(thyroid, event):
        pass

    @staticmethod
    def exit(thyroid, event):
        pass

    @staticmethod
    def do(thyroid):
        #if thyroid.angle < math.atan2(-game_framework.stack[0].boy.y + thyroid.y, -game_framework.stack[0].boy.x + thyroid.x) + (90*3.14/180):
        #    thyroid.angle += thyroid.spinspeed * game_framework.frame_time
        #else:
        #    thyroid.angle -= thyroid.spinspeed * game_framework.frame_time

        for bullet in game_world.objects[1]:
            if bullet.name == 1:
                if (bullet.x - thyroid.x)**2 + (bullet.y - thyroid.y)**2 < (thyroid.xsize*0.5 + 8)**2 and bullet.y-6 < thyroid.y + (thyroid.ysize/2)-50:
                    game_world.remove_object(bullet)
                    if(thyroid.nucked == False and thyroid.hp > 0):
                        thyroid.nucked = True
                        thyroid.nucktime = 0.5
                        thyroid.hp -= 1
                        thyroid.hitsound.play()
            if bullet.name == 0:
                thyroid.distance = math.sqrt((bullet.x - thyroid.x)**2 + (bullet.y - thyroid.y)**2)
                if bullet.x+(bullet.size*0.5) > thyroid.x-(thyroid.xsize/2) and bullet.x-(bullet.size*0.5) < thyroid.x + (thyroid.xsize/2) and bullet.y+(bullet.size*0.5) > thyroid.y - (thyroid.ysize/2) and bullet.y-(bullet.size*0.5) < thyroid.y + (thyroid.ysize/2):
                    thyroid.speed = 0.0
                    thyroid.xspeed = -math.sin(thyroid.angle) * thyroid.speed * game_framework.frame_time
                    thyroid.yspeed = math.cos(thyroid.angle) * thyroid.speed * game_framework.frame_time
                    bullet.x += -math.sin(thyroid.angle)
                    bullet.y += math.cos(thyroid.angle)
                    if bullet.godmod == False and bullet.hp>0:
                        bullet.hp -= 1
                        bullet.godmod = True
                else:
                    thyroid.speed = 30.0
                    thyroid.xspeed = -math.sin(thyroid.angle) * thyroid.speed * game_framework.frame_time
                    thyroid.yspeed = math.cos(thyroid.angle) * thyroid.speed * game_framework.frame_time

                if thyroid.attackstate:
                    if thyroid.attacktype == 1:
                        if thyroid.cooltime == 0.0:
                            realbullet = Bullet((thyroid.size + 20) * 0.5 * -math.sin(thyroid.angle) + thyroid.x,
                                            (thyroid.size + 20) * 0.5 * math.cos(thyroid.angle) + thyroid.y,
                                                thyroid.angle, 200.0)
                            realbullet.center_object = bullet
                            game_world.add_object(realbullet, 1)
                            thyroid.cooltime += game_framework.frame_time
                        if thyroid.cooltime >2.0:
                            thyroid.cooltime = 0.0

        thyroid.angle = math.atan2(-game_framework.stack[0].boy.y + thyroid.y, -game_framework.stack[0].boy.x + thyroid.x) + (90*3.14/180)

        if thyroid.attackstate == False:
            thyroid.y += thyroid.yspeed
            thyroid.x += thyroid.xspeed

        if thyroid.nucktime > 0.0:
            thyroid.nucktime -= game_framework.frame_time

        if thyroid.nucktime <= 0.0:
            thyroid.nucked = False

            thyroid.frame = (thyroid.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8

        thyroid.beattimer += game_framework.frame_time
        thyroid.spawntimer += game_framework.frame_time

        if thyroid.spawntimer>thyroid.spawncycle:
            if random.randint(0,1):
                enemy = Enemy((thyroid.xsize-50) * 0.5 * -math.sin(thyroid.angle) + thyroid.x, (thyroid.ysize - 50) * 0.5 * math.cos(thyroid.angle) + thyroid.y,random.randint(10,30),random.randint(1,2), 0, 1000)
            else:
                enemy = Enemy(thyroid.xsize * 0.5 * -math.sin(thyroid.angle) + thyroid.x, thyroid.ysize * 0.5 * math.cos(thyroid.angle) + thyroid.y, random.randint(10, 30), random.randint(1, 2), 1, 1000)
            enemy.center_object = game_framework.stack[0].boy
            game_world.add_object(enemy, 1)
            time = 0.0
            thyroid.spawntimer = 0.0
        #thyroid.spawncycle = thyroid.hp*0.9


        if thyroid.beattimer>3.0:
            thyroid.beattimer = 0.0

    @staticmethod
    def draw(thyroid):
        if thyroid.nucked:
            thyroid.image.opacify(math.cos(thyroid.nucktime*30))
        else:
            thyroid.image.opacify(1)
        thyroid.image.draw(thyroid.cx,thyroid.cy,math.cos(math.sin(thyroid.beattimer*5)*(12-thyroid.hp))*10+thyroid.xsize,math.cos(math.sin(thyroid.beattimer*5)*(12-thyroid.hp))*5+thyroid.ysize)







next_state_table = {
    MoveState: {}
}

class Thyroid:

    image = None
    hitsound = None

    def __init__(self, x = 0, y = 0, spinspeed = 1.0, hp = 10):
        self.x, self.y = x, y
        if Thyroid.image == None:
            Thyroid.image = load_image('resource\img\\thyroid.png')
        if Thyroid.hitsound == None:
            Thyroid.hitsound = load_wav('resource\se\\blood.wav')
        self.font = load_font('ENCR10B.TTF', 16)
        self.frame = 0
        self.event_que = []
        self.cur_state = MoveState
        self.cur_state.enter(self, None)
        self.size = 32
        self.angle = 0.0
        self.spinspeed = spinspeed
        self.speed = 30.0
        self.hp = hp
        self.name = 22
        self.cx = 0.0
        self.cy = 0.0
        self.xspeed = 0.0
        self.yspeed = 0.0
        self.mp = 100
        self.distance = 0
        self.timer = 0.0
        self.attackstate = False
        self.cooltime = 0.0
        self.nucktime =0.0
        self.nucked = False
        self.beattimer = 0.0
        self.xsize=400.0
        self.ysize = 400.0
        self.spawncycle = 0.5
        self.spawntimer = 0.0
        self.deathtimer = 0.0

    def set_center_object(self, boy):
        self.center_object = boy

    def fire_ball(self):
        pass


    def fire_ghost(self):
        pass

    def add_event(self, event):
        self.event_que.insert(0, event)

    def update(self):
        self.cx, self.cy = self.x - self.center_object.bg.window_left, self.y - self.center_object.bg.window_bottom
        self.cur_state.do(self)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            self.cur_state = next_state_table[self.cur_state][event]
            self.cur_state.enter(self, event)
        if self.hp <= 0:
            self.deathtimer += game_framework.frame_time
            self.image.opacify((2-self.deathtimer)*0.5)
            if self.deathtimer > 1.0:
                game_world.remove_object(self)

    def draw(self):
        self.cur_state.draw(self)
        self.font.draw(self.cx - 60, self.cy + 50, '(hp: %d)' % self.hp, (255, self.hp*50, self.hp*50))