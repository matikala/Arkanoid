import ast
import json
import pygame


class Map:
    def __init__(self):
        self.name = None
        self.bricks_amount_x = None
        self.bricks_amount_y = None
        self.bricks_array = None
        self.lives = None
        self.ball_velocity = None
        self.font_color = None
        self.font = None
        self.background_path = None
        self.background_texture = None
        self.racket_path = None
        self.racket_texture = None
        self.ball_path = None
        self.ball_texture = None
        self.brick_path = None
        self.brick_texture = None
        self.powerup_path = None
        self.powerup_texture = None

    def load_map(self, file):
        self.clear_map()
        with open(file, 'r') as json_file:
            data = json.load(json_file)
            self.name = data["name"]
            self.bricks_amount_x = data["bricks_amount_x"]
            self.bricks_amount_y = data["bricks_amount_y"]
            self.bricks_array = data["bricks_array"]
            self.background_path = data["background_texture"]
            self.background_texture = pygame.image.load('maps/' + self.background_path).convert()
            self.racket_path = data["racket_texture"]
            self.racket_texture = pygame.image.load('maps/' + self.racket_path)
            self.ball_path = data["ball_texture"]
            self.ball_texture = pygame.image.load('maps/' + self.ball_path)
            self.brick_path = data["brick_texture"]
            self.brick_texture = pygame.image.load('maps/' + self.brick_path).convert()
            self.powerup_path = data["powerup_texture"]
            self.powerup_texture = pygame.image.load('maps/' + self.powerup_path)
            self.lives = data['lives']
            self.ball_velocity = data['ball_velocity']
            self.font_color = ast.literal_eval(data['font_color'])
            if "font" in data:
                self.font = data["font"]
            else:
                self.font = None

    def clear_map(self):
        self.name = None
        self.bricks_amount_x = None
        self.bricks_amount_y = None
        self.bricks_array = None
        self.background_path = None
        self.racket_path = None
        self.ball_path = None
        self.brick_path = None
        self.background_texture = None
        self.racket_texture = None
        self.ball_texture = None
        self.brick_texture = None
        self.lives = None
        self.ball_velocity = None
        self.font_color = None
        self.font = None
