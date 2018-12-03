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
    def enter(lymph_node, event):
        pass

    @staticmethod
    def exit(lymph_node, event):
        pass

    @staticmethod
    def do(lymph_node):
        #if lymph_node.angle < math.atan2(-game_framework.stack[0].boy.y + lymph_node.y, -game_framework.stack[0].boy.x + lymph_node.x) + (90*3.14/180):
        #    lymph_node.angle += lymph_node.spinspeed * game_framework.frame_time
        #else:
        #    lymph_node.angle -= lymph_node.spinspeed * game_framework.frame_time

        for bullet in game_world.objects[1]:
            if bullet.name == 1:
                if bullet.x+6 > lymph_node.x-(lymph_node.xsize/2) and bullet.x-6 < lymph_node.x + (lymph_node.xsize/2) and bullet.y+6 > lymph_node.y - (lymph_node.ysize/2) and bullet.y-6 < lymph_node.y + (lymph_node.ysize/2):
                    game_world.remove_object(bullet)
                    if(lymph_node.nucked == False):
                        lymph_node.nucked = True
                        lymph_node.nucktime = 0.5
                        lymph_node.hp -= 1
                        lymph_node.hitsound.play()
            if bullet.name == 0:
                lymph_node.distance = math.sqrt((bullet.x - lymph_node.x)**2 + (bullet.y - lymph_node.y)**2)
                if bullet.x+(bullet.size*0.5) > lymph_node.x-(lymph_node.xsize/2) and bullet.x-(bullet.size*0.5) < lymph_node.x + (lymph_node.xsize/2) and bullet.y+(bullet.size*0.5) > lymph_node.y - (lymph_node.ysize/2) and bullet.y-(bullet.size*0.5) < lymph_node.y + (lymph_node.ysize/2):
                    lymph_node.speed = 0.0
                    lymph_node.xspeed = -math.sin(lymph_node.angle) * lymph_node.speed * game_framework.frame_time
                    lymph_node.yspeed = math.cos(lymph_node.angle) * lymph_node.speed * game_framework.frame_time
                    bullet.x += -math.sin(lymph_node.angle)
                    bullet.y += math.cos(lymph_node.angle)
                    if bullet.godmod == False and bullet.hp>0:
                        bullet.hp -= 1
                        bullet.godmod = True
                else:
                    lymph_node.xspeed = -math.sin(lymph_node.angle) * lymph_node.speed * game_framework.frame_time
                    lymph_node.yspeed = math.cos(lymph_node.angle) * lymph_node.speed * game_framework.frame_time

                if lymph_node.attackstate:
                    if lymph_node.attacktype == 1:
                        if lymph_node.cooltime == 0.0:
                            realbullet = Bullet((lymph_node.size + 20) * 0.5 * -math.sin(lymph_node.angle) + lymph_node.x,
                                            (lymph_node.size + 20) * 0.5 * math.cos(lymph_node.angle) + lymph_node.y,
                                                lymph_node.angle, 200.0)
                            realbullet.center_object = bullet
                            game_world.add_object(realbullet, 1)
                            lymph_node.cooltime += game_framework.frame_time
                        if lymph_node.cooltime >2.0:
                            lymph_node.cooltime = 0.0

        if lymph_node.distance<300.0:
            lymph_node.angle = math.atan2(-game_framework.stack[0].boy.y + lymph_node.y, -game_framework.stack[0].boy.x + lymph_node.x) + (90*3.14/180)
        else:
            lymph_node.attackstate = False
            lymph_node.speed = 0.0
            lymph_node.timer -= game_framework.frame_time
            if lymph_node.timer < 0:
                lymph_node.timer += 1.0
                lymph_node.angle = random.random() * 2 * math.pi

        if lymph_node.attackstate == False:
            lymph_node.y += lymph_node.yspeed
            lymph_node.x += lymph_node.xspeed

        if lymph_node.nucktime > 0.0:
            lymph_node.nucktime -= game_framework.frame_time

        if lymph_node.nucktime <= 0.0:
            lymph_node.nucked = False

            lymph_node.frame = (lymph_node.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8

        lymph_node.beattimer += game_framework.frame_time
        lymph_node.spawntimer += game_framework.frame_time

        if lymph_node.spawntimer>lymph_node.spawncycle:
            enemy = Enemy(lymph_node.x + random.randint(-150,150),lymph_node.y + random.randint(-100,-50),lymph_node.hp*8,lymph_node.hp, random.randint(0,1), 250)
            enemy.center_object = game_framework.stack[0].boy
            game_world.add_object(enemy, 1)
            time = 0.0
            lymph_node.spawntimer = 0.0
        lymph_node.spawncycle = lymph_node.hp*0.9


        if lymph_node.beattimer>3.0:
            lymph_node.beattimer = 0.0

    @staticmethod
    def draw(lymph_node):
        if lymph_node.nucked:
            lymph_node.image.opacify(math.cos(lymph_node.nucktime*30))
        else:
            lymph_node.image.opacify(1)
        lymph_node.image.draw(lymph_node.cx,lymph_node.cy,math.cos(math.sin(lymph_node.beattimer*5)*(12-lymph_node.hp))*10+lymph_node.xsize,math.cos(math.sin(lymph_node.beattimer*5)*(12-lymph_node.hp))*5+lymph_node.ysize)







next_state_table = {
    MoveState: {}
}

class Lymphnode:

    image = None
    hitsound = None

    def __init__(self, x = 0, y = 0, spinspeed = 1.0, hp = 10):
        self.x, self.y = x, y
        if Lymphnode.image == None:
            Lymphnode.image = load_image('resource\img\lymph_node.png')
        self.font = load_font('ENCR10B.TTF', 16)
        self.frame = 0
        self.event_que = []
        self.cur_state = MoveState
        self.cur_state.enter(self, None)
        self.size = 32
        self.angle = 0.0
        self.spinspeed = spinspeed
        self.speed = 50.0
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
        self.ysize = 200.0
        self.spawncycle = 10.0
        self.spawntimer = 0.0
        self.hitsound = load_wav('resource\se\\blood.wav')

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
            game_world.remove_object(self)

    def draw(self):
        self.cur_state.draw(self)
        self.font.draw(self.cx - 60, self.cy + 50, '(hp: %d)' % self.hp, (255, self.hp*50, self.hp*50))