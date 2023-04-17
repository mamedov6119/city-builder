from gameconfig import *;

import arcade, random;


class Meteor(arcade.Sprite):


    def __init__(self, dim=2):
        super().__init__("./images/Meteor.png", image_width=BLOCK_SIZE*dim, image_height=BLOCK_SIZE*dim)
        self.center_x = BLOCK_SIZE
        self.center_y = BLOCK_SIZE
        self.dim = dim
        self.angle = random.randrange(0, 360)
        self.speed = random.randrange(1, 5)
        self.center_x = random.randrange(BLOCK_SIZE*3, SCREEN_WIDTH)
        self.center_y = random.randrange(0, SCREEN_HEIGHT-BLOCK_SIZE)

    