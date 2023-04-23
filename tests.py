import unittest, json, os
from gameconfig import *
from logic.variables import v
from classes.Building import *

class Logic(unittest.TestCase):
    def setup(self):
        """ Setup a new game """
        v.money = 1000
        v.items = []
        building_sprites.clear()
        humans_sprites.clear()
        self.buildings = [PowerPlant, FireDepartment, PoliceDepartment, Stadium, Road]

    def test_building_empty(self):
        """" Created list is empty """
        self.setup()
        self.assertEqual(len(building_sprites), 0)

    def test_building_place_one(self):
        """" Inserted building is in the list """
        self.setup()
        v.place_building(PowerPlant, 0, 0)
        self.assertEqual(len(building_sprites), 1)

    def test_building_place_all(self):
        """" Inserted buildings are in the list """
        self.setup()
        pos = 0
        for b in self.buildings:
            v.place_building(b, pos, pos)
            pos += 2
        self.assertEqual(len(building_sprites), len(self.buildings))
        
    def test_building_remove_one(self):
        """" Removed building is not in the list """
        self.setup()
        v.place_building(PowerPlant, 0, 0)
        self.assertEqual(len(building_sprites), 1)
        v.remove_building(0, 0)
        self.assertEqual(len(building_sprites), 0)
    
    def test_building_remove_multiple(self):
        """" Removed buildings are not in the list """
        self.setup()
        v.place_building(PowerPlant, 0, 0)
        v.place_building(FireDepartment, 2, 2)
        v.place_building(PoliceDepartment, 4, 4)
        v.remove_building(0, 0)
        v.remove_building(2, 2)
        v.remove_building(4, 4)
        self.assertEqual(len(building_sprites), 0)

    def test_money_charge(self):
        """ Charging money system """
        self.setup()
        m = v.money
        v.place_building(PowerPlant, 0, 0)
        self.assertEqual(v.money, m - PowerPlant().getCost())  

    def test_money_charge_all(self):
        """ Charging money system ALL"""
        self.setup()
        pos = 0
        for b in self.buildings:
            m = v.money
            v.place_building(b, pos, pos)
            self.assertEqual(v.money, m - b().getCost())
            pos += 2
        
    def test_money_refund(self):
        """ Refund money system """
        self.setup()
        m = v.money
        v.place_building(PowerPlant, 0, 0)
        v.remove_building(0, 0)
        self.assertEqual(v.money, m)
    
    def test_money_refund_all(self):
        """ Refund money system ALL """
        self.setup()
        pos = 0
        for b in self.buildings:
            m = v.money
            v.place_building(b, pos, pos)
            v.remove_building(pos, pos)
            self.assertEqual(v.money, m)
            pos += 2

    def test_save(self):
        """ Save game """
        self.setup()
        v.place_building(PowerPlant, 0, 0)
        v.save('test.json')
        data = None
        with open('test.json', 'r') as f:
            data = json.load(f)
        self.assertEqual(len(data["items"]), 1)
        os.remove('test.json')

    def test_load(self):
        """ Load game """
        self.setup()
        v.place_building(PowerPlant, 0, 0)
        v.save('test.json')
        v.load('test.json')
        self.assertEqual(len(v.items), 1)
        os.remove('test.json')

    def test_speed_method(self):
        """ Speed check using method """
        self.setup()
        v.change_speed(2)
        self.assertEqual(v.speed, 2)

    def test_save_speed_method(self):
        """ Speed check using method """
        self.setup()
        v.change_speed(2)
        v.save('test.json')
        data = None
        with open('test.json', 'r') as f:
            data = json.load(f)
        self.assertEqual(data["speed"], 2)
        os.remove('test.json')

if __name__ == '__main__':
    unittest.main()