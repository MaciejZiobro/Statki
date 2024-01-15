import unittest
from ppoints import Point
from ship import Ship
from bot import ship_space

class Test_Bot(unittest.TestCase):
    def test_ship_space(self):
        point = Point(4, 2)
        points_used = [Point(2, 2), Point(3, 3), Point(4, 3)]
        ships_placement = [Ship(0, 0, False, 4), Ship(0,0, True, 4)]

        self.assertEqual([True, False], ship_space(point, points_used, ships_placement))
        
        point = Point(0, 0)
        points_used = [Point(1, 1), Point(0, 1), Point(1, 0)]
        ships_placement = [Ship(0, 0, False, 4), Ship(0,0, True, 2)]
        self.assertEqual([False, False], ship_space(point, points_used, ships_placement))
        

if __name__ == '__main__':
    unittest.main()