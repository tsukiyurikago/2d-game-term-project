from pico2d import *
import game_framework
import game_world
import math

# Ghost Run Speed
PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_KMPH = 20.0 #km.hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# Ghost Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8

class Ghost:
    image = None

    def __init__(self, x = 400, y = 300, dir = 1):
        if Ghost.image == None:
            self.image = load_image('animation_sheet.png')
        self.frame = 0
        self.x = x
        self.y = y
        self.angle = -90.0
        self.dir = dir

    def draw(self):
        self.image.opacify(math.cos((self.angle - 90.0) * 3.14 / 360)*0.5 + 0.5)
        if self.dir == 1:
            self.image.clip_draw(int(self.frame) * 100, 300, 100, 100, 100.0 * math.cos(self.angle * 3.14 / 180) + self.x - 25, 100.0 * math.sin(self.angle * 3.14 / 180) + self.y + 100)
        else:
            self.image.clip_draw(int(self.frame) * 100, 200, 100, 100, 100.0 * math.cos(self.angle * 3.14 / 180) + self.x + 25, 100.0 * math.sin(self.angle * 3.14 / 180) + self.y + 100)

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
        self.angle += game_framework.frame_time * 720.0
        if self.angle > 630.0 :
            self.angle = -90.0 ##실수 자료형에서는 %연산이가능한지 몰라서 if로 값을 반복해서 바꿨씁니다

        if self.x < 25 or self.x > 1600 - 25:
            game_world.remove_object(self)
