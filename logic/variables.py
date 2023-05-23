import json, arcade, datetime
from classes.Disaster import *
from gameconfig import *

class Variables:
    time = 0
    speed = 1
    items = []
    zones = []
    money = 1000
    population = 0
    satisfaction = 100
    donotremove = []
    last_income = -1
    last_maintenance = -1

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
                self.time = data["time"]   if "time" in data else self.time
                self.speed = data["speed"] if "speed" in data else self.speed
                self.money = data["money"] if "money" in data else self.money
                self.items = data["items"] if "items" in data else self.items
                self.zones = data["zones"] if "zones" in data else self.zones
        except: self.reset()

    def save(self, filename):
        """ Save the game to a file """
        with open(filename, "w") as f:
            json.dump({"time": v.time, "speed": v.speed, "money": v.money, "items": v.items, "zones" : v.zones }, f)

    def place_building(self, building, x, y):
        """ Place a building on the map """
        b = building(x=x, y=y)
        if not b.place():
            return False
        self.money -= b.getCost()
        obj = {"x": x, "y": y, "type": building.__name__}
        if building.__name__ == "Road":
            obj["index"] = b.index; obj["rotation"] = b.rotation
            self.road_logic(x,y)
        self.items.append(obj)
        self.check_powered()
        print("Power" + str(b.powered))

    def road_logic(self, x, y):
        """ Logic for roads, as checking for nearby zones """
        zonelist, roadlist = self.nearest_zone_by_roads(x, y, self.into_matrix(), [], [])
        titles = [ t[2] for t in zonelist ]
        if 'R' in titles and ('S' in titles or 'I' in titles):
            for pos in roadlist:
                self.donotremove.append(pos)
            for pos in zonelist:
                finder = arcade.Sprite()
                finder.center_x = ((pos[0]+3)*BLOCK_SIZE + (1)*BLOCK_SIZE/2)
                finder.center_y = ((pos[1]+1)*BLOCK_SIZE - (1)*BLOCK_SIZE/2)
                finder.texture = arcade.make_soft_square_texture(BLOCK_SIZE, arcade.color.RED, outer_alpha=255)
                target = arcade.check_for_collision_with_list(finder, zone_sprites)
                target[0].buildHouse(path=roadlist)

    def into_matrix(self):
        """ Convert the map into a matrix """
        matrix = [['-' for i in range((SCREEN_WIDTH-(3*BLOCK_SIZE))//BLOCK_SIZE)] for j in range((SCREEN_HEIGHT-(1*BLOCK_SIZE))//BLOCK_SIZE)]
        for item in self.items:
            if item["type"] == "Road":
                matrix[item["y"]][item["x"]] = 'O'
        for zone in self.zones:
            matrix[zone["y"]][zone["x"]] = zone["type"][0]
        return matrix
    
    def nearest_zone_by_roads(self, x, y, matrix, found=[], path=[]):
        """ Find the nearest zone through roads """
        queue = [(x, y)]
        prev_x, prev_y = x, y
        visited = [[False for i in range((SCREEN_WIDTH-(3*BLOCK_SIZE))//BLOCK_SIZE)] for j in range((SCREEN_HEIGHT-(1*BLOCK_SIZE))//BLOCK_SIZE)]
        visited[y][x] = True
        while queue:
            x, y = queue.pop(0)
            if matrix[y][x] in ['R', 'S', 'I']:
                print("Zone found: " + matrix[y][x] + " x: " + str(x) + " y: " + str(y))
                if (x, y, matrix[y][x]) not in found:
                    found.append((x, y, matrix[y][x]))
                matrix[y][x] = '-'
                return self.nearest_zone_by_roads(prev_x, prev_y, matrix, found, path)
            for i in range(4):
                if i == 0:   nx, ny = x+1, y
                elif i == 1: nx, ny = x-1, y
                elif i == 2: nx, ny = x, y+1
                elif i == 3: nx, ny = x, y-1
                if nx < 0 or nx >= len(matrix[0]) or ny < 0 or ny >= len(matrix) or visited[ny][nx] or matrix[ny][nx] == '-':
                    continue
                queue.append((nx, ny))
                visited[ny][nx] = True
                prev_x, prev_y = x, y
                if (x, y) not in path: path.append((x, y))
        return (found, path)
    
    def get_zone(self, x, y):
        """ Get a zone from the map """
        for zone in self.zones:
            if zone["x"] == x and zone["y"] == y:
                return zone["type"]
        return None

    def change_road(self, b):
        """ Change a road type """
        b.change_type()
        for item in self.items:
            if item["x"] == b.x and item["y"] == b.y and item["type"] == "Road":
                item["index"] = b.index
                break
        
    def rotate_road(self, b):
        """ Rotate a road """
        b.rotate()
        for item in self.items:
            if item["x"] == b.x and item["y"] == b.y and item["type"] == "Road":
                item["rotation"] = b.rotation
                break

    def remove_building(self, x, y):   
        """ Remove a building from the map """
        try:
            if (x, y) in self.donotremove:
                return False
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

    def maintenance_charge(self):
        """ Charge the maintenance of the buildings """
        date = datetime.date(2000, 1, 1) + datetime.timedelta(days=self.time)
        if date.day == 1 and date.month == 1 and self.last_maintenance != int(self.time): 
            for i in range(len(self.items)):
                self.money -= building_sprites[i].getMaintenance()
                print("Maintenance charge:", building_sprites[i].getMaintenance())
            self.last_maintenance = int(self.time)

    def populate_buildings(self):
        """ Populate the buildings """
        # if a week has passed and the satisfaction is greater than 10, add a person to a random house
        if self.time % 7 == 0:
            if self.satisfaction > 10:
                for item in building_sprites:
                    if item.p_inside < item.capacity:
                        item.p_inside += 1
                        self.population += 1
                        break

    def place_zone(self, zone, x, y):
        """ Place a zone on the map """
        z = zone(x=x, y=y)
        if not z.place():
            return False
        self.money -= z.getCost()
        self.zones.append({"x": x, "y": y, "type": zone.__name__})

    def update_satisfaction(self):
        """ Update the satisfaction of the zones """
        temp = []
        for item in building_sprites:
            if item.__class__.__name__ == "House":
                for human in item.humans:
                    temp.append(human.satisfaction)
        self.population = len(temp)
        if len(temp) < 5:
            self.satisfaction = 100
        else: self.satisfaction = sum(temp) / len(temp)

    def update_population(self):
        """ Update the population of the zones """
        sum = 0
        for item in building_sprites:
            if item.__class__.__name__ == "House":
                sum += len(item.humans)
        self.population = sum

    def is_within_reach(self, building, radius=6):
        """ Check if the building has electricity """
        for item in self.items:
            if item["type"] == "PowerPlant":
                # Calculating Euclidean distance
                distance = abs(item["x"] - building.x) + abs(item["y"] - building.y)
                if distance <= radius:
                    print("Within reach")
                    return True
        print("Not within reach")
        return False

    def collect_income(self):
        """ Collect income from all buildings. """
        date = datetime.date(2000, 1, 1) + datetime.timedelta(days=self.time)
        if int(date.day) == 1 and self.last_income != int(self.time):
            for building in building_sprites:
                if building.powered:
                    self.money += building.getIncome()
                    print("Income:",building.getIncome())
            self.last_income = int(self.time)
    
    def check_powered(self):
        """ Check if the buildings are powered """
        for building in building_sprites:
            if self.is_within_reach(building):
                building.setPower(True)

            
# --------------------------------------------------
v = Variables()
