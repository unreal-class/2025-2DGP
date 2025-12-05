from pico2d import load_image, get_canvas_width, get_canvas_height, clamp, load_music
import common

class Court:
    def __init__(self):
        self.image = load_image('futsal_court.png')
        self.cw = get_canvas_width()
        self.ch = get_canvas_height()
        self.w = self.image.w
        self.h = self.image.h
        # fill here


    def update(self):
        self.window_left = clamp(0, int(common.boy.x) - self.cw // 2, self.w - self.cw - 1)
        self.window_bottom = clamp(0, int(common.boy.y) - self.ch // 2, self.h - self.ch - 1)

    def draw(self):
        self.image.clip_draw_to_origin(self.window_left, self.window_bottom, self.cw, self.ch, 0, 0)


