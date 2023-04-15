from gameconfig import *;

import arcade;

class Building(arcade.Sprite):
    def __init__(self, filename, building_scaling):
        super().__init__("./images/" + filename, building_scaling)

    def place(self,x,y):
        self.center_x = (BLOCK_SIZE*2) 
        self.center_y = BLOCK_SIZE*10

class PowerPlant(Building):
    def __init__(self):
        super().__init__("PowerPlant.png", 0.5)
