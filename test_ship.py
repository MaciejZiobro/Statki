import unittest
from ship import Ship
from ppoints import Point

class ShipTest(unittest.TestCase):
    def test_is_destroyed(self):
        ship = Ship(2, 2, True, 2)
        self.assertFalse(ship.is_destroyed)
        
        ship.strike(Point(2, 2))
        ship.strike(Point(3, 2))
        self.assertTrue(ship.is_destroyed)

    def test_list_of_points(self):
        ship = Ship(0, 0, True, 3)
        self.assertEqual(ship.list_of_points(), [Point(0, 0), Point(1, 0), Point(2, 0)])
        ship = Ship(2, 2, False, 4)
        self.assertEqual(ship.list_of_points(), [Point(2, 2), Point(2, 3), Point(2, 4), Point(2, 5)])


    def test_strike(self):
        ship = Ship(2, 2, True, 2)
        ship.strike(Point(2, 2))
        self.assertTrue(ship.strike_list[0])
        self.assertFalse(ship.strike_list[1])
        ship.strike(Point(3, 2))
        self.assertTrue(ship.strike_list[1])
        
    def test_extend_list_of_points(self):
        ship = Ship(2, 2, True, 2)
        self.assertEqual(ship.extend_list_of_points(), {Point(2, 2), Point(3, 2), Point(2, 3), Point(3, 3), Point(1, 2), Point(2, 1), Point(1, 1), Point(3, 1), Point(1, 3), Point(4, 2), Point(4, 3), Point(4, 1)})

        ship = Ship(9, 9, True, 2)
        self.assertEqual(ship.extend_list_of_points(), {Point(8,8), Point(8,9), Point(9,8), Point(9,9)})


if __name__ == '__main__':
    unittest.main()