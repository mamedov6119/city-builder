from collections import deque;
from gameconfig import *;

# import gui.window as w;
import arcade, math, random;
import gameconfig as gc;
from logic.variables import v;
from arcade import check_for_collision_with_list;
import numpy as np;

class Human(arcade.Sprite):
    def __init__(self, x=0, y=0, path=[]):
        super().__init__("./images/Human.png", CHRACTER_SCALING)
        # self.circle_center_x = x+BLOCK_SIZE//2 # random.randrange(150, 700)
        # self.circle_center_y = y+BLOCK_SIZE//2 # random.randrange(150, 700)
        # self.circle_radius = random.randrange(10, 200)
        # self.circle_angle = random.random() * 2 * math.pi
        self.satisfaction = 100
        # self.center_x = x * BLOCK_SIZE + BLOCK_SIZE * 4
        # self.center_y = y * BLOCK_SIZE + BLOCK_SIZE//2
        # print(x, y)
        self.speed = HUMAN_SPEED * v.speed
        self.center_x, self.center_y = x, y  # Start position
        self.pos_list = sorted([[p[0]*BLOCK_SIZE+BLOCK_SIZE*3.5, p[1]*BLOCK_SIZE+BLOCK_SIZE//2] for p in path], key=lambda pos : (pos[0], pos[1])) #[[p.x*BLOCK_SIZE+BLOCK_SIZE*3.5, p.y*BLOCK_SIZE+BLOCK_SIZE//2] for p in building_sprites]
        print(path)
        self.cur_pos = 0
        self.center_x, self.center_y = self.pos_list[self.cur_pos]
        humans_sprites.append(self)

    def update(self):
        # print(pos_list)
        start_x = self.center_x
        start_y = self.center_y

        dest_x, dest_y = self.pos_list[self.cur_pos]

        x_diff = dest_x - start_x
        y_diff = dest_y - start_y

        angle = math.atan2(y_diff, x_diff)

        distance = math.sqrt((self.center_x - dest_x) ** 2 + (self.center_y - dest_y) ** 2)

        # How fast should we go? If we are close to our destination,
        # lower our speed so we don't overshoot.
        speed = min(random.uniform(0.2, 2.0), distance)

        change_x = math.cos(angle) * speed
        change_y = math.sin(angle) * speed

        self.center_x += change_x
        self.center_y += change_y

        distance = math.sqrt((self.center_x - dest_x) ** 2 + (self.center_y - dest_y) ** 2)

        # Reached the end of the list, start over.
        if distance <= self.speed:
            self.cur_pos += 1
            # Reached the end of the list, start over.
            if self.cur_pos >= len(self.pos_list):
                self.cur_pos = 0
                self.pos_list = self.pos_list[::-1]
        
        

    def collides_with_list(self, sprite_list):
        return check_for_collision_with_list(self, sprite_list)
    
    