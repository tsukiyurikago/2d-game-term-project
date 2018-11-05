from pico2d import *
import game_framework
import game_world

class Wall:
    image = None

    def __init__(self, x1, y1, x2, y2, type = 0):
        if Wall.image == None:
            #Wall.image = load_image('ball21x21.png')
            pass
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.type = type
        self.name = 3

    def draw(self):
        #self.image.draw(self.x, self.y)
        pass

    def update(self):
        for o in game_world.objects[1]:
            if o.name != 3:
                if self.type == 1:
                    if o.y > self.x1 and o.y < self.x2:
                        if o.y <= self.y1 and o.y + math.cos(o.angle) * o.speed * game_framework.frame_time >= self.y1:
                            o.y = self.y1 - 2.0

                elif self.type == 2:
                    pass
                elif self.type == 3:
                    pass
                elif self.type == 4:
                    pass