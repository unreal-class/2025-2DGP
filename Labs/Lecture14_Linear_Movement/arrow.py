import random

from pico2d import *

import game_world

class Arrow:
    def __init__(self):
        self.image = load_image('hand_arrow.png')
        self.reset_position()

    def reset_position(self):
        self.x, self.y = random.randint(100, 1280-100), random.randint(100, 1024-100)

    def update(self):
        pass

    def get_bb(self):
        return self.x - 5, self.y - 5, self.x + 5, self.y + 5

    def draw(self):
        self.image.draw(self.x+25, self.y-25)

    def handle_collision(self, group, other):
        pass