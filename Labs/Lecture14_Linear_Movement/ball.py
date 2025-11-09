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

    def draw(self):
        self.image.draw(self.x, self.y)
        draw_rectangle(*self.get_bb())

    def update(self):
        # 위치 업데이트
        self.x += self.xv * game_framework.frame_time * PIXEL_PER_METER
        self.y += self.yv * game_framework.frame_time * PIXEL_PER_METER

        # y 축 속도에 중력 가속도 적용
        self.yv -= GRAVITY * game_framework.frame_time  # m/s

    def stop(self):
        self.xv, self.yv = 0.0, 0.0
        game_world.remove_collision_pair('zombie:ball', None, self)


    # fill here
    def get_bb(self):
        return self.x - 10, self.y - 10, self.x + 10, self.y + 10

    # fill here
    def handle_collision(self, group, other):
        match group:
            case 'boy:ball':
                game_world.remove_object(self)
            case 'grass:ball':
                # 바닥에 닿으면 공 움직임 멈춤
                self.stop()
            case 'zombie:ball':
                game_world.remove_object(self)