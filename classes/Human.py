from gameconfig import *;

import arcade, math;
from arcade import check_for_collision_with_list;

class Human(arcade.Sprite):
    def __init__(self):
        super().__init__("./images/Human.png", CHRACTER_SCALING)
        self.circle_angle = 0
        self.circle_radius = 0
        self.circle_speed = 0.008
        self.circle_center_x = 0
        self.circle_center_y = 0
        # self.center_x = 100
        # self.center_y = 100
        self.speed = HUMAN_SPEED
        
    # def movement(self, x):
    #     self.center_x += x

    def update(self):
        self.center_x = self.circle_radius * math.sin(self.circle_angle) \
            + self.circle_center_x
        self.center_y = self.circle_radius * math.cos(self.circle_angle) \
            + self.circle_center_y
        self.circle_angle += self.circle_speed
        self.check_boundary_collision(SCREEN_WIDTH, SCREEN_HEIGHT)

    def collides_with_list(self, sprite_list):
        return check_for_collision_with_list(self, sprite_list)
    
    def check_boundary_collision(self, screen_width, screen_height):
        if self.right > screen_width:
            self.right = screen_width
            return True
        elif self.left < 3*BLOCK_SIZE:
            self.left = 3*BLOCK_SIZE
            return True
        if self.top > screen_height - BLOCK_SIZE:
            self.top = screen_height - BLOCK_SIZE
            return True
        elif self.bottom < 0:
            self.bottom = 0
            return True
        return False