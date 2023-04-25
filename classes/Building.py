from gameconfig import *;
import arcade;

class Building(arcade.Sprite):
    def __init__(self, filename, cost=0, maintenance=0, capacity=0, dim=1, x=-1, y=-1):
        super().__init__("./images/" + filename, image_width=BLOCK_SIZE*dim, image_height=BLOCK_SIZE*dim)
        self.maintenance = maintenance
        self.capacity = capacity
        self.cost = cost
        self.dim = dim
        self.x = x
        self.y = y
        if (x != -1 and y != -1):
            self.place(x,y)
            self.append()

    def place(self,x,y):
        self.center_x = ((x+3)*BLOCK_SIZE + (self.dim)*BLOCK_SIZE/2)
        self.center_y = ((y+1)*BLOCK_SIZE - (self.dim)*BLOCK_SIZE/2)

    def append(self):
        building_sprites.append(self)

    def getDim(self):
        return self.dim
    
    def getCost(self):
        return self.cost
    
    def getMaintenance(self):
        return self.maintenance
    
    def getCapacity(self):
        return self.capacity

class PowerPlant(Building):
    def __init__(self, x=-1, y=-1):
        super().__init__("PowerPlant.png", cost=1000, maintenance=200, capacity=30, dim=2, x=x, y=y)

class FireDepartment(Building):
    def __init__(self, x=-1, y=-1, sradius=1, ftruck=1):
        super().__init__("FireDepartment.png", cost=1200, maintenance=300, capacity=20, dim=2, x=x, y=y)
        self.sradius = sradius
        self.ftruck = ftruck

    def getSafetyRadius(self):
        return self.sradius
    
# class FireTruck(FireDepartment):
#     def __init__(self):
#         super().__init__("FireTruck.png", 0.2)

class PoliceDepartment(Building):
    def __init__(self, x=-1, y=-1, sradius=1):
        super().__init__("PoliceDepartment.png", cost=1200, maintenance=250, capacity=20, dim=2, x=x, y=y)
        self.sradius = sradius

    def getSafetyRadius(self):
        return self.sradius
    
class Stadium(Building):
    def __init__(self, x=-1, y=-1, sradius=1, bonus=1.5):
        super().__init__("Stadium.png", cost=1500, maintenance=300, capacity=30, dim=2, x=x, y=y)
        self.sradius = sradius
        self.bonus = bonus

class House(Building):
    def __init__(self, x=-1, y=-1):
        super().__init__("House.png", capacity=20)

class WorkPlace(Building):
    def __init__(self, x=-1, y=-1):
        super().__init__("WorkPlace.png", capacity=30, dim=1, x=x, y=y)

class Road(Building):
    images = ["Road.png", "RoadL.png", "CrossRoad.png"]

    def __init__(self, x=-1, y=-1, index=0):
        super().__init__("Road.png", dim=1, x=x, y=y, cost=0)
        self.index = index % len(self.images)
        self.texture = arcade.load_texture("./images/" + self.images[self.index])
        # check if there is a collision with another road
        a = arcade.check_for_collision_with_list(self, building_sprites)
        if len(a) > 0 and a[0].__class__.__name__ == "Road":
            a[0].index = (a[0].index + 1) % len(a[0].images)
            a[0].texture = arcade.load_texture("./images/" + a[0].images[a[0].index])
            self.kill()
            return

    def rotate(self):
        self.turn_left(90)
