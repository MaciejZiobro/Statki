import sys
import random
import math
import time

import pygame

from ship import Ship
from ppoints import Point
from bot import bot_move

# Lista zawierająca informacje o ilości danych statków oraz stałe definujące plansze
list_of_sizes = [1,2,3,4] # ilość statków do rozmieszczenia kolejno rozmiarów 1,2,3,4
size_of_board = 10 # rozmiar planszy
P_list_of_ships = [] # listy zaweirające statki (obiekty klasy Ship) odpowiednio gracza - P i komputera C
C_list_og_ships = []

def ships_placment(list_of_sizes):
    """Funkcja genrująca położenie statków
    Args:
        list_of_sizes (list): lista ilości statków poszczególnego rozmiaru od tyłu
    Returns:
        list: Zwraca list obiektów klasy Ship
    """
    # tworzymy zbiór punktów możliwych do losowania
    set_of_points = set()
    for x in range(10):
        for y in range(10):
            set_of_points.add(Point(x,y))
            
    ships_created = []
    for length, count in enumerate(list_of_sizes):
        ship_length =  len(list_of_sizes) - length
        for j in range(count):
            random_flag = True # bool wprowadzony aby powtarzac losowanie, aż zostaną wyznaczone poprawne punkty
            while random_flag: # Dla prawdziwej wartości flaga wskazuje, że losowanie było niepoprawne - statek nie może być zbudowany
                random_flag = False
                head_point = random.choice(list(set_of_points))
                orientation = bool(random.randint(0,1)) # w prawo(True) lub w doł(False)
                # odrzucanie puntktów poza mapą
                ship = Ship(head_point.x, head_point.y, orientation, ship_length)
                random_flag = False
                for point in ship.list_of_points():
                    if point not in set_of_points:
                        random_flag = True
                if len(set_of_points) == 0:
                    return ships_placment(list_of_sizes) 
                if random_flag is False:
                    ships_created.append(ship)
                    set_of_points -= ship.extend_list_of_points()
            
    return ships_created






### GUI
pygame.init()

# definicje kolorów
black = (0, 0, 0)
gray = (128, 128, 128)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
orange = (255, 215, 0)

# flaga sprawdzajaca czy checmy zagrać ponowanie
play_again = True

while play_again:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            play_again = False
            
    # ustawiania fps
    FPS = 60  
    clock = pygame.time.Clock()

    # inicjalizacja statków gracza i bota
    player_ships_placment = ships_placment(list_of_sizes)

    bot_ships_placment = ships_placment(list_of_sizes)
    bot_moves = bot_move(player_ships_placment) # lista ruchów bota
        
    square_size = 50 #  rozmiar pojedynczego pola
        
    # listy kwadratów, obiektów pygame.Rect służące do reprezentacji pól
    player_squares_list = [[],[],[],[],[],[],[],[],[],[]]
    bot_squares_list = [[],[],[],[],[],[],[],[],[],[]]

    # stałe związane z ustawaniem elemntów na planszy
    rect_size = 55
    y_offset = 200
    player_x_offset = 100
    bot_x_offset = 2*player_x_offset + rect_size*10 + 40

    # tworzenie pygame.Rect dla każdego pola i przypisujemy je do listy
    for x in range(10):
        for y in range(10):
            temp_square = pygame.Rect(player_x_offset+rect_size*x, y_offset+rect_size*y, square_size, square_size)
            player_squares_list[x].append(temp_square)
            
            temp_square_bot = pygame.Rect(bot_x_offset+rect_size*x, y_offset+rect_size*y, square_size, square_size)
            bot_squares_list[x].append(temp_square_bot)

    # inicjalizacja okna gry
    size = (width, height) = (1400, 900)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Statki')

    # fonty
    font_squares = pygame.font.Font(None, 40) #  font do numerowania pól
    font_end = pygame.font.Font(None, 200) # font napisów końcowych
    font_ships = pygame.font.Font(None, 60) # font liczb statków
    font_menu = pygame.font.Font(None, 40) # font przycisków w menu startowym
    
    # home page obrazek
    home_page = pygame.image.load('home_page.png')
    # zmienna, trzymająca kto zaczyna gre
    start_flag = True
    
    # część kody odpowaidająca za menu startowe
    menu_done = False 
    end_menu_done = False
    def start_menu():
        global menu_done, start_flag
        while not menu_done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    menu_done = True
                    
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        x1, y1 = event.pos
                        if player_start_text_rect.left<= x1 <= player_start_text_rect.right and player_start_text_rect.top <= y1 <= player_start_text_rect.bottom:
                            start_flag = True
                            menu_done = True
                        elif bot_start_text_rect.left<= x1 <= bot_start_text_rect.right and bot_start_text_rect.top <= y1 <= bot_start_text_rect.bottom:
                            start_flag = False
                            menu_done = True
                        elif rand_start_text_rect.left<= x1 <= rand_start_text_rect.right and rand_start_text_rect.top <= y1 <= rand_start_text_rect.bottom:
                            start_flag = random.choice([True, False])
                            menu_done = True
                    
            screen.fill(black)
            screen.blit(home_page, pygame.Rect(0, 0, size[0], size[1]))
            
            # tytuł
            start_title_surf = font_end.render("Statki", True, orange)
            start_title_rect = start_title_surf.get_rect(center=(width // 2, height // 4))
            screen.blit(start_title_surf, start_title_rect)
            
            # 3 przyciski odpowaiedzialne za wybór kto zaczyna
            player_start_text_surf = font_menu.render("Ty zaczynasz", True, blue)
            player_start_text_rect = player_start_text_surf.get_rect(center=(width // 4, 2*height // 3))
            screen.blit(player_start_text_surf, player_start_text_rect)
            
            rand_start_text_surf = font_menu.render("Losowa kolejność", True, blue)
            rand_start_text_rect = rand_start_text_surf.get_rect(center=(2*width // 4, 2*height // 3))
            screen.blit(rand_start_text_surf, rand_start_text_rect)
            
            bot_start_text_surf = font_menu.render("Zaczyna przeciwnik", True, blue)
            bot_start_text_rect = bot_start_text_surf.get_rect(center=(3*width // 4, 2*height // 3))
            screen.blit(bot_start_text_surf, bot_start_text_rect)
            
            pygame.display.flip()
            clock.tick(FPS)
    
    # częśc kodu odpowiadająca za menu końcowe
    def end_menu():
        global play_again, end_menu_done
        
        screen.fill(black)
        # napis z pytaniem
        end_title_surf = font_ships.render("Czy chcesz zagrać ponownie?", True, orange)
        end_title_rect = end_title_surf.get_rect(center=(width // 2, height // 4))
        screen.blit(end_title_surf, end_title_rect)
        # 2 przyciski odpowaiedzialne za wybór czy chcemy zagrać ponownie czy wyjść z gry
        play_again_text_surf = font_menu.render("Tak", True, green)
        play_again_text_rect = play_again_text_surf.get_rect(center=(width // 3, 2*height // 3))
        screen.blit(play_again_text_surf, play_again_text_rect)
            
        quit_text_surf = font_menu.render("Wyjdź z gry", True, blue)
        quit_text_rect = quit_text_surf.get_rect(center=(2*width // 3, 2*height // 3))
        screen.blit(quit_text_surf, quit_text_rect)
        
        pygame.display.flip()
        clock.tick(FPS)
        
        while not end_menu_done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    end_menu_done = True
                    
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        x1, y1 = event.pos
                        if play_again_text_rect.left<= x1 <= play_again_text_rect.right and play_again_text_rect.top <= y1 <= play_again_text_rect.bottom:
                            play_again = True
                            end_menu_done = True
                        elif quit_text_rect.left<= x1 <= quit_text_rect.right and quit_text_rect.top <= y1 <= quit_text_rect.bottom:
                            play_again = False
                            end_menu_done = True
                            

            
        

    # inicjaliza obrazków
    galeon = pygame.image.load('galeon.png')
    shot_galeon = pygame.image.load('shot_galeon.png')
    sunk_galeon = pygame.image.load('sunk_galeon.png')
    sea = pygame.image.load('sea.png')
    sea_used = pygame.image.load('sea_used.png')
    sea_marked = pygame.image.load('sea_marked.png')
    sea_current_bot_move = pygame.image.load('sea_current_move.png')

    # zmienne pomocnicze, słuzące do obsługi pól - wyświtlania czy zostały użyte/zaznaczone
    bot_points_used = [] # punkty w które bot strzelał
    player_points_used = [] # punkty w które gracz strzelał
    player_points_marked = [] # punkty oznaczone przez gracza   

    done = False  # flaga kończąca grę
    bot_counter = -1 # licznik ruchów bota
    bot_move_current = bot_moves[0] # aktualny ruch bota
    player_move_flag = True # flaga określająca czyja jest tura
    win_flag = [True, False] # true - wygrał gracz, false - wygrał bot, druga wartoś pokazuje czy ktokolwiek wygrał
    first_move_flag = False # flaga oznaczający czy odbył się pierwszy ruch
    bot_delay = 15 # opóźnienie ruchu bota
    bot_delay_counter = 0 # licznik opóźnienia ruchu bota - pozwala faktycznie sprawdzić ile mineło czasu (klatek)

    start_menu() # wywołanie menu startowego
    
    # ustawienie flagi określającej czyja jest tura
    if start_flag is True:
        player_move_flag = True
    else:
        player_move_flag = False

    while not done: # główna pętla gry
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            # obsługa myszy gracza
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # obsługa strzałów
                if event.button == 1:
                    x1, y1 = event.pos
                    for x in range(10):
                        for y in range(10):
                            rect = bot_squares_list[x][y]
                            if rect.left<= x1 <= rect.right and rect.top <= y1 <= rect.bottom:
                                if player_move_flag is True:
                                    player_move_flag = False
                                    first_move_flag = True
                                    player_points_used.append(Point(x,y))
                                    for ship in bot_ships_placment:
                                        for point in ship.list_of_points():
                                            if point == Point(x,y): # sprawdzenie czy na danym polu jest statek
                                                ship.strike(Point(x,y))
                                                ship.strike_draw(Point(x,y))
                                                
                # obsługa pomocniczych oznacczeń pól             
                elif event.button == 3:
                    x1, y1 = event.pos
                    for x in range(10):
                        for y in range(10):
                            rect = bot_squares_list[x][y]
                            if rect.left<= x1 <= rect.right and rect.top <= y1 <= rect.bottom:
                                if Point(x,y) not in player_points_marked:
                                    player_points_marked.append(Point(x,y))
                                else:
                                    player_points_marked.remove(Point(x,y))
                    
        # Warunek kończenia gry gracza
        player_end_flag = True
        for ship in bot_ships_placment:
            if not ship.is_destroyed:
                player_end_flag = False
        
        if player_end_flag is True:
            done = True
            player_move_flag = True
            win_flag = [True, True]
            
        # ruch bota
        if player_move_flag is False:
            if bot_delay_counter >= bot_delay:
                bot_counter += 1
                bot_move_current = bot_moves[bot_counter]
                player_move_flag = True    
                first_move_flag = True
                bot_delay_counter = 0
            else:
                bot_delay_counter += 1
            
        #warunek kończenia gry bota
        bot_end_flag = True
        for ship in player_ships_placment:
            if not ship.is_destroyed_draw:
                bot_end_flag = False
        
        if bot_end_flag is True:
            done = True
            win_flag = [False, True]
                    
        screen.fill(black)
        
        # Napis tury
        turn_text = ""
        if player_move_flag:
            turn_text = "Twoja tura"
        else:
            turn_text = "Tura przeciwnika"
            
        turn_text_surf = font_ships.render(turn_text, True, orange)
        turn_text_rect = turn_text_surf.get_rect(center=(width // 2, y_offset // 2))
        screen.blit(turn_text_surf, turn_text_rect)
        
        # dodanie podpisów nad i obok pól
        text_int = 65
        num_int = 1      
        text_y_offset = y_offset - 35
        text_player_x_offset = player_x_offset+25
        text_bot_x_offset = bot_x_offset + 25
        
        for x in range(10):
            player_text_surf = font_squares.render(chr(text_int), True, white)
            player_text_rect = player_text_surf.get_rect(center=(text_player_x_offset+rect_size*x, text_y_offset))
            screen.blit(player_text_surf, player_text_rect)
            
            bot_text_surf = font_squares.render(chr(text_int), True, white)
            bot_text_rect = bot_text_surf.get_rect(center=(text_bot_x_offset+rect_size*x, text_y_offset))
            screen.blit(bot_text_surf, bot_text_rect)
            
            text_int += 1

        for y in range(10):
            player_text_surf = font_squares.render(str(num_int), True, white)
            player_text_rect = player_text_surf.get_rect(center=(text_player_x_offset - rect_size, text_y_offset + rect_size*y + 60))
            screen.blit(player_text_surf, player_text_rect)
            
            bot_text_surf = font_squares.render(str(num_int), True, white)
            bot_text_rect = bot_text_surf.get_rect(center=(text_bot_x_offset - rect_size, text_y_offset + rect_size*y + 60))
            screen.blit(bot_text_surf, bot_text_rect)
            
            num_int += 1
        
        # dodanie ilości statków pod plansze
        ships_y = text_y_offset+10*rect_size+120
        ships_x = player_x_offset + 11
        for ship in player_ships_placment:
            if ship.is_destroyed_draw:
                player_ship_text_surf = font_ships.render(str(ship.length), True, red)
            else:
                player_ship_text_surf = font_ships.render(str(ship.length), True, white)
                
            player_ship_text_rect = player_ship_text_surf.get_rect(center=(ships_x, ships_y))
            screen.blit(player_ship_text_surf, player_ship_text_rect)
            ships_x += 58
        
        ships_x += player_x_offset + 15
        for ship in bot_ships_placment:
            if ship.is_destroyed_draw:
                player_ship_text_surf = font_ships.render(str(ship.length), True, red)
            else:
                player_ship_text_surf = font_ships.render(str(ship.length), True, white)
                
            player_ship_text_rect = player_ship_text_surf.get_rect(center=(ships_x, ships_y))
            screen.blit(player_ship_text_surf, player_ship_text_rect)
            ships_x += 58
        
        # rysowanie wszytki pól z tłem morza
        for x in range(10):
            for y in range(10):
                #pygame.draw.rect(screen, gray, player_squares_list[x][y])
                #pygame.draw.rect(screen, gray, bot_squares_list[x][y])
                screen.blit(sea, player_squares_list[x][y])
                screen.blit(sea, bot_squares_list[x][y])
                
        # zaznaczenie pól użytych przez gracza i bota
        for point in bot_points_used:
            #pygame.draw.rect(screen, white, player_squares_list[point.x][point.y])
            screen.blit(sea_used, player_squares_list[point.x][point.y])
        
        for point in player_points_used:
            #pygame.draw.rect(screen, white, bot_squares_list[point.x][point.y])
            screen.blit(sea_used, bot_squares_list[point.x][point.y])
            
        # rysowanie statków z uwzględnieniem rozróżnienia na zniszczone, trafione i nietrafione
        for ship in player_ships_placment:
            for count, point in enumerate(ship.list_of_points()):
                if ship.is_destroyed_draw:
                    #pygame.draw.rect(screen, orange, bot_squares_list[point.x][point.y])
                    screen.blit(sunk_galeon, player_squares_list[point.x][point.y])
                elif ship.strike_draw_list[count] is True:
                    # pygame.draw.rect(screen, red, player_squares_list[point.x][point.y])
                    screen.blit(shot_galeon, player_squares_list[point.x][point.y])
                else:
                    screen.blit(galeon, player_squares_list[point.x][point.y])
                    
        for ship in bot_ships_placment:
            for count, point in enumerate(ship.list_of_points()):
                if ship.is_destroyed:
                    #pygame.draw.rect(screen, orange, bot_squares_list[point.x][point.y])
                    screen.blit(sunk_galeon, bot_squares_list[point.x][point.y])
                elif ship.strike_draw_list[count] is True:
                    #pygame.draw.rect(screen, red, bot_squares_list[point.x][point.y])
                    screen.blit(shot_galeon, bot_squares_list[point.x][point.y])
        if first_move_flag:
            for ship in player_ships_placment:
                for point in ship.list_of_points():
                    if point == bot_move_current:     
                        ship.strike_draw(point)
                    
        # pola oznaczone przez gracza
        for point in player_points_marked:
            #pygame.draw.rect(screen, white, bot_squares_list[point.x][point.y])
            screen.blit(sea_marked, bot_squares_list[point.x][point.y])
            
        # zaznaczenie ostatniego ruchu bota czerwoną kropką
        #pygame.draw.rect(screen, blue, player_squares_list[bot_move_current.x][bot_move_current.y])
        if first_move_flag:
            screen.blit(sea_current_bot_move, player_squares_list[bot_move_current.x][bot_move_current.y])
            bot_points_used.append(bot_move_current)

        pygame.display.flip()
        clock.tick(FPS)
        
    # wyświetalanie napisów końcowych   
    if win_flag[1] is True:
        if win_flag[0] is True:
            end_text_surf = font_end.render("Wygrałeś", True, orange)
            end_text_rect = end_text_surf.get_rect(center=(width // 2, height // 2))
            screen.blit(end_text_surf, end_text_rect)
            pygame.display.flip()
            time.sleep(5)
        elif win_flag[0] is False:
            end_text_surf = font_end.render("Przegrałeś", True, red)
            end_text_rect = end_text_surf.get_rect(center=(width // 2, height // 2))
            screen.blit(end_text_surf, end_text_rect)
            pygame.display.flip()
            time.sleep(5)
    end_menu()


pygame.quit() 