import sys
import pygame
import os
import random
from map import Map
from utils import Utils
from bluedot import BlueDot


class Arkanoid:
    def __init__(self):
        self.bd = BlueDot()
        self.bd.when_pressed = self.dpad
        self.bd.set_when_moved(self.dpad, background=True)
        self.bd.set_when_released(self.dpad_stop, background = True)
        self.selected_map = 0
        self.delay_tick = 0
        self.moving = 0
        self.delay_input = False
        pygame.init()
        pygame.font.init()
        self.utils = Utils()
        self.state = self.utils.GameState.start_screen
        self.screen = pygame.display.set_mode(self.utils.screen_size)
        pygame.display.set_caption("Arkanoid")
        self.clock = pygame.time.Clock()
        self.menu_texture = pygame.image.load('textures/background.jpg')
        self.menu_texture = pygame.transform.scale(self.menu_texture, (self.utils.screen_width, self.utils.screen_height))
        self.win_texture = pygame.image.load('textures/win.png')
        self.win_texture = pygame.transform.scale(self.win_texture, (self.utils.screen_width, self.utils.screen_height))
        self.lose_texture = pygame.image.load('textures/lose.png')
        self.lose_texture = pygame.transform.scale(self.lose_texture, (self.utils.screen_width, self.utils.screen_height))
        if pygame.font:
            self.font = pygame.font.Font("font/redline.ttf", 54)
            self.font_menu = pygame.font.Font("font/redline.ttf", 30)
        else:
            self.font = None

    def init_game(self):
        self.lives = self.map.lives
        self.score = 0
        self.state = self.utils.GameState.out_of_area
        self.racket = pygame.Rect(200, self.utils.padding_y_pos, 150, 20)
        self.ball = [pygame.Rect(150, self.utils.padding_y_pos - self.utils.ball_radius, self.utils.ball_diameter, self.utils.ball_diameter)]

    def load_map(self, file):
        self.map = Map()
        self.map.load_map(file)
        self.velocity = [self.map.ball_velocity, -self.map.ball_velocity]
        self.utils.set_game_values(self.map.bricks_amount_x, self.map.bricks_amount_y)
        self.map.brick_texture = pygame.transform.scale(self.map.brick_texture, (self.utils.brick_width, self.utils.brick_height))
        self.map.ball_texture = pygame.transform.scale(self.map.ball_texture, (self.utils.ball_diameter, self.utils.ball_diameter))
        self.map.powerup_texture = pygame.transform.scale(self.map.powerup_texture,
                                                       (self.utils.ball_diameter, self.utils.ball_diameter))
        self.map.racket_texture = pygame.transform.scale(self.map.racket_texture, (150, 20))
        self.utils.racket_velocity = int(self.map.ball_velocity*1.2)
        self.racket_size = 150
        self.create_bricks()
        self.init_game()

    def create_bricks(self):
        y_ofs = self.utils.padding
        self.bricks = []
        self.powerups = []
        for brick_row in self.map.bricks_array:
            x_ofs = self.utils.padding
            for b in brick_row:
                if b:
                    self.bricks.append(pygame.Rect(x_ofs, y_ofs, self.utils.brick_width, self.utils.brick_height))
                x_ofs += self.utils.brick_width + 10
            y_ofs += self.utils.brick_height + 5

    def draw_bricks(self):
        for brick in self.bricks:
            self.screen.blit(self.map.brick_texture, brick)

    def dpad(self, pos):
        if self.state == self.utils.GameState.start_screen:
            if self.delay_input and pygame.time.get_ticks() - self.delay_tick > 300:
                self.delay_input = False
                self.delay_tick = 0
            if pos.bottom:
                if not self.delay_input:
                    self.selected_map += 1
                    self.delay_input = True
                    self.delay_tick = pygame.time.get_ticks()
                    if self.selected_map > self.utils.maps_amount - 1:
                        self.selected_map = 0
            if pos.top:
                if not self.delay_input:
                    self.selected_map -= 1
                    self.delay_input = True
                    self.delay_tick = pygame.time.get_ticks()
                    if self.selected_map < 0:
                        self.selected_map = self.utils.maps_amount - 1
            if pos.middle:
                if not self.delay_input:
                    self.delay_input = True
                    self.delay_tick = pygame.time.get_ticks()
                    self.load_map(self.utils.files[self.selected_map])
                    self.state = self.utils.GameState.out_of_area

        if pos.left:
            self.moving = -1
            self.racket.left -= self.utils.racket_velocity
            if self.racket.left <= 0:
                self.racket.left = 0
        elif pos.right:
            self.moving = 1
            self.racket.left += self.utils.racket_velocity
            if self.racket.right > self.utils.screen_width:
                self.racket.right = self.utils.screen_width
        else:
            self.moving = 0
        if pos.top and self.state == self.utils.GameState.out_of_area:
            self.ball_vel = [self.map.ball_velocity, -self.map.ball_velocity]
            self.state = self.utils.GameState.playing

        if self.state == self.utils.GameState.win or self.state == self.utils.GameState.game_over and pos.middle:
            self.state = self.utils.GameState.start_screen
            self.delay_input = True
            self.delay_tick = pygame.time.get_ticks()
    def dpad_stop(self, pos):
        self.moving = 0

    def dpad_loop(self):
        if self.moving == -1:
            self.racket.left -= self.utils.racket_velocity
            if self.racket.left <= 0:
                self.racket.left = 0

        if self.moving == 1:
            self.racket.left += self.utils.racket_velocity
            if self.racket.right > self.utils.screen_width:
                self.racket.right = self.utils.screen_width

    def keyboard_input(self):
        keys = pygame.key.get_pressed()
        if self.state == self.utils.GameState.start_screen:
            '''for i in range(1, 10):
                if keys[48 + i] and i <= self.utils.maps_amount:
                    self.load_map(self.utils.files[i-1])
                    self.state = self.utils.GameState.out_of_area'''
            if self.delay_input and pygame.time.get_ticks() - self.delay_tick > 500:
                self.delay_input = False
                self.delay_tick = 0
            if keys[pygame.K_DOWN]:
                if not self.delay_input:
                    self.selected_map+=1
                    self.delay_input = True
                    self.delay_tick = pygame.time.get_ticks()
                    if self.selected_map> self.utils.maps_amount-1:
                        self.selected_map=0
            if keys[pygame.K_UP]:
                if not self.delay_input:
                    self.selected_map -= 1
                    self.delay_input = True
                    self.delay_tick = pygame.time.get_ticks()
                    if self.selected_map < 0:
                        self.selected_map = self.utils.maps_amount-1
            if keys[pygame.K_SPACE]:
                self.load_map(self.utils.files[self.selected_map])
                self.state = self.utils.GameState.out_of_area

        if keys[pygame.K_LEFT]:
            self.racket.left -= self.utils.racket_velocity
            if self.racket.left <= 0:
                self.racket.left = 0

        if keys[pygame.K_RIGHT]:
            self.racket.left += self.utils.racket_velocity
            if self.racket.right > self.utils.screen_width:
                self.racket.right = self.utils.screen_width

        if keys[pygame.K_SPACE] and self.state == self.utils.GameState.out_of_area:
            self.ball_vel = [self.map.ball_velocity, -self.map.ball_velocity]
            self.state = self.utils.GameState.playing
        elif keys[pygame.K_RETURN] and (self.state == self.utils.GameState.game_over or self.state == self.utils.GameState.win):
            self.init_game()
            self.create_bricks()
        if keys[pygame.K_q]:
            sys.exit()
        if keys[pygame.K_m]:
                self.state = self.utils.GameState.start_screen

    def move_ball(self):
        ball_n = -2
        for ball in self.ball:
            ball_n += 2
            ball.left += self.velocity[ball_n + 0]
            ball.top -= self.velocity[ball_n + 1]

            if ball.left <= 0:
                ball.left = 0
                self.velocity[ball_n + 0] = -self.velocity[ball_n + 0]
            elif ball.left >= self.utils.max_ball_x:
                ball.left = self.utils.max_ball_x
                self.velocity[ball_n + 0] = -self.velocity[ball_n + 0]

            if ball.top < 0:
                ball.top = 0
                self.velocity[ball_n + 1] = -self.velocity[ball_n + 1]
            elif ball.top >= self.utils.max_ball_y:
                ball.top = self.utils.max_ball_y
                self.velocity[ball_n + 1] = -self.velocity[ball_n + 1]

    def handle_collisions(self):
        ball_n = -2
        for ball in self.ball:
            ball_n += 2
            for brick in self.bricks:
                collision = [False] *8
                hit = False
                if ball.colliderect(brick):
                    collision[0] = brick.collidepoint(ball.topleft)
                    collision[1] = brick.collidepoint(ball.topright)
                    collision[2] = brick.collidepoint(ball.bottomleft)
                    collision[3] = brick.collidepoint(ball.bottomright)

                    collision[4] = brick.collidepoint(ball.midleft)
                    collision[5] = brick.collidepoint(ball.midright)
                    collision[6] = brick.collidepoint(ball.midtop)
                    collision[7] = brick.collidepoint(ball.midbottom)

                    if collision[6] or collision[7]:
                        self.velocity[ball_n + 1] = -self.velocity[ball_n + 1]
                        hit = True
                    if collision[4] or collision[5]:
                        self.velocity[ball_n + 0] = -self.velocity[ball_n + 0]
                        hit = True
                    if hit:
                        self.score += 10
                        if random.randint(0,10) >= 9:
                            self.drop_powerup(brick)
                        self.bricks.remove(brick)
                        break
                    else:
                        continue


        if len(self.bricks) == 0:
            self.state = self.utils.GameState.win

        if len(self.ball)== 1:
            if self.ball[0].colliderect(self.racket):
                self.ball[0].top = self.utils.padding_y_pos - self.utils.ball_diameter
                self.velocity[1] = -self.velocity[1]
            elif self.ball[0].top > self.racket.top:
                self.lives -= 1
                if self.lives > 0:
                    self.state = self.utils.GameState.out_of_area
                else:
                    self.state = self.utils.GameState.game_over
        else:
            ball_n = -2
            for ball in self.ball:
                ball_n += 2
                if ball.colliderect(self.racket):
                    ball.top = self.utils.padding_y_pos - self.utils.ball_diameter
                    self.velocity[ball_n + 1] = -self.velocity[ball_n + 1]
                elif ball.top > self.racket.top:
                    if len(self.ball)>1:
                        self.ball.remove(ball)
                        self.velocity.pop(ball_n)
                        self.velocity.pop(ball_n)


    def handle_powerup_collisions(self):
        for powerup in self.powerups:
            if powerup.colliderect(self.racket):
                self.score+=20
                self.powerups.remove(powerup)
                random_int = random.randint(0, 10)
                #new ball
                if random_int <= 4:
                    self.ball.append(pygame.Rect(self.ball[0].left,self.ball[0].top, self.utils.ball_diameter, self.utils.ball_diameter))
                    self.velocity.append(self.map.ball_velocity * (1 + random.randint(-3,3) / 10))
                    self.velocity.append(-self.map.ball_velocity * (1 + random.randint(-3,3) / 10))
                #longer racket
                elif random_int <= 8:
                    if self.racket_size <= 400:
                        self.racket_size += 50
                        self.racket = pygame.Rect(self.racket.left, self.racket.top, self.racket_size , 20)
                        self.map.racket_texture = pygame.transform.scale(self.map.racket_texture, (self.racket_size, 20))
                    else:
                        self.score += 100
                #+1 life
                else:
                    self.lives += 1
    def drop_powerup(self, brick):
        powerup = pygame.Rect(brick.left + brick.width/2 , brick.top, self.utils.ball_diameter, self.utils.ball_diameter)
        self.powerups.append(powerup)
    def move_powerups(self):
        for powerup in self.powerups:
            powerup.top += self.map.ball_velocity/2
            if powerup.top < 0:
                self.powerups.remove(powerup)
    def draw_powerups(self):
        for powerup in self.powerups:
            self.screen.blit(self.map.powerup_texture, (powerup.left, powerup.top))
    def show_stats(self):
        if self.font:
            text = "SCORE: " + str(self.score) + "    LIVES: " + str(self.lives)
            font_surface = self.font.render(text , False, self.map.font_color)
            self.screen.blit(font_surface, (self.utils.screen_width//2 - self.font.size(text)[0]//2, 10))

    def start_screen(self):
        self.screen.blit(self.menu_texture, (0, 0))
        text_height = int(self.font_menu.size("1")[1]*1.3)
        font_surface = self.font.render("Choose map number: ", False, (255, 255, 255))
        self.screen.blit(font_surface, (self.utils.screen_width//2 - self.font.size("Choose map number: ")[0]//2, text_height))
        map_num = 1
        for file in self.utils.files:
            name = os.path.splitext(os.path.basename(file))
            if map_num-1 == self.selected_map:
                font_surface = self.font_menu.render("* " + str(map_num) + ": " + name[0] + " *", False, (255, 255, 255))
            else:
                font_surface = self.font_menu.render(str(map_num) + ": " + name[0], False, (255, 255, 255))
            self.screen.blit(font_surface, (self.utils.screen_width//2 - self.font_menu.size(str(map_num) + ": " + name[0])[0]//2, text_height*(map_num + 2)))
            map_num = map_num + 1

    def win_screen(self):
        self.screen.blit(self.map.background_texture, (0, 0))
        self.screen.blit(self.win_texture, (0, 0))

    def lose_screen(self):
        self.screen.blit(self.map.background_texture, (0, 0))
        self.screen.blit(self.lose_texture, (0, 0))

    def game_screen(self):
        self.screen.blit(self.map.background_texture, (0, 0))
        for ball in self.ball:
            self.screen.blit(self.map.ball_texture, (ball.left, ball.top))
        self.screen.blit(self.map.racket_texture, (self.racket.left, self.racket.top))
        self.draw_bricks()
        self.draw_powerups()
        self.show_stats()

    def start(self):
        while 1:
            self.clock.tick(50)
            self.screen.fill((0, 0, 0))
            self.keyboard_input()
            self.dpad_loop()
            if self.state == self.utils.GameState.start_screen:
                self.start_screen()
            elif self.state == self.utils.GameState.win:
                self.win_screen()
            elif self.state == self.utils.GameState.game_over:
                self.lose_screen()
            else:
                self.move_powerups()
                self.handle_powerup_collisions()
                if self.state == self.utils.GameState.playing:
                    self.move_ball()
                    self.handle_collisions()
                elif self.state == self.utils.GameState.out_of_area:
                    for ball in self.ball:
                        ball.left = self.racket.left + self.racket.width / 2
                        ball.top = self.racket.top - ball.height
                self.game_screen()
            pygame.event.pump()
            pygame.display.flip()
