from gameconfig import *;
import arcade, random, math, time;

class Meteor(arcade.Sprite):
    def __init__(self, dim=2):
        super().__init__("./images/Meteor.png", image_width=BLOCK_SIZE*dim, image_height=BLOCK_SIZE*dim)
        self.dim = dim
        self.destroy = 0
        self.center_x = BLOCK_SIZE*2
        self.center_y = BLOCK_SIZE*2
        humans_sprites.append(self)
        self.assign_target()

    def assign_target(self, x=None, y=None):
        self.target_x = random.randint(BLOCK_SIZE*3, SCREEN_WIDTH) if x is None else x
        self.target_y = random.randint(0, SCREEN_HEIGHT - BLOCK_SIZE) if y is None else y
        self.angle = math.degrees(math.atan2(self.target_y - self.center_y, self.target_x - self.center_x))

    def explode(self):
        duration = 20 * 5
        self.destroy += 1
        if self.destroy == 1:
            self.texture = arcade.make_circle_texture(self.width, arcade.color.RED, 255)
        elif self.destroy == duration:
            buildings = arcade.check_for_collision_with_list(self, building_sprites)
            for b in buildings:
                b.kill()
            self.kill()

    def update(self):
        if self.center_x < self.target_x and self.center_y < self.target_y:
            self.center_x += math.cos(math.radians(self.angle)) * 2
            self.center_y += math.sin(math.radians(self.angle)) * 2
        else:
            self.explode()
            
    