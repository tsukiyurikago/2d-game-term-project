from pico2d import *
import game_world
import game_framework

class Bullet:
    image = None

    def __init__(self, x = 400, y = 300, angle = 0.0, speed = 0.0):
        if Bullet.image == None:
            Bullet.image = load_image('testbullet.png')
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = speed
        self.name = 1
        self.cx = 0.0
        self.cy = 0.0

    def draw(self):
        self.image.rotate_draw(self.angle, self.cx, self.cy, 16, 16)

    def set_center_object(self, boy):
        self.center_object = boy

    def update(self):
        self.y += math.cos(self.angle) * self.speed * game_framework.frame_time
        self.x += -math.sin(self.angle) * self.speed * game_framework.frame_time
        self.cx, self.cy = self.x - self.center_object.bg.window_left, self.y - self.center_object.bg.window_bottom

        if self.x < 0 or self.x > 2048 or self.y < 0 or self.y > 2048:
            game_world.remove_object(self)

