import json, arcade
from gameconfig import *

class Variables:
    time = 0
    speed = 1
    items = []
    money = 1000

    def reset(self):
        self.time = 0
        self.speed = 1
        self.items = []
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
        except: self.reset()

    def save(self, filename):
        """ Save the game to a file """
        print("Saving...", end=" ")
        with open(filename, "w") as f:
            json.dump({"time": v.time, "speed": v.speed, "money": v.money, "items": v.items}, f)
        print("Save complete!")

    def place_building(self, building, x, y):
        """ Place a building on the map """
        roadFound = False
        b = building(x=x, y=y)
        self.money -= b.getCost()
        obj = {"x": x, "y": y, "type": building.__name__}
        if building.__name__ == "Road":
            obj["index"] = b.index
            obj["rotation"] = b.rotation
            for item in self.items:
                if item["x"] == x and item["y"] == y and item["type"] == "Road":
                    roadFound = True
                    item["index"] += 1 
                    item["index"] %= 4
                    break
        if not roadFound:
            self.items.append(obj)
        
    def rotate_road(self, b):
        b.rotate()
        for item in self.items:
            if item["x"] == b.x and item["y"] == b.y and item["type"] == "Road":
                item["rotation"] = b.rotation
                break

    def remove_building(self, x, y):   
        """ Remove a building from the map """
        b = arcade.get_sprites_at_point([(x+4)*BLOCK_SIZE, (y+1)*BLOCK_SIZE], building_sprites)[0]
        self.money += b.getCost()
        obj = {"x": b.x, "y": b.y, "type": b.__class__.__name__}
        if b.__class__.__name__ == "Road":
            obj["index"] = b.index
            obj["rotation"] = b.rotation
        self.items.remove(obj)
        b.kill()

    def change_speed(self, speed):
        """ Change the speed of the game """
        self.speed = speed

# --------------------------------------------------
v = Variables()
