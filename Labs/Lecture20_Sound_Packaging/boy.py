import sys
import os

# PyInstaller 임시 폴더 경로 반환 함수
def resource_path(relative_path):
    """PyInstaller의 임시 폴더 경로를 반환"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

from pico2d import load_image, load_font, draw_rectangle, get_canvas_width, get_canvas_height, clamp
from sdl2 import SDL_KEYDOWN, SDLK_SPACE, SDLK_RIGHT, SDL_KEYUP, SDLK_LEFT, SDLK_UP, SDLK_DOWN

import common
import game_world
import game_framework

from state_machine import StateMachine


def space_down(e):  # e is space down ?
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE


def event_stop(e):
    return e[0] == 'STOP'

def event_run(e):
    return e[0] == 'RUN'


# Boy의 Run Speed 계산

# Boy Run Speed
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 20.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# Boy Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8


class Idle:

    def __init__(self, boy):
        self.boy = boy

    def enter(self, e):
        if event_stop(e):
            self.boy.face_dir = e[1] # 이전 방향 유지

    def exit(self, e):
        if space_down(e):
            self.boy.fire_ball()

    def do(self):
        self.boy.frame = (self.boy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
        # Removed timeout trigger for sleep.

    def draw(self):
        sx = self.boy.x - common.court.window_left
        sy = self.boy.y - common.court.window_bottom

        self.boy.font.draw(sx - 30, sy + 60, f'{self.boy.ball_count:03d}', (255, 255, 0))



        if self.boy.face_dir == 1:  # right
            self.boy.image.clip_draw(int(self.boy.frame) * 100, 300, 100, 100, sx, sy)
        else:  # face_dir == -1: # left
            self.boy.image.clip_draw(int(self.boy.frame) * 100, 200, 100, 100, sx, sy)


class Run:
    def __init__(self, boy):
        self.boy = boy

    def enter(self, e):
        if self.boy.xdir != 0:
            self.boy.face_dir = self.boy.xdir

    def exit(self, e):
        if space_down(e):
            self.boy.fire_ball()

    def do(self):
        self.boy.frame = (self.boy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
        self.boy.x += self.boy.xdir * RUN_SPEED_PPS * game_framework.frame_time
        self.boy.y += self.boy.ydir * RUN_SPEED_PPS * game_framework.frame_time


    def draw(self):
        sx = self.boy.x - common.court.window_left
        sy = self.boy.y - common.court.window_bottom
        self.boy.font.draw(sx - 30, sy + 60, f'{self.boy.ball_count:03d}', (255, 255, 0))


        if self.boy.xdir == 0: # 위 아래로 움직이는 경우
            if self.boy.face_dir == 1: # right
                self.boy.image.clip_draw(int(self.boy.frame) * 100, 100, 100, 100, sx, sy)
            else:
                self.boy.image.clip_draw(int(self.boy.frame) * 100, 0, 100, 100, sx, sy)
        elif self.boy.xdir == 1:
            self.boy.image.clip_draw(int(self.boy.frame) * 100, 100, 100, 100, sx, sy)
        else:
            self.boy.image.clip_draw(int(self.boy.frame) * 100, 0, 100, 100, sx, sy)




class Boy:
    def __init__(self):

        # self.font = load_font('ENCR10B.TTF', 30)
        self.font = load_font('ENCR10B.TTF', 30)

        # 물리 좌표계로 바꿔야 함.
        self.x, self.y = common.court.w / 2, common.court.h / 2
        self.ball_count = 0
        self.frame = 0
        self.face_dir = 1
        self.xdir, self.ydir = 0, 0

        self.image = load_image('animation_sheet.png')

        self.IDLE = Idle(self)
        self.RUN = Run(self)
        self.state_machine = StateMachine(
            self.IDLE,
            {
                self.IDLE: {event_run: self.RUN},
                self.RUN: {event_stop: self.IDLE}
            }
        )


    def update(self):
        self.state_machine.update()
        self.x = clamp(50.0, self.x, common.court.w - 50.0)
        self.y = clamp(50.0, self.y, common.court.h - 50.0)


    def handle_event(self, event):
        if event.key in (SDLK_LEFT, SDLK_RIGHT, SDLK_UP, SDLK_DOWN):
            cur_xdir, cur_ydir = self.xdir, self.ydir
            if event.type == SDL_KEYDOWN:
                if event.key == SDLK_LEFT: self.xdir -= 1
                elif event.key == SDLK_RIGHT: self.xdir += 1
                elif event.key == SDLK_UP: self.ydir += 1
                elif event.key == SDLK_DOWN: self.ydir -= 1
            elif event.type == SDL_KEYUP:
                if event.key == SDLK_LEFT: self.xdir += 1
                elif event.key == SDLK_RIGHT: self.xdir -= 1
                elif event.key == SDLK_UP: self.ydir -= 1
                elif event.key == SDLK_DOWN: self.ydir += 1
            if cur_xdir != self.xdir or cur_ydir != self.ydir: # 방향키에 따른 변화가 있으면
                if self.xdir == 0 and self.ydir  == 0: # 멈춤
                    self.state_machine.handle_state_event(('STOP', self.face_dir)) # 스탑 시 이전 방향 전달
                else: # 움직임
                    self.state_machine.handle_state_event(('RUN', None))
        else:
            self.state_machine.handle_state_event(('INPUT', event))


    def draw(self):
        self.state_machine.draw()

    # fill here
    def get_bb(self):
        return self.x - 20, self.y - 50, self.x + 20, self.y + 50

    def handle_collision(self, group, other):
        match group:
            case 'boy:ball':
                self.ball_count += 1