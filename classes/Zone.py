import arcade;
from gameconfig import *;
from classes.Building import House, WorkPlace;

class Zone(arcade.Sprite):
    hasBuilding = False

    def __init__(self, cost=0, dim=1, x=-1, y=-1, color=arcade.color.BLACK):
        super().__init__(image_width=BLOCK_SIZE*dim, image_height=BLOCK_SIZE*dim)
        self.texture = arcade.make_soft_square_texture(BLOCK_SIZE*dim, color, 255, 100)
        self.cost = cost
        self.dim = dim
        self.x = x
        self.y = y

    def place(self,x=None,y=None):
        if x is None: x = self.x
        if y is None: y = self.y
        self.center_x = ((x+3)*BLOCK_SIZE + (self.dim)*BLOCK_SIZE/2)
        self.center_y = ((y+1)*BLOCK_SIZE - (self.dim)*BLOCK_SIZE/2)
        a = arcade.check_for_collision_with_list(self, building_sprites)
        b = arcade.check_for_collision_with_list(self, zone_sprites)
        if len(a) > 0 or len(b) > 0:
            self.kill()
            return False
        self.append()
        return True

    def append(self):
        zone_sprites.append(self)
    
    def getCost(self):
        return self.cost
    
    def buildHouse(self):
        if self.hasBuilding:
            return None
        wp = WorkPlace(x=self.x, y=self.y)
        wp.place()
        self.hasBuilding = True
        return wp

class Residential (Zone):
    def __init__(self, x=-1, y=-1):
        super().__init__(cost=100, dim=1, x=x, y=y, color=arcade.color.WHITE)
    
    def buildHouse(self):
        if self.hasBuilding:
            return None
        house = House(x=self.x, y=self.y)
        house.place()
        self.hasBuilding = True
        return house

class Industrial (Zone):
    def __init__(self, x=-1, y=-1):
        super().__init__(cost=200, dim=1, x=x, y=y, color=arcade.color.ORANGE)

class Service (Zone):
    def __init__(self, x=-1, y=-1):
        super().__init__(cost=300, dim=1, x=x, y=y, color=arcade.color.CYAN)
    