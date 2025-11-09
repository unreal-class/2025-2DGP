import random
from pico2d import *

import game_framework
import game_world

from arrow import Arrow
from boy import Boy
from ground import Ground
from ball import Ball
from zombie import Zombie

boy = None
zombie = None

def handle_events():
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            boy.handle_event(event)

def init():
    global boy
    global arrow

    ground = Ground()
    game_world.add_object(ground, 0)

    boy = Boy()
    game_world.add_object(boy, 1)

    zombie = Zombie()
    game_world.add_object(zombie, 1)





def update():
    game_world.update()
    game_world.handle_collisions()


def draw():
    clear_canvas()
    game_world.render()
    update_canvas()


def finish():
    game_world.clear()

def pause(): pass
def resume(): pass

