import enum
from glob import glob
import os


class Utils:
    def __init__(self):
        self.screen_size = (1280, 720)
        self.screen_width = self.screen_size[0]
        self.screen_height = self.screen_size[1]
        self.padding = 0.05 * self.screen_width
        script_location = os.getcwd()
        folder_name = 'maps/'
        self.files = glob(script_location + '/' + folder_name + '*.json')
        self.maps_amount = len(self.files)
        self.brick_width = None
        self.brick_height = None
        self.ball_diameter = None
        self.ball_radius = None
        self.padding_x_pos = None
        self.padding_y_pos = None
        self.max_ball_x = None
        self.max_ball_y = None
        self.racket_velocity = None

    def set_game_values(self, bricks_amount_x, bricks_amount_y):
        self.brick_width = int((self.screen_width - 2*self.padding - (bricks_amount_x-1)*10) / bricks_amount_x)
        self.brick_height = int((0.6*self.screen_height - 2*self.padding) // bricks_amount_y)
        self.ball_diameter = self.screen_width // 50
        self.ball_radius = self.ball_diameter // 2
        self.padding_x_pos = self.screen_width - self.padding
        self.padding_y_pos = self.screen_height - self.padding
        self.max_ball_x = self.screen_width - self.ball_diameter
        self.max_ball_y = self.screen_height - self.ball_diameter

    class GameState(enum.Enum):
        out_of_area = 0
        playing = 1
        win = 2
        game_over = 3
        start_screen = 4
