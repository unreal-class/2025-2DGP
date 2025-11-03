from pico2d import *
import game_world
import game_framework

PIXEL_PER_METER = (1.0 / 0.03)  # 1pixel = 3cm, 1m = 33.33 pixel
GRAVITY = 9.8  # 중력 가속도 (m/s²)

class Ball:
    image = None

    def __init__(self, x = 400, y = 300, throwin_speed = 15, throwin_angle = 45):
        if Ball.image == None:
            Ball.image = load_image('ball21x21.png')
        self.x, self.y = x, y
        self.xv = throwin_speed * math.cos(math.radians(throwin_angle))  # m/s
        self.yv = abs(throwin_speed * math.sin(math.radians(throwin_angle)))   # m/s
        self.stopped = True if throwin_speed == 0.0 else False

    def draw(self):
        self.image.draw(self.x, self.y)

    def update(self):
        if self.stopped:
            return
        # 위치 업데이트
        self.x += self.xv * game_framework.frame_time * PIXEL_PER_METER
        self.y += self.yv * game_framework.frame_time * PIXEL_PER_METER

        # y 축 속도에 중력 가속도 적용
        self.yv -= GRAVITY * game_framework.frame_time  # m/s



