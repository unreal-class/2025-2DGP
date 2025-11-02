from pico2d import *
import game_framework
import play_mode

image = None

def init():
    global image
    image = load_image('title.png')

def finish():
    global image
    del image

def handle_events():
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
            game_framework.change_mode(play_mode)

def draw():
    clear_canvas()
    image.draw(400,300)
    update_canvas()

def update(): pass
def pause(): pass
def resume(): pass





