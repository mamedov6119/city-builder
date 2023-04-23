import unittest
from gameconfig import *
from gui.window import Window
from classes.Building import *;

class Logic(unittest.TestCase):
    def setup(self):
        """ Setup a new game """
        building_sprites.clear()
        humans_sprites.clear()
        self.game = Window()
        self.game.setup()
        self.buildings = [PowerPlant, FireDepartment, PoliceDepartment, Stadium, Road]

    def test_window(self):
        """" Window dimensions are correct """
        self.setup()
        self.assertEqual(self.game.width, SCREEN_WIDTH) 
        self.assertEqual(self.game.height, SCREEN_HEIGHT) 

    def test_building_empty(self):
        """" Created list is empty """
        self.setup()
        self.assertEqual(len(building_sprites), 0)

    def test_building_place_one(self):
        """" Inserted building is in the list """
        self.setup()
        PowerPlant(0, 0)
        self.assertEqual(len(building_sprites), 1)

    def test_building_place_all(self):
        """" Inserted buildings are in the list """
        self.setup()
        pos = {'x': 0, 'y': 1}
        for building in self.buildings:
            b = building(pos['x'], pos['y'])
            pos['x'] += b.getDim()
            if (3*BLOCK_SIZE) + pos['x']*BLOCK_SIZE > SCREEN_WIDTH:
                pos['x'] = 0; pos['y'] += b.getDim()
        self.assertEqual(len(building_sprites), len(self.buildings))
        
    def test_building_remove_one(self):
        """" Removed building is not in the list """
        self.setup()
        b = PowerPlant(0, 0)
        self.assertEqual(len(building_sprites), 1)
        b.kill()
        self.assertEqual(len(building_sprites), 0)
    
    def test_building_remove_multiple(self):
        """" Removed buildings are not in the list """
        self.setup()
        list = [PowerPlant(0, 0), FireDepartment(2, 2), PoliceDepartment(4, 4)]
        for b in list: b.kill()
        self.assertEqual(len(building_sprites), 0)
    
if __name__ == '__main__':
    unittest.main()