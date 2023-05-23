from gameconfig import *;
import arcade, math, random;
from logic.variables import v;

class Human(arcade.Sprite):
    def __init__(self, x=0, y=0, path=[], satisfaction=100):
        super().__init__("./images/Human.png", CHRACTER_SCALING)
        self.satisfaction = satisfaction
        self.center_x, self.center_y = x, y 
        if len(path) > 0:
            self.pos_list = sorted([[p[0]*BLOCK_SIZE+BLOCK_SIZE*3.5, p[1]*BLOCK_SIZE+BLOCK_SIZE//2] for p in path], key=lambda pos : (pos[0], pos[1])) #[[p.x*BLOCK_SIZE+BLOCK_SIZE*3.5, p.y*BLOCK_SIZE+BLOCK_SIZE//2] for p in building_sprites]
        else: self.pos_list = [(x,y)]
        self.cur_pos = 0
        self.center_x, self.center_y = self.pos_list[self.cur_pos]
        humans_sprites.append(self)

    def update(self):
        
        start_x = self.center_x
        start_y = self.center_y

        dest_x, dest_y = self.pos_list[self.cur_pos]

        x_diff = dest_x - start_x
        y_diff = dest_y - start_y

        angle = math.atan2(y_diff, x_diff)

        distance = math.sqrt((self.center_x - dest_x) ** 2 + (self.center_y - dest_y) ** 2)

        
        speed = min(random.uniform(0.2, 2.0), distance) * v.speed

        change_x = math.cos(angle) * speed  
        change_y = math.sin(angle) * speed  

        self.center_x += change_x
        self.center_y += change_y

        distance = math.sqrt((self.center_x - dest_x) ** 2 + (self.center_y - dest_y) ** 2)

        if distance <= speed:
            self.cur_pos += 1
            if self.cur_pos >= len(self.pos_list):
                self.cur_pos = 0
                self.pos_list = self.pos_list[::-1]

        self.satisfaction -= 0.001 * v.speed
        

    def inc(self):
        self.satisfaction += 1
        if self.satisfaction > 100:
            self.satisfaction = 100
    
    def dec(self):
        self.satisfaction -= 1
        if self.satisfaction < 0:
            self.satisfaction = 0
    
    