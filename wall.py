from pico2d import *
import game_framework
import game_world

class Wall:
    image = None

    def __init__(self, x1, y1, x2, y2):
        if Wall.image == None:
            #Wall.image = load_image('ball21x21.png')
            pass
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.name = 3

    def draw(self):
        #self.image.draw(self.x, self.y)
        pass

    def update(self):
        for o in game_world.objects[1]:
            if o.name == 2 or (o.name == 0 and o.super == False):
                if o.x+(o.size/2)>self.x1 and o.x-(o.size/2) < self.x2 and o.y+(o.size/2)>self.y1 and o.y-(o.size/2) <self.y2:
                    if o.x < self.x1 and o.y > self.y1 - (o.size/2) + 1 and o.y < self.y2 + (o.size/2) - 1:
                        o.x = self.x1 - (o.size/2) - 1
                    if o.x > self.x2 and o.y > self.y1 - (o.size/2) + 1 and o.y < self.y2 + (o.size/2) - 1:
                        o.x = self.x2 + (o.size/2) + 1
                    if o.y < self.y1 and o.x > self.x1 - (o.size/2) + 1 and o.x < self.x2 + (o.size/2) - 1:
                        o.y = self.y1 - (o.size/2) - 1
                    if o.y > self.y2 and o.x > self.x1 - (o.size/2) + 1 and o.x < self.x2 + (o.size/2) - 1:
                        o.y = self.y2 + (o.size/2) + 1
            elif o.name == 1:
                if o.x>self.x1 and o.x < self.x2 and o.y>self.y1 and o.y <self.y2:
                    game_world.remove_object(o)

                pass