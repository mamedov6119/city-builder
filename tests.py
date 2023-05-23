import unittest, json, os, datetime
from classes.Zone import *
from gameconfig import *
from classes.Building import *
from logic.variables import v, Variables

class Disaster(unittest.TestCase):
    def setup(self):
        """ Setup a new game """
        v.reset()
        humans_sprites.clear()
        building_sprites.clear()
        zone_sprites.clear()
    
    def test_disaster(self):
        """ Test disaster """
        self.setup()
        # No errors expected
        v.summon_disaster() 
        m = humans_sprites[0]
        self.assertEqual(m.__class__.__name__, "Meteor")

    def test_disaster_methods(self):
        """ Test disaster methods """
        pos = 2
        self.setup()
        v.place_building(PowerPlant, pos, pos)
        v.summon_disaster()
        m = humans_sprites[0]
        self.assertEqual(m.__class__.__name__, "Meteor")
        m.assign_target(x=(pos+3)*BLOCK_SIZE, y=(pos+1)*BLOCK_SIZE)
        for _ in range(0, 2 * 50 * 10):
            m.update()
        self.assertEqual(len(humans_sprites), 0)
        self.assertEqual(len(building_sprites), 0)

    def test_endurance_work(self):
        """ Endurance of a work place """
        self.setup()
        v.place_zone(Residential, 0, 0)
        v.place_zone(Industrial, 0, 2)
        v.place_building(Road, 0, 1)
        v.road_logic(0,2)   
        v.summon_disaster()
        m = humans_sprites[5]
        self.assertEqual(m.__class__.__name__, "Meteor")
        m.assign_target(x=(0+3)*BLOCK_SIZE, y=(2+1)*BLOCK_SIZE)
        for _ in range(0, 2 * 50 * 10):
            m.update()
        self.assertEqual(len(building_sprites), 3)
    
    # def test_endurance_house(self):
    #     """ Endurance of a house """
    #     self.setup()
    #     v.place_zone(Residential, 0, 0)
    #     v.place_zone(Industrial, 0, 2)
    #     v.place_building(Road, 0, 1)
    #     v.road_logic(0,2)   
    #     v.summon_disaster()
    #     m = humans_sprites[5]
    #     self.assertEqual(m.__class__.__name__, "Meteor")
    #     m.assign_target(x=(0+3)*BLOCK_SIZE, y=(0+1)*BLOCK_SIZE)
    #     for _ in range(0, 2 * 50 * 1000):
    #         m.update()
    #     self.assertEqual(len(building_sprites), 3)
    #     self.assertEqual(sum([h.satisfaction for h in humans_sprites]), 500-5)


class Humans(unittest.TestCase):

    def test_human(self):
        """ Test human Initialization """
        h = Human(x=3,y=3, satisfaction=50)
        self.assertEqual(h.center_x, 3)
        self.assertEqual(h.center_y, 3)
        self.assertEqual(h.satisfaction, 50)

    def test_human_movement(self):
        """Movement of a human"""
        path=[[4,5],[5,6],[6,7]]
        h = Human(x=3,y=3, path=path, satisfaction=50)

        self.assertEqual(h.pos_list, [[p[0]*BLOCK_SIZE+BLOCK_SIZE*3.5, p[1]*BLOCK_SIZE+BLOCK_SIZE//2] for p in path])
        for _ in range(len(path)*2): h.update()

    def test_donotremove(self):
        """ Indestructible buildings/roads """
        v.place_zone(Residential, 0, 0)
        v.place_zone(Industrial, 0, 2)
        v.place_building(Road, 0, 1)
        v.road_logic(0,2)  
        attempt1 = v.remove_building(0,0)
        attempt2 = v.remove_building(0,1)
        self.assertEqual(attempt1, False)
        self.assertEqual(attempt2, False)
    
    def test_satisfaction(self):
        """ Satisfaction of a human """
        h = Human(x=3,y=3, satisfaction=50)
        h.inc()
        self.assertEqual(h.satisfaction, 51)
        h.dec()
        self.assertEqual(h.satisfaction, 50)
    
    def test_satisfaction_max_min(self):
        """ Satisfaction of a human, max and min values """
        h = Human(x=3,y=3, satisfaction=100)
        h.inc()
        self.assertEqual(h.satisfaction, 100)
        h.satisfaction = 0
        h.dec()
        self.assertEqual(h.satisfaction, 0)


class Buildings(unittest.TestCase):
    def setup(self):
        """ Setup a new game """
        v.reset()
        v.population = 0
        humans_sprites.clear()
        building_sprites.clear()
        zone_sprites.clear()

    def test_road(self):
        """ Placement of a road """
        self.setup()
        v.place_building(Road, 0, 0)
        road = building_sprites[0]
        self.assertEqual(road.index, 0)
        self.assertEqual(road.rotation, 0)
        self.assertEqual(road.getDim(), 1)
        self.assertEqual(road.getCost(), 100)
        self.assertEqual(road.getMaintenance(), 100)
    
    def test_road_types(self):
        """ Ability to change the road type """
        self.setup()
        v.place_building(Road, 0, 0)
        # Place another (same index) to change the type
        road = building_sprites[0]      # index = 0
        v.place_building(Road, 0, 0)    # index = 1
        v.place_building(Road, 0, 0)    # index = 2
        self.assertEqual(road.index, 2)

    def test_road_rotation(self):
        """ Ability to rotate the road """
        self.setup()
        v.place_building(Road, 0, 0)
        # Each rotation is 90 degrees at [0..360]
        road = building_sprites[0]      # rotation = 0
        v.rotate_road(road)             # rotation = 90
        v.rotate_road(road)             # rotation = 180
        self.assertEqual(road.rotation, 180)

    def test_zone_type(self):
        """ Ability to change the zone type """
        self.setup()
        v.place_zone(Residential, 0, 0)
        self.assertEqual(v.get_zone(0,0), "Residential")
        self.assertEqual(v.get_zone(1,0), None)

    def test_capacity(self):
        """ General capacity check """
        self.setup()
        self.assertEqual(PowerPlant(0,0).getCapacity(), 30)
        self.assertEqual(FireDepartment(2,2).getCapacity(), 20)
        self.assertEqual(PoliceDepartment(4,4).getCapacity(), 20)

    def test_safety_radius(self):
        """ General radius check """
        self.setup()
        self.assertEqual(FireDepartment(0,0).getSafetyRadius(), 1)
        self.assertEqual(PoliceDepartment(2,2).getSafetyRadius(), 1)

    def test_income(self):
        """ General income check """
        self.setup()
        print(Stadium(0,0).getIncome())
        self.assertEqual(Stadium(0,0).getIncome(), 500)
        v.place_building(Stadium, 0, 0)
        v.place_building(PowerPlant, 2, 2)
        v.check_powered()
        
        # one year later
        d = datetime.date(2001, 1, 1) - datetime.date(2000, 1, 1)
        v.time = d.days

        v.collect_income()
        self.assertEqual(v.money, -600)


    def test_house(self):
        """ Placement of a house """
        self.setup()
        v.place_zone(Residential, 0, 0)
        v.place_zone(Industrial, 0, 2)
        v.place_building(Road, 0, 1)
        v.road_logic(0,2)
        self.assertEqual(len(building_sprites), 3)
        
    def test_forest(self):
        """ Placement of a forest """
        self.setup()
        v.place_building(Forest, 0, 0)
        self.assertEqual(len(building_sprites), 1)

    def test_update_satisfaction(self):
        """ Satisfaction calculation for whole map """
        self.setup()
        v.update_satisfaction()
        self.assertEqual(v.satisfaction, 100)
        v.place_zone(Residential, 0, 0)
        v.place_zone(Industrial, 0, 2)
        v.place_building(Road, 0, 1)
        v.road_logic(0,2)
        v.update_satisfaction()
        self.assertEqual(v.satisfaction, 100)

    def test_update_population(self):
        """ Population calculation for whole map """
        self.setup()
        v.update_population()
        self.assertEqual(v.population, 0)
        v.place_zone(Residential, 0, 0)
        v.place_zone(Industrial, 0, 2)
        v.place_building(Road, 0, 1)
        v.road_logic(0,2)
        v.update_population()
        self.assertEqual(v.population, 10)

    # def test_other_buildings(self):
    #     """ Variables of other buildings """
    #     self.setup()
    #     h = House()
    #     self.assertEqual(h.x, -1)
    #     self.assertEqual(h.y, -1)
    #     self.assertEqual(h.getDim(), 1)
    #     w = WorkPlace()
    #     self.assertEqual(w.x, -1)
    #     self.assertEqual(w.y, -1)
    #     self.assertEqual(w.getDim(), 1)


class Logic(unittest.TestCase):
    def setup(self):
        """ Setup a new game """
        v.reset()
        humans_sprites.clear()
        building_sprites.clear()
        self.buildings = [PowerPlant, FireDepartment, PoliceDepartment, Stadium, Road]
        zone_sprites.clear()

    def test_building_empty(self):
        """ Created list is empty """
        self.setup()
        self.assertEqual(len(building_sprites), 0)

    def test_building_place_one(self):
        """ Inserted building is in the list """
        self.setup()
        pos = 2
        v.place_building(PowerPlant, pos, pos)
        self.assertEqual(len(building_sprites), 1)

    def test_building_place_multiple(self):
        """ Inserted buildings are in the list """
        self.setup()
        pos = 2
        v.place_building(PowerPlant, pos, pos)
        pos += 2
        v.place_building(FireDepartment, pos, pos)
        self.assertEqual(len(building_sprites), 2)
        
    def test_building_remove_one(self):
        """ Removed building is not in the list """
        self.setup()
        pos = 2
        v.place_building(PowerPlant, pos, pos)
        self.assertEqual(len(building_sprites), 1)
        v.remove_building(pos, pos)
        self.assertEqual(len(building_sprites), 0)
    
    def test_building_remove_multiple(self):
        """ Removed buildings are not in the list """
        self.setup()
        v.place_building(PowerPlant, 0, 0)
        v.place_building(FireDepartment, 2, 2)
        v.place_building(PoliceDepartment, 4, 4)
        v.remove_building(0, 0)
        v.remove_building(2, 2)
        v.remove_building(4, 4)
        self.assertEqual(len(building_sprites), 0)

    def test_building_fail(self):
        """ Building on top of another (not allowed to) """
        self.setup()
        v.place_building(PowerPlant, 2, 2)
        v.place_building(PowerPlant, 2, 2)
        self.assertEqual(len(building_sprites), 1)

    def test_zone_fail(self):
        """ Zone on top of another (not allowed to) """
        self.setup()
        v.place_zone(Residential, 2, 2)
        v.place_zone(Industrial, 2, 2)
        self.assertEqual(len(zone_sprites), 1)

    def test_money_charge(self):
        """ Charging money system """
        self.setup()
        m = v.money
        pos = 2
        v.place_building(PowerPlant, pos, pos)
        self.assertEqual(v.money, m - PowerPlant().getCost())  

    def test_money_charge_mult(self):
        """ Charging money system multiple"""
        self.setup()
        m = v.money
        pos = 2
        v.place_building(Stadium, pos, pos)
        pos += 2
        v.place_building(PoliceDepartment, pos, pos)
        self.assertEqual(v.money, m - Stadium().getCost() - PoliceDepartment().getCost())

    def test_money_refund(self):
        """ Refund money system """
        self.setup()
        m = v.money
        v.place_building(PowerPlant, 0, 0)
        v.remove_building(0, 0)
        self.assertEqual(v.money, m)
    
    def test_money_refund_mult(self):
        """ Refund money system multiple """
        self.setup()
        pos = 0
        for b in self.buildings:
            m = v.money
            v.place_building(b, pos, pos)
            v.remove_building(pos, pos)
            self.assertEqual(v.money, m)
            pos += 2

    def test_speed_method(self):
        """ Speed check using method """
        self.setup()
        v.change_speed(2)
        self.assertEqual(v.speed, 2)

    def test_maintenance_charge(self):
        """ Maintenance charge """
        self.setup()
        m = v.money
        d0 = datetime.date(2000, 1, 1)
        d1 = datetime.date(2001, 1, 1)
        delta = d1 - d0
        v.time = 0
        pos = 2
        v.place_building(PowerPlant, pos, pos)
        v.time = delta.days
        v.maintenance_charge()
        self.assertEqual(v.money, m - PowerPlant().getMaintenance() - PowerPlant().getCost())

    def test_maintenance_charge_multiple(self):
        """ Maintenance charge for multiple buildings """
        self.setup()
        d0 = datetime.date(2000, 1, 1)
        d1 = datetime.date(2001, 1, 1)
        delta = d1 - d0
        v.time = 0
        pos = 2
        v.place_building(PowerPlant, pos, pos)
        pos += 2
        v.place_building(Road, 1, 1)
        v.place_building(FireDepartment, pos, pos)
        print(v.time)
        m = v.money
        v.maintenance_charge()
        self.assertEqual(v.money, m - PowerPlant().getMaintenance() - Road().getMaintenance() - FireDepartment().getMaintenance())
        


class Saves(unittest.TestCase):
    def setup(self):
        """ Setup a new game """
        v.reset()
        humans_sprites.clear()
        building_sprites.clear()
        zone_sprites.clear()

    def test_save(self):
        """ Save game """
        building = PowerPlant
        self.setup()
        v.place_building(building, 2, 4)
        v.save('test.json')
        data = None
        with open('test.json', 'r') as f:
            data = json.load(f)
        self.assertEqual(len(data["items"]), 1)
        self.assertEqual(data["items"][0]["type"], building.__name__)
        os.remove('test.json')

    def test_load(self):
        """ Load game """
        building = PowerPlant; pos = 2
        self.setup()
        v.place_building(building, pos, pos)
        v.save('test.json')
        v.load('test.json')
        self.assertEqual(len(v.items), 1)
        self.assertEqual(v.items[0]['type'], building.__name__)
        os.remove('test.json')
    
    def test_load_unexistent(self):
        """ Load unexistent file """
        self.setup()
        v.load('unexistent.json')
        self.assertEqual(v.time, 0)
        self.assertEqual(v.speed, 1)
        self.assertEqual(v.money, 1000)
        self.assertEqual(len(v.items), 0)
        

    def test_save_speed_method(self):
        """ Speed check using method """
        speed = 3
        self.setup()
        v.change_speed(speed)
        v.save('test.json')
        data = None
        with open('test.json', 'r') as f:
            data = json.load(f)
        self.assertEqual(data["speed"], speed)
        os.remove('test.json')

    def test_save_zone_industr(self):
        """ Save zone """
        self.setup()
        zone = Industrial
        v.place_zone(zone, 2, 4)
        v.save('test.json')
        data = None
        with open('test.json', 'r') as f:
            data = json.load(f)
        self.assertEqual(len(data["zones"]), 1)
        self.assertEqual(data["zones"][0]["type"], zone.__name__)
        os.remove('test.json')
    
    def test_save_zone_resident(self):
        """ Save zone """
        self.setup()
        zone = Residential
        v.place_zone(zone, 0, 0)
        v.place_zone(Service, 0, 2)
        v.place_building(Road, 0, 1)
        v.road_logic(0,1)
        v.save('test.json')
        data = None
        with open('test.json', 'r') as f:
            data = json.load(f)
        self.assertEqual(len(data["zones"][0]["humans"]), 25)
        os.remove('test.json')


if __name__ == '__main__':
    unittest.main()