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

    def draw(self):
        self.image.rotate_draw(self.angle, self.x, self.y, 16, 16)

    def update(self):
        self.y += math.cos(self.angle) * self.speed * game_framework.frame_time
        self.x += -math.sin(self.angle) * self.speed * game_framework.frame_time

        if self.x < 0 or self.x > 1024 or self.y < 0 or self.y > 768:
            game_world.remove_object(self)

