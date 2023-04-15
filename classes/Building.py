from gameconfig import *;

import arcade;

class Building(arcade.Sprite):
    def __init__(self, filename, cost=0, maintenance=0, capacity=0, dim=1):
        super().__init__("./images/" + filename, image_width=BLOCK_SIZE*dim, image_height=BLOCK_SIZE*dim)
        self.maintenance = maintenance
        self.capacity = capacity
        self.cost = cost
        self.dim = dim
        self.append()

    def place(self,x,y):
        # print(f"x:{x}, y:{y}. BX:{x*BLOCK_SIZE}, BY:{y*BLOCK_SIZE}")
        self.center_x = ((x+3)*BLOCK_SIZE + (self.dim)*BLOCK_SIZE/2)
        self.center_y = ((y+1)*BLOCK_SIZE - (self.dim)*BLOCK_SIZE/2)

    def append(self):
        building_sprites.append(self)
    
    def getCost(self):
        return self.cost
    
    def getMaintenance(self):
        return self.maintenance
    
    def getCapacity(self):
        return self.capacity

class PowerPlant(Building):
    def __init__(self, x=0, y=0):
        super().__init__("PowerPlant.png", cost=1000, maintenance=200, capacity=30, dim=2)
        self.place(x,y)

class FireDepartment(Building):
    def __init__(self, sradius, ftruck=1):
        self.sradius = sradius
        self.ftruck = ftruck
        super().__init__("FireDepartment.png", cost=1200, maintenance=300, capacity=20, dim=2)

    def getSafetyRadius(self):
        return self.sradius
    
# class FireTruck(FireDepartment):
#     def __init__(self):
#         super().__init__("FireTruck.png", 0.2)

class PoliceDepartment(Building):
    def __init__(self, sradius):
        self.sradius = sradius
        super().__init__("PoliceDepartment.png", cost=1200, maintenance=250, capacity=20, dim=2)

    def getSafetyRadius(self):
        return self.sradius
    
class Stadium(Building):
    def __init__(self, sradius, bonus=1.5):
        self.sradius = sradius
        self.bonus = bonus
        super().__init__("Stadium.png", cost=1500, maintenance=300, capacity=30, dim=2)

class House(Building):
    def __init__(self):
        super().__init__("House.png", capacity=20)

class WorkPlace(Building):
    def __init__(self):
        super().__init__("WorkPlace.png", capacity=30)