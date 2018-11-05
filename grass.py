from pico2d import *

class Grass:
    def __init__(self):
        self.image = load_image('testbg.png')

    def update(self):
        pass

    def draw(self):
        self.image.draw(512, 384)
