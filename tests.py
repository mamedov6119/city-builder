import unittest
from gameconfig import *
from logic.variables import v
from classes.Building import *

class Logic(unittest.TestCase):
    def setup(self):
        """ Setup a new game """
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
        list = [PowerPlant(0, 0), FireDepartment(2, 2), PoliceDepartment(4, 4)]
        for b in list: v.remove_building(b.x, b.y)
        self.assertEqual(len(building_sprites), 0)
    
if __name__ == '__main__':
    unittest.main()