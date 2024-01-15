import sys
import random
import math
import time

import pygame

from ship import Ship
from ppoints import Point

def ship_space(point, points_used, ships_placment):
    """Funkcja, mówi ile miejsca w obu kierunkach jest na potencjalny statek.
       Celem, jest umożliweinie wyklucznia pewnych pól ze względu na to, że statki danych rozmiarów nie zmieściłyby się na nich

    Args:
        point (ppoint.Point): Punkt, w którm sprawdzamy ship_space
        points_used (list): lista puntków zużytych, takich w które strzelono albo na których nie może być statku
        ships_placment (list): Lista obiektów typu Ship, mówiąca o ich rozmieszczeniu
        
    Returns:
        space (list): Lista dów wartości typu bool, mówiących czy w danym kierunku mógłby znajdować się statek danego rozmiaru
    """
    min_size = 4
    for ship in ships_placment:
        if ship.is_destroyed is False:
            if ship.length<=min_size:
                min_size = ship.length
    
    x = point.x
    y = point.y
    counter_x = 1
    counter_y = 1
    for j in range(min_size-1):
        i = j + 1
        if Point(x+i, y) not in points_used and x+i<10:
            counter_x += 1
        if Point(x-i, y) not in points_used and x-i>=0:
            counter_x += 1
        if Point(x, y+i) not in points_used and y+i<10:
            counter_y += 1
        if Point(x, y-i) not in points_used and y-i>=0:
            counter_y -= 1
        
    return [bool(counter_x>=min_size), bool(counter_y>=min_size)]



def new_move(ships_placment, points_used, current_ship):
    """Funkcja ma za zadanie, określić ruch bota w sytuacji, w której nie wie gdzie może znajdować się jakiś statek (nie ma żadanego statku, w który trafił i nie jest zatopiony)

    Args:
        ships_placment (list): List obiektów typu ship, mówiąca o rozmieszczeniu statków gracza
        points_used (list): Lista obiektów typu Point, mówi o punktach na których na pewno nie ma niezatopionych statków

    Returns:
        ppoints.Point: zwraca punkt, w który strzelił bot
    """
    random_flag = True # flaga, do sprawdzania poprawności losowań
    while random_flag:
        random_flag = False
        x = random.randint(0,9)
        y = random.randint(0,9)
        # Sprawdzenie czy punkt jest poprawny
        if True in ship_space(Point(x,y), points_used, ships_placment):
            for i in points_used:
                if i.x == x and i.y == y:
                    random_flag = True
        else:
            random_flag = True
        # Właściwy kod ruchu
        if random_flag is False:
            points_used.append(Point(x, y))
            for ship in ships_placment:
                for ship_point in ship.list_of_points():
                    if ship_point == Point(x,y):
                        ship.strike(Point(x,y))
                        if ship.is_destroyed:
                            points_used.extend(list(ship.extend_list_of_points()))
                            current_ship.clear()
                            return Point(x,y)
                        current_ship.append(Point(x,y))
                        return Point(x,y)
            return Point(x,y)
            
def after_strike_move(ships_placment, points_used, current_ship):
    """_summary_

    Args:
        ships_placment (ship.Ship): List obiektów typu ship, mówiąca o rozmieszczeniu statków gracza
        points_used (list): Lista obiektów typu Point, mówi o punktach na których na pewno nie ma niezatopionych statków
        current_ship (list): Lista obiektów typu Point, mówi o punktach statku, który aktualnie zatapia bot.

    Returns:
        ppoints.Point: Punkt, w który strzlił bot
    """
    random_flag = True # flaga, do sprawdzania poprawności losowań
    while random_flag:
        random_flag = False
        x = 0
        y = 0
        if len(current_ship) == 1: # gdy znany jets tylko jednen ptk ostrzlywywanego statku
            direction = bool(random.randint(0,1)) # True - prawo, Dalse - w dół
            if ship_space(current_ship[0], points_used, ships_placment)[direction] is True:
                x = current_ship[0].x + (int(direction))*random.choice([-1,1])
                y = current_ship[0].y + (int(not direction))*random.choice([-1,1])
                if x < 0  or x>=10 or y<0 or y>=10:
                    random_flag = True
                if Point(x,y) in points_used:
                    random_flag = True
            if random_flag is False:
                points_used.append(Point(x,y))
                for ship in ships_placment:
                    for ship_point in ship.list_of_points():
                        if ship_point == Point(x,y):
                            ship.strike(Point(x,y))
                            if ship.is_destroyed:
                                current_ship.clear()
                                points_used.extend(ship.extend_list_of_points())
                                return Point(x,y)
                            current_ship.append(Point(x,y))
                            return Point(x,y)
                return Point(x,y)
            
        if len(current_ship) >= 2: # Gdy znany jest więcej niż jeden ptk ostrzliwywanego statku - pozwala to stweirdzić jednoznacznie jego kierunek
            random_flag = True
            if current_ship[0].x == current_ship[1].x:
                direction = True
                x = current_ship[0].x
                y = random.choice([max(y.y for y in current_ship)+1, min(y.y for y in current_ship)-1])
                if y<10 and y>=0:
                    random_flag = False
            elif current_ship[0].y == current_ship[1].y:
                direction = False
                y = current_ship[0].y
                x = random.choice([max(x.x for x in current_ship)+1, min(x.x for x in current_ship)-1])
                if 0 <= x < 10:
                    random_flag = False
                
            if Point(x,y) in points_used:
                random_flag = True
                 
            if random_flag is False:
                points_used.append(Point(x,y))
                for ship in ships_placment:
                    for ship_point in ship.list_of_points():
                        if ship_point == Point(x,y):
                            ship.strike(Point(x,y))
                            if ship.is_destroyed:
                                points_used.extend(ship.extend_list_of_points())
                                current_ship.clear()
                                return Point(x,y)
                            current_ship.append(Point(x,y))
                            return Point(x,y)
                return Point(x,y)
                
                            
def bot_move(ships_placment):

    """Głowna funckja operująca ruchami bota, zapisuje do tablicy wszytkie ruchy od początku do momentu, w którym bot by wygrał.
    Args:
        ships_placment (ship.Ship): List obiektów typu ship, mówiąca o rozmieszczeniu statków gracza

    Returns:
        list: lista zawierająca ptk, w które bot strzela w kolejności w czasie
    """
    list_of_moves = []
    end_flag = False # flaga końca gry (ta flaga sprawdza tylko czy bot wygrał)
    move_flag = False # bool mówiący, czy został wykonany już ruch w tym przjściu pętli while
    points_used = [] # list trzyma ptk, w które bot strzelał oraz te w które nie może strzelić np, ze względu na sąsiadujący statek
    list_of_moves = [] 
    current_ship = [] # lista trzymająca współrzędne puntków aktualnie "ostrzliwanego" statku
    while not end_flag:
        move_flag = False
        if len(current_ship) == 0:
            list_of_moves.append(new_move(ships_placment, points_used, current_ship))
            move_flag = True
      
        if len(current_ship)>0 and move_flag is False:
            list_of_moves.append(after_strike_move(ships_placment, points_used, current_ship))
            # Sprawdzenie warunku końca gry
        end_flag = True          
        if False in (ship.is_destroyed for ship in ships_placment):
            end_flag = False
          
    return list_of_moves     