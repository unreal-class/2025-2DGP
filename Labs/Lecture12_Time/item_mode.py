from pico2d import *

import game_world
import game_framework
import play_mode
from pannel import Pannel

pannel = None

def init():
    global pannel
    pannel = Pannel()
    game_world.add_object(pannel, 2)

def finish():
    global pannel
    game_world.remove_object(pannel)
    del pannel

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                game_framework.pop_mode()
            elif event.key == SDLK_0:
                play_mode.boy.item = None
                game_framework.pop_mode()
            elif event.key == SDLK_1:
                play_mode.boy.item = 'Ball'
                game_framework.pop_mode()
            elif event.key == SDLK_2:
                play_mode.boy.item = 'BigBall'
                game_framework.pop_mode()



def draw():
    clear_canvas()
    game_world.render()
    update_canvas()


def update():
    game_world.update()

def pause():
    pass

def resume():
    pass

