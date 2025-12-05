import random

from pico2d import *
import game_framework


import game_world
import common

from boy import Boy
# from court import Court
# from court import TileCourt as Court
from court import Court
from ball import Ball


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()

        else:
            common.boy.handle_event(event)


def init():
    common.court = Court()
    game_world.add_object(common.court, 0)

    common.boy = Boy()
    game_world.add_object(common.boy, 1)
    game_world.add_collision_pair('boy:ball', common.boy, None)

    for _ in range(100):
        ball = Ball()
        game_world.add_object(ball, 1)
        game_world.add_collision_pair('boy:ball', None, ball)

def finish():
    game_world.clear()
    pass


def update():
    game_world.update()
    game_world.handle_collisions()

def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def pause():
    pass

def resume():
    pass

