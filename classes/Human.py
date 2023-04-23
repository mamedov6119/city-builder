from gameconfig import *;

# import gui.window as w;
import arcade, math, random;
from logic.variables import v;
from arcade import check_for_collision_with_list;

class Human(arcade.Sprite):
    def __init__(self):
        super().__init__("./images/Human.png", CHRACTER_SCALING)
        self.circle_center_x = random.randrange(150, 700)
        self.circle_center_y = random.randrange(150, 700)
        self.circle_radius = random.randrange(10, 200)
        self.circle_angle = random.random() * 2 * math.pi
        humans_sprites.append(self)

    def update(self):
        # if (not self.collides_with_list(building_sprites)):
        self.center_x = self.circle_radius * math.sin(self.circle_angle) \
            + self.circle_center_x
        self.center_y = self.circle_radius * math.cos(self.circle_angle) \
            + self.circle_center_y
        self.circle_angle += HUMAN_SPEED * v.speed
        self.check_boundary_collision()

    def collides_with_list(self, sprite_list):
        return check_for_collision_with_list(self, sprite_list)
    
    def check_boundary_collision(self):
        if self.right > SCREEN_WIDTH: self.right = SCREEN_WIDTH
        if self.left < 3*BLOCK_SIZE: self.left = 3*BLOCK_SIZE
        if self.top > SCREEN_HEIGHT - BLOCK_SIZE: self.top = SCREEN_HEIGHT - BLOCK_SIZE
        if self.bottom < 0: self.bottom = 0