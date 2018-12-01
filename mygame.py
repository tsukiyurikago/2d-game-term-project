import game_framework
import pico2d

import start_state
import main_state

pico2d.open_canvas(1024, 768)
game_framework.run(start_state)
pico2d.close_canvas()