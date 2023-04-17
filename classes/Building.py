from gameconfig import *;

import arcade;
import math;
class Building(arcade.Sprite):
    def __init__(self, filename, cost=0, maintenance=0, capacity=0, dim=1, x=-1, y=-1):
        super().__init__("./images/" + filename, image_width=BLOCK_SIZE*dim, image_height=BLOCK_SIZE*dim)
        self.maintenance = maintenance
        self.capacity = capacity
        self.cost = cost
        self.dim = dim
        if (x != -1 and y != -1):
            self.place(x,y)
            self.append()

    def place(self,x,y):
        # print(f"x:{x}, y:{y}. BX:{x*BLOCK_SIZE}, BY:{y*BLOCK_SIZE}")
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
        self.putFireDown()

    def getSafetyRadius(self):
        return self.sradius
    
    def getFireTrucks(self):
        return self.ftruck
    
    def setFireTrucks(self, ftruck):
        self.ftruck = ftruck

    def putFireDown(self):
        self.truck = self.FireTruck(self.center_x+30, self.center_y+30, 100, 100)
        fireTruck_sprites.append(self.truck)
        self.truck.update()
    
    class FireTruck(arcade.Sprite):
        def __init__(self, x, y, where_to_x, where_to_y):
            super().__init__("./images/FireTruck.png", 1)
            self.center_x = x
            self.center_y = y
            self.speed = FIRETRUCK_SPEED
            self.where_to_x = where_to_x
            self.where_to_y = where_to_y

        def update(self):
            start_x = self.center_x
            start_y = self.center_y

            dest_x = self.where_to_x
            dest_y = self.where_to_y

            x_diff = dest_x - start_x
            y_diff = dest_y - start_y

            angle = math.atan2(y_diff, x_diff)

            distance = math.sqrt((self.center_x - dest_x) ** 2 + (self.center_y - dest_y) ** 2)

            speed = min(self.speed, distance)

            change_x = math.cos(angle) * speed
            change_y = math.sin(angle) * speed

            self.center_x += change_x
            self.center_y += change_y

            distance = math.sqrt((self.center_x - dest_x) ** 2 + (self.center_y - dest_y) ** 2)

            if distance <= self.speed:
                print("Fire put down!")


class Fire(Building):
    def __init__(self, x=-1, y=-1):
        super().__init__("Fire.png", x=x, y=y)


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

class Road(Building):
    def __init__(self, x=-1, y=-1):
        super().__init__("Road.png", dim=1, x=x, y=y)


class House(Building):
    def __init__(self):
        super().__init__("House.png", capacity=20)

class WorkPlace(Building):
    def __init__(self, x=-1, y=-1):
        super().__init__("WorkPlace.png", capacity=30, dim=1, x=x, y=y)