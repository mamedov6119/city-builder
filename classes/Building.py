from gameconfig import *;

import arcade;

class Building(arcade.Sprite):
    def __init__(self, filename, building_scaling, cost, maintenance, capacity, dim):
        super().__init__("./images/" + filename, building_scaling)
        self.cost = cost
        self.maintenance = maintenance
        self.capacity = capacity
        self.dim = dim

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
        super().__init__("PowerPlant.png", 0.5, 1000, 200, 30, 2)
        self.place(x,y)
        self.append()


class FireDepartment(Building):
    def __init__(self, sradius, ftruck=1):
        self.sradius = sradius
        self.ftruck = ftruck
        super().__init__("FireDepartment.png", 0.5, 1200, 300, 20)

    def getSafetyRadius(self):
        return self.sradius
    
class FireTruck(FireDepartment):
    def __init__(self):
        super().__init__("FireTruck.png", 0.2)

class PoliceDepartment(Building):
    def __init__(self, sradius):
        self.sradius = sradius
        super().__init__("PoliceDepartment.png", 0.5, 1200, 250, 20)

    def getSafetyRadius(self):
        return self.sradius
    
class Stadium(Building):
    def __init__(self, sradius, bonus=1.5):
        self.sradius = sradius
        self.bonus = bonus
        super().__init__("Stadium.png", 0.5, 1500, 300, 30)

class House(Building):
    def __init__(self):
        super().__init__("House.png", 0.5, capacity=20)

class WorkPlace(Building):
    def __init__(self):
        super().__init__("WorkPlace.png", 0.5, capacity=30)