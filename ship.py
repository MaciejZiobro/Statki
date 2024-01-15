import sys
import random
import math

import pygame

from ppoints import Point

class Ship:
    def __init__(self, x1, y1, orientation, length):
        # współrzędne "głowy" statku, i kierunek - w prawo(True) lub w doł(False)
        self.p = Point(x1,y1)
        self.x = x1
        self.y = y1
        self.orientation = orientation
        self.length = length
        self.strike_list = []
        for i in range(self.length):
            self.strike_list.append(False)
        self.strike_draw_list = []
        for i in range(self.length):
            self.strike_draw_list.append(False)
        
        

    def __str__(self):
        return "Ship("+ str(self.x) + ", " + str(self.y) + ", " + str(self.orientation) + ", " + str(self.length)+")"
    
    @property
    def is_destroyed(self):
        for i in self.strike_list:
            if i is False:
                return False
        return True
    @property
    def is_destroyed_draw(self):
        for i in self.strike_draw_list:
            if i is False:
                return False
        return True
        
    # lista punktów zajmowyanych przez statek
    def list_of_points(self):
        list = []
        for i in range(self.length):
            list.append(Point(self.x+int(self.orientation)*i, self.y+int(not self.orientation)*i))
        return list
    
    # lista punktów zajmowaanych przez statek oraz pol sąsienich, czyli takich na których nie moze być innego statku
    def extend_list_of_points(self):
        list_of_point=[]
        # dodajemy wszystkie ptk w okolicy statku
        for i in range(self.length):
            temp_x = self.x+int(self.orientation)*i
            temp_y = self.y+int(not self.orientation)*i
        
            list_of_point.append(Point(temp_x, temp_y))
            list_of_point.append(Point(temp_x+1,temp_y))
            list_of_point.append(Point(temp_x, temp_y+1))
            list_of_point.append(Point(temp_x+1, temp_y+1))
            list_of_point.append(Point(temp_x-1,temp_y))
            list_of_point.append(Point(temp_x, temp_y-1))
            list_of_point.append(Point(temp_x-1, temp_y-1))
            list_of_point.append(Point(temp_x+1, temp_y-1))
            list_of_point.append(Point(temp_x-1, temp_y+1))
        # usuwamy te niebędące na mapie   
        list_of_point = list(set(list_of_point))
        for p in list_of_point.copy():
            if p.x > 9 or p.x < 0 or p.y >= 10 or p.y<0:
                list_of_point.remove(p)
                
        # set pozwala na zaniedbanie powtórek które wynikają z konstrukcji listy    
        return set(list_of_point)
        
    def strike(self, point): # funkcja pokazuje, które punkty zostały zestrzelone
        for count, p in enumerate(self.list_of_points()):
            if p == point:
                self.strike_list[count] = True
                
    def strike_draw(self, point): # funkcja pokazuje, które punkty zostały zestrzelone
        for count, p in enumerate(self.list_of_points()):
            if p == point:
                self.strike_draw_list[count] = True