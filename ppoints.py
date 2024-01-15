from math import sqrt

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "("+str(self.x)+","+str(self.y)+")"

    def __repr__(self):
        return "Point"+str(self)

    def __eq__(self, other):
        if self.x == other.x and self.y == other.y:
            return True
        return False

    def __ne__(self, other):       
        return not self == other

    def __add__(self, other):
        return Point(self.x+other.x, self.y+other.y)

    def __sub__(self, other):
        return Point(self.x-other.x, self.y-other.y)

    def __mul__(self, other):
        return self.x*other.x+self.y*other.y

    def cross(self, other):      
        return self.x * other.y - self.y * other.x

    def length(self):
        return sqrt(self.x**2+self.y**2)

    def __hash__(self):
        return hash((self.x, self.y))
    

import unittest

class TestPoint(unittest.TestCase):
    def setUp(self):
        self.zero = Point(0,0)
        self.p1 = Point(5,3)
        self.pp1 = Point(-5,-3)
        self.po1 = Point(3,-5)
        self.pm2 = Point(10,6)
        self.p2 = Point(3,1)
        
    def test_str(self):
        self.assertEqual(str(self.zero),"(0,0)")
        self.assertEqual(str(self.p1),"(5,3)")
        self.assertEqual(str(self.p2),"(3,1)")
        
    def test_repr(self):
        self.assertEqual(repr(self.zero),"Point(0,0)")
        self.assertEqual(repr(self.p1),"Point(5,3)")
        self.assertEqual(repr(self.p2),"Point(3,1)")
        
    def test_eq(self):
        self.assertEqual(self.zero == self.zero, True)
        self.assertEqual(self.p1 == self.p1, True)
        self.assertEqual(self.p1 == self.zero, False)
        self.assertEqual(self.pm2 == self.pp1, False)
        
    def test_ne(self):
        self.assertEqual(self.zero != self.zero, False)
        self.assertEqual(self.p1 != self.p1, False)
        self.assertEqual(self.p1 != self.zero, True)
        self.assertEqual(self.pm2 != self.pp1, True)
        self.assertEqual(self.p1 != self.p1, not self.p1 == self.p1)
        
    def test_add(self):
        self.assertEqual(self.zero+self.p1, self.p1)
        self.assertEqual(self.zero+self.zero, self.zero)
        self.assertEqual(self.p1+self.pp1, self.zero)
        self.assertEqual(self.p1+self.p2, self.p2+self.p1)
        self.assertEqual(self.p1+self.p2, Point(8,4))
        self.assertEqual(self.pp1+self.po1, Point(-2,-8))
        
    def test_sub(self):
        self.assertEqual(self.zero-self.p1, Point(-5,-3))
        self.assertEqual(self.zero-self.zero, self.zero)
        self.assertEqual(self.p1-self.p1, self.zero)
        self.assertEqual(self.p1-self.p2, self.zero-(self.p2-self.p1))
        self.assertEqual(self.p1-self.p2, Point(2,2))
        self.assertEqual(self.pp1-self.po1, Point(-8,2))
        
    def test_mul(self):
        self.assertEqual(self.zero*self.p1, 0)
        self.assertEqual(self.zero*self.zero, 0)
        self.assertEqual(self.p1*self.p1, 34)
        self.assertEqual(self.p1*self.p2, 18)
        self.assertEqual(self.p1*self.po1, 0)
        
    def test_cross(self):
        self.assertEqual(self.zero.cross(self.p1), 0)
        self.assertEqual(self.zero.cross(self.zero), 0)
        self.assertEqual(self.p1.cross(self.p1), 0)
        self.assertEqual(self.p1.cross(self.p2), -4)
        self.assertEqual(self.p1.cross(self.pp1), 0)
        self.assertEqual(self.p1.cross(self.pm2), 0)
        self.assertEqual(self.p1.cross(self.po1), -34)
        
    def test_len(self):
        self.assertEqual(self.zero.length(),0)
        self.assertEqual(self.p1.length(),sqrt(34))
        self.assertEqual(self.pp1.length(), self.p1.length())
        self.assertEqual(self.pm2.length(), 2*self.p1.length())
        
    def test_hash(self):
        self.assertEqual(hash(self.p1),hash(self.p1))
        self.assertEqual(hash(self.p1)!=hash(self.p2), True)
        self.assertEqual(hash(self.p1)!=hash(self.pm2), True)
        self.assertEqual(hash(self.p1)!=hash(self.pp1), True)
        self.assertEqual(hash(self.zero),hash(self.zero))
          
        
    
if __name__ == "__main__":
    unittest.main()