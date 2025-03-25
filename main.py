from collections import defaultdict
import argparse
import time
from colorama import Fore

def open_puzzle(puzzle) -> list: # Check
    '''
    Funkcja zamienia plik.txt na macierz z tymi samymi warościami co w pliku

    Args:
        puzzle: Plik txt z reprezentacją naszej planszy i podanymi wymiarami w 1 linijce

    Returns:
        Macierz z wartościami z pliku
    '''

    file = open(puzzle, "r")
    txt = file.read()
    lines = txt.split("\n")
    lines.remove(lines[0])
    ans = [list(map(int, line.split("\t"))) for line in lines] # Tworzenie macierzy
    return ans




def making_dict(matrix:list) -> dict: # Check

    '''
    Ta funkcja zmienia nam naszą macierz na słownik z koordynatami każdego z klocków
     w postaci listy tupli[(wiersz, kolumna)]
    Args:
        matrix: Macierz z reprezentacją naszych klocków
    Returns:
        Słownik z koordyntami każdego klocka gdzie kolor kolor klocka to key a koordynaty to values
    '''

    ans = {}
    for row in range(len(matrix)):
        for col in range(len(matrix[row])):
            curr_value = matrix[row][col]
            if curr_value in ans:
                ans[curr_value].append((row, col))
            else:
                ans[curr_value] = [(row, col)] # Jeśli pierwszy raz znajdujemy część klocka to ją dodajemy
    return ans

def finding_pieces(fullmatrix:list, missingmatrix:list) -> dict: # Check
    '''
    Funkcja ta na podstawie zapełnionej macierzy i macierzy do
    wypełnienia znajduje nam brakującego klocki do naszej układanki
    i zwraca nam je w postaci słownika z koordynatami, które ustalają nam kształt klocka

    Args:
        fullmatrix: Macierz bez pustych miejsc w której są wszystkie klocki których możemy użyć
        missingmatrix: Macierz niezapełniona w której nie ma niektorych klocków z fullmatrix

    Returns:
         Słownik w którym są wszystkie koordynaty klocków których brakuje missingmatrix

    '''
    missing_pieces = {}
    full = making_dict(fullmatrix)
    missing = making_dict(missingmatrix)
    for i in full:
        if i not in missing:
            missing_pieces[i] = full[i]
    return missing_pieces


def notation(coords: dict) -> dict: # Check
    '''
    Zmienia koordynaty klocków ze słownika na notacje (0,0), (0,1), (1,0) itp.
    Innymi słowy upraszcza koordynaty klocków do wpasowania
    Przykład:
    4:[(4,9),(4,10),(4,8),(3,10)] -> 4:[(0,0),(0,1),(0,-1),(-1,1)]

    Args:
        coords: Koordynaty brakujących elementów w postaci starych koordyantów z fullmatrix

    Returns:
         Słownik z tymi samymi klockami, ale z uproszczoną notacją koordynatów
    '''

    ans ={}
    for i in coords:
        x = coords[i]
        ans[i] = [(0, 0)]
        tuple1 = x[0]
        for j in range(1, len(x)):
            added_tuple = tuple(x - y for x,y in zip(x[j], tuple1))
            ans[i].append(added_tuple)
    return ans


def empty_space(matrix:list) -> list: # Check
    '''
    Znajduje nam puste miejsca z w naszej macierzy do wypełnienia

    Args:
        matrix: macierz z pustymi miejscami (0)

    Returns:
         Lista z koordynatami pustych miejsc(0)
    '''

    empty = []
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] == 0:
                empty.append((i, j))
    return empty

'''
ZMIENNE
'''
# ZMIENNE Z PARSOWANIA
parser = argparse.ArgumentParser(description="Układanie puzzli")
parser.add_argument("-p", "--Ulozona_plansza", type=str, help="Plik.txt z plansza do ułożenia")
parser.add_argument("-plansza", "--Plansza_do_ulozenia", type=str, help="Plik.txt z planszą do ułożenia")
parser.add_argument("-n","--czas_ukladania", type=float, help="liczba typu float z delayem wyświetlania kroków rozwiązania")
args = parser.parse_args()
calaPlansza = args.Ulozona_plansza
pustaPlansza = args.Plansza_do_ulozenia
delay = args.czas_ukladania
if delay == None:
    delay = 0 # jeśli nie damy warunku -n to delay = 0

# Zmienne potrzebne do rozwiązania puzzli
matrixAfter = open_puzzle(calaPlansza)
matrixBefore = open_puzzle(pustaPlansza)
full_dict = making_dict(matrixAfter)
start_dict = making_dict(matrixBefore)
missing_blocks = finding_pieces(matrixAfter, matrixBefore)
blocks = notation(missing_blocks)
empty_spaces = empty_space(matrixBefore)

'''
ROZWIĄZYWANIE
'''

def place_block(matrix: list, block: list, row: int, col: int, block_id: int) -> None:

    '''
    Stawia klocek na konkretnym miejscu w macierzy

    Args:
        matrix: Macierz do której wstawiamy klocka
        block: Kształt konkretnego klocka w postaci list tupli(wiersz, kolumna) zapisnaego w notacji notation()
        row: wiersz wkładania pola startowego (0,0)
        col: kolumna wkładania pola startowego (0,0)
        block_id: "Kolor" klocka
    Returns:
        None
    '''

    for x, y in block:
        matrix[row + x][col + y] = block_id

def remove_block(matrix:list, block:tuple, row:int, col:int) -> None:
    '''
    Analogiczna funkcja do place_block()
    Usuwa klocek z macierzy

    Args:
       matrix: Macierz do której wstawiamy klocka
        block: Części konkretnego klocka w postaci tupli(x,y)
        row: wiersz wkładania pola startowego (0,0)
        col: kolumna wkładania pola startowego (0,0)
    Returns:
        None
    '''
    for x, y in block:
        matrix[row + x][col + y] = 0


def printMatrix(matrix: list) -> None:
    '''
    Wywołuje nam macierz
    Funkcja ta ma w sobie także słownik z odpowiednikami kolorów dla kolejnych liczb
    Używamy tutaj modułu colorama do kolorowania kolejnych wartosci z macierzy
    Macierz jest także sformatowana i ograniczona za pomocą width aby 2 cyfrowe liczby nie nisczyczły wyglądu

    Args:
        matrix: macierz z reprezentacją naszych puzzli
    Returns:
        None
    '''
    width = max(max(len(str(element)) for wiersz in matrix for element in wiersz), 2) + 1 # Szuka najszerszego elementu i dostoswuje do niego wolną przestrzeń
    colors = {
    0: Fore.BLACK,
    1: Fore.LIGHTRED_EX,
    2: Fore.LIGHTCYAN_EX,
    3: Fore.YELLOW,
    4: Fore.LIGHTBLUE_EX,
    5: Fore.LIGHTBLACK_EX,
    6: Fore.CYAN,
    7: Fore.WHITE,
    8: Fore.RED,
    9: Fore.GREEN,
    10: Fore.LIGHTYELLOW_EX,
    11: Fore.BLUE,
    12: Fore.MAGENTA,
    13: Fore.CYAN
    } # Słownik ze wszystkimi kolorami
    for row in matrix:
        for element in row:
            print(f"{colors[element]}{str(element):<{width}}", end=" ") # Printujemy z dostosowaną szerokoscia i kolorem
        print("")
    print("\n")



def rotate_coordinates(coordinates:tuple) -> list[tuple[int, int]]: #check
    '''
    Obraca RAZ klocek o 90 stopni

    Args:
    coordinates: część koordynatów klocka w postaci tupla

    Returns:
        Obrócona częśc klocka w postacia tupla
    '''
    return [(y, -x) for x, y in coordinates]

def rotate(coordinates:tuple, angle:int, mirror:bool) -> tuple: #check
    '''
    Bardziej dokładne obracanie w którym uwzględnione jest obracanie lustrzane i więcej niż 90 stopni

    Args:
        coordinates: koordynaty klocka w postaci tupli
        angle: Kąt w postaci integera(0-3), który mówi o ile obracamy klocek angle * 90stopni
        mirror: Bool, który mówi czy klocek jest odbity lustrzanie czy nie
    Returns:
        Obrócony tuple
    '''
    new_cords = coordinates
    for i in range(angle):
        new_cords = rotate_coordinates(new_cords) # Używamy funkcji powyżej okreslona ilosc razy
    if mirror:
        new_cords = [(x, -y) for x, y in new_cords]
    return new_cords


def can_place(matrix: list, block: list, row: int, col: int) -> bool: # Check
    '''
    Przechodzi przez każdy element klocka i sprawdza czy można postawić klocka na wybranym miejscu

    Args:
        matrix: Macierz do ułożenia przez klocki
        block: Kształ Klocka który chcemy włożyć do macierzy
        row: wiersz wkładania
        col: kolumna wkładania

    Returns:
        Zwraca prawde gdy można wstawić klocek lub fałsz gdy nie można
    '''
    for x, y in block:
        if row + x < 0 or row + x >= len(matrix) or col + y < 0 or col + y >= len(matrix[0]) or matrix[row + x][col + y] != 0: # Edge cases
            return False
    return True


def finding_places(blocks:dict, matrix:list) -> dict:# Check
    '''
    Znajduje wszystkie możliwe pola w które można włożyc wszystkie klocki

    Args:
        blocks: Słownik z klockami w notacji do wstawienia
        matrix: Macierz z pustymi miejscami które są do wypełnienia
    Returns:
        Słownik z każdą możliwa pozycją klocka gdzie (i, j) to koordyanty początkowe, angle kąt obrotu, mirror to
        czy jest lustrzane odbicie czy nie. Zwraca tylko pierwszy koordynat (0,0) klocka
        Przykładowo:
        4:[(0,9,1,True)] oznacza ze klocek 4 zaczyna ulozenie w punkcie (0,9) jest obrocony o 90stopni * 1 i jest odbity lustrzanie
    '''
    legal_places = defaultdict(list) # Uzywamy defaultdicta by moc swobodnie appendowac do slownika
    for block_id, block in blocks.items(): # Bierzemy ostatni klocek z listy i jego ksztalt z funkcji notation()
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                if matrix[i][j] == 0:
                    for mirror in [False, True]:
                        for angle in range(4):
                            temp_block = rotate(block, angle, mirror) # temp_block to lista tupli jednego konkretnego kształtu
                            if can_place(matrix, temp_block, i, j): # Sprawdzamy czy klocek można wpasować w to miejsce
                                legal_places[block_id].append((i, j, angle, mirror)) # Jeśli można wstawić to dodajemy do odpowiedzi pole startowe z indeksami pola startowego
    return legal_places


def solve(blocks: dict, matrix: list, places_of_blocks: dict) -> bool: #check
    '''
    Funkcja rekurencyjnie rozwiązująca macierz. Działanie polega na braniu ostatniego elementu ze słownika z blokami
    i następnie przechodzenie przez liste legalnych pól położenia klocka i dopasowywanie klocka względem planszy
    W tym momencie pokazujemy naszą macierz i następnie znowu wchodzimy do naszej funkcji. Jeśli włożenie klocka się
    nie powiedzie to wracamy do poprzedniego klocka i zmieniamy jego obrót i legalne pole.

    Args:
         blocks: Domyśle ustawienie klocków do wypełnienia w macierzy zapisane w slowniku prze funkcje notation()
         matrix: Macierz do wypełnienia
         places_of_blocks: Słownik ze wszystkimi możliwymi kombinacjami włożenia klocka startowego stworzony przez funkcje
            finding_places

    Returns:
        Zwraca prawde, gdy ułożymy plansze z sukcesem i Fałsz gdy próba zakończy się niepowodzeniem.
    '''
    if not blocks:
        return True
    color, shape = blocks.popitem() # Bierzemy ostatni element ze słownika
    legal_places = places_of_blocks[color] # Legalne pola tego jednego klocka

    for start in legal_places: # Przechodzimy przez liste startowych pól
        row, col, angle, mirror = start
        rotated_shape = rotate(shape, angle, mirror) # Obracamy kształt klocka tak jak mówia nam parametry z finding_places()

        if can_place(matrix, rotated_shape, row, col): # Jeśli możemy wstawić klocek to go wstawiamy i printujemy macierz
            place_block(matrix, rotated_shape, row, col, color)
            time.sleep(delay)
            printMatrix(matrix)

            if solve(blocks, matrix, places_of_blocks) == True: # Znowu robimy to samo tylko z nowym klockiem
                return True

            remove_block(matrix, rotated_shape, row, col)
    blocks[color] = shape # Klocek sie nie wstawil wiec wraca on do slownika by ponownie go użyć
    return False # Jeśli klocek nie jest mozliwy do wstawienia to wracamy do ifa wywouljącego funkcja i ponawiamy wstawianie z innym ulozeniem





starting_points = finding_places(blocks, matrixBefore) # Możliwości wstawienia klocków


solve(blocks, matrixBefore, starting_points) # Wywoływanie rozwiązania
