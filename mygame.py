import game_framework
import pico2d

import start_state
import stage0_state
import gameover_state
import stage1_state

pico2d.open_canvas(1024, 768)
game_framework.run(stage1_state)
pico2d.close_canvas()