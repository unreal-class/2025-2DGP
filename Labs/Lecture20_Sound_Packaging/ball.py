import random

from pico2d import *
import game_world

import common

class Ball:
    image = None
    boy_eat_sound = None

    def __init__(self, x = None, y = None):
        if Ball.image == None:
            Ball.image = load_image('ball21x21.png')
        self.x = x if x else random.randint(100, common.court.w - 100)
        self.y = y if y else random.randint(100, common.court.h - 100)

        # fill here


    def draw(self):
        self.image.draw(self.x - common.court.window_left, self.y - common.court.window_bottom)

    def update(self):
        pass

    def get_bb(self):
        return self.x - 10, self.y - 10, self.x + 10, self.y + 10

    def handle_collision(self, group, other):
        if group == 'boy:ball':
            # fill here
            game_world.remove_object(self)
