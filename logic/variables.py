import json, arcade
from gameconfig import *
from classes.Disaster import *

class Variables:
    time = 0
    speed = 1
    items = []
    zones = []
    money = 1000
    population = 100
    satisfaction = 100

    def reset(self):
        self.time = 0
        self.speed = 1
        self.items = []
        self.zones = []
        self.money = 1000

    def load(self, filename):
        """ Load the game from a file """
        try:
            with open(filename, "r") as f:
                data = json.load(f)
                self.time = data["time"] if "time" in data else self.time
                self.speed = data["speed"] if "speed" in data else self.speed
                self.money = data["money"] if "money" in data else self.money
                self.items = data["items"] if "items" in data else self.items
                self.zones = data["zones"] if "zones" in data else self.zones
        except: self.reset()

    def save(self, filename):
        """ Save the game to a file """
        print("Saving...", end=" ")
        with open(filename, "w") as f:
            json.dump({"time": v.time, "speed": v.speed, "money": v.money, "items": v.items, "zones" : v.zones }, f)
        print("Save complete!")

    def place_building(self, building, x, y):
        """ Place a building on the map """
        b = building(x=x, y=y)
        if not b.place():
            return False
        self.money -= b.getCost()
        obj = {"x": x, "y": y, "type": building.__name__}
        if building.__name__ == "Road":
            obj["index"] = b.index; obj["rotation"] = b.rotation
            self.check_road(x, y, self.into_matrix())
        self.items.append(obj)


    def into_matrix(self):
        cells_x = int(SCREEN_HEIGHT / BLOCK_SIZE)
        cells_y = int(SCREEN_WIDTH / BLOCK_SIZE)
        matrix = [["-" for x in range(cells_x)] for y in range(cells_y)]
        for zone in self.zones:
            matrix[zone["x"]][zone["y"]] = zone["type"][0]
        for road in self.items:
            if road["type"] == "Road":
                matrix[road["x"]][road["y"]] = "O"
        for row in matrix:
            for item in row:
                print(item, end=" ")
            print()
        return matrix
    
    def check_road(self, x, y, mat, direction=(0,0), visited=[]):
        # # road check until it reaches a zone
        # # check if there is a road in the 3 directions (dont check the one it came from)
        # directions = [(0,1), (1,0), (0,-1), (-1,0)]
        # if direction != (0,0):
        #     # remove the opposite direction
        #     directions.remove((-direction[0], -direction[1]))
        # for d in directions:
        #     # if not visited and its road - continue searching
        #     if (x+d[0], y+d[1]) not in visited and mat[x+d[0]][y+d[1]] == "O":
        #         visited.append((x+d[0], y+d[1]))
        #         self.check_road(x+d[0], y+d[1], mat, d, visited)
        #     # if its a zone - print a message the road is connected
        #     elif mat[x+d[0]][y+d[1]] != "-" and mat[x+d[0]][y+d[1]] != "O":
        #         print("Road is connected")
        #         return True
        # # if no road is found - print a message the road is not connected
        # print("Road is not connected")
        return False

    def change_road(self, b):
        b.change_type()
        for item in self.items:
            if item["x"] == b.x and item["y"] == b.y and item["type"] == "Road":
                item["index"] = b.index
                break

    def remove_building(self, x, y):   
        """ Remove a building from the map """
        try:
            b = arcade.get_sprites_at_point([(x+4)*BLOCK_SIZE, (y+1)*BLOCK_SIZE], building_sprites)[0]
            self.money += b.getCost()
            obj = {"x": b.x, "y": b.y, "type": b.__class__.__name__}
            if b.__class__.__name__ == "Road":
                obj["index"] = b.index
                obj["rotation"] = b.rotation
            self.items.remove(obj)
            b.kill()
        except: return False

    def change_speed(self, speed):
        """ Change the speed of the game """
        self.speed = speed

    def summon_disaster(self):
        """ Summon a disaster """
        Meteor()
        if self.satisfaction > 0:
            self.satisfaction -= (self.population * 0.01) * 0.01

    def maintenance_charge(self):
        """ Charge the maintenance of the buildings """
        if self.time % 365 == 0: 
            for i in range(len(self.items)):
                self.money -= building_sprites[i].getMaintenance()

    def place_zone(self, zone, x, y):
        """ Place a zone on the map """
        z = zone(x=x, y=y)
        if not z.place():
            return False
        self.money -= z.getCost()
        self.zones.append({"x": x, "y": y, "type": zone.__name__})

# --------------------------------------------------
v = Variables()
