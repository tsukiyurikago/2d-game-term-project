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
            if o.name != 3:
                t=0.0
                s=0.0
                pass