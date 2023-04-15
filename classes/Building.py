from gameconfig import *;

import arcade;

class Building(arcade.Sprite):
    def __init__(self, filename, building_scaling, dim):
        super().__init__("./images/" + filename, building_scaling)
        self.dim = dim

    def place(self,x,y):
        # print(f"x:{x}, y:{y}. BX:{x*BLOCK_SIZE}, BY:{y*BLOCK_SIZE}")
        self.center_x = ((x+3)*BLOCK_SIZE + (self.dim)*BLOCK_SIZE/2)
        self.center_y = ((y+1)*BLOCK_SIZE - (self.dim)*BLOCK_SIZE/2)

    def append(self):
        building_sprites.append(self)
    

class PowerPlant(Building):
    def __init__(self, x=0, y=0):
        super().__init__("PowerPlant.png", 0.5, 2)
        self.place(x,y)
        self.append()
