import collections
import copy
import time

class Car:                                                                          # kazde auto je jeden objekt s vlastnou farbou, polohou, velkostou a nasmerovanim
    def __init__(self, color, size, x, y, direction):
        self.color = color
        self.size = size                                                            # "2" alebo "3"
        self.x = x
        self.y = y
        self.direction = direction                                                  # "h" alebo "v"


class Node:                                                                         # kazdy uzol je objekt s polom aut, rodicom, operatorom, aktualnou mapou priestoru
    def __init__(self, cars, parent, operator, mapa):
        self.cars = cars                                                            # pole aut s ich aktualnymi polohami x, y v priestore
        self.parent = parent                                                        # uzol, z ktoreho sme sa dostali do tohto uzla
        self.operator = operator                                                    # o aky posun s akym autom sa jedna napr. LEFT(cervene, 1)
        self.mapa = mapa                                                            # mapa aktualneho priestoru

    def code_name_of_node(self, mapa):                                              # zakoduje mapu priestoru do stringu
        map_string = ""
        for i in range(rows):
            for j in range(columns):
                map_string += mapa[i][j]
        return map_string


def create_map(cars):                                                               # vytvori pociatocnu mapu priestoru na zaklade zadanych aut
    mapa = []
    for x in range(0, 6):
        mapa.append(list("------"))

    for car in cars:
        if car.direction == "h":
            for i in range(int(car.y), int(car.y) + int(car.size)):
                mapa[int(car.x)][i] = car.color[0]

        else:
            for i in range(int(car.x), int(car.x) + int(car.size)):
                mapa[i][int(car.y)] = car.color[0]

    return mapa


def find_sequence_to_red_final_position(final_node):                                # vypise postupnost posunov do ciela
    node = final_node
    moves = []
    while node.parent != None:                                                      # prehladava rodicov uzlov az kym nenarazi na root uzol (povodny stav na vstupe)
        moves.append(node.operator)
        node = node.parent
    moves = moves[::-1]
    for i in range(len(moves)):
        print(moves[i])
    print(len(moves))
    return 1


def can_move_n_steps(car, state, n, way):                                           # zisti, ci sa auto moze pohnut do daneho smeru o 1 krok
    if way == "L":
        if int(state.cars[car].y) - n < 0:                                          # nie, ak by auto vyslo z mapy v lavej casti
            return False
        if state.mapa[int(state.cars[car].x)][int(state.cars[car].y) - n] == "-":   # ano, ak je policko, kam chce auto ist volne
            return True

    elif way == "R":
        if int(state.cars[car].y) + int(state.cars[car].size) + n - 1 >= columns:   # nie ak by auto vyslo z mapy v pravej casti
            return False
        if state.mapa[int(state.cars[car].x)][int(state.cars[car].y) + int(state.cars[car].size) + n - 1] == "-":
            return True

    elif way == "U":
        if int(state.cars[car].x) - n < 0:                                          # nie, ak by auto vyslo z mapy v hornej casti
            return False
        if state.mapa[int(state.cars[car].x) - n][int(state.cars[car].y)] == "-":
            return True

    elif way == "D":
        if int(state.cars[car].x) + int(state.cars[car].size) - 1 + n >= rows:      # nie, ak by auto vyslo z mapy v dolnej casti
            return False
        if state.mapa[int(state.cars[car].x) + int(state.cars[car].size) - 1 + n][int(state.cars[car].y)] == "-":
            return True

    return False                                                                    # nie, ak je na danom policku ine auto


def LEFT(prev_state, car, move):                                                    # prev_state = rodic, car = index auta v poli aut stavu, move = pohni sa o 1
    if can_move_n_steps(car, prev_state, move, "L"):
        new_map = copy.deepcopy(prev_state.mapa)                                    # deepcopy mapy rodicovskeho uzla
        new_cars = []

                                                                                    # zmaze auto, ktorym hybeme v mape
        for i in range(int(prev_state.cars[car].y), int(prev_state.cars[car].y) + int(prev_state.cars[car].size)):
            new_map[int(prev_state.cars[car].x)][i] = "-"

                                                                                    # skopiruje do noveho zoznamu aut pozicie aut z rodicovskeho uzla
        for car_copy in prev_state.cars:
            new_cars.append(Car(copy.deepcopy(car_copy.color), copy.deepcopy(car_copy.size), copy.deepcopy(car_copy.x), copy.deepcopy(car_copy.y), copy.deepcopy(car_copy.direction)))

                                                                                    # vlozi auto do mapy na pozicie, kam sa pohne
        for i in range(0, int(prev_state.cars[car].size)):
            new_map[int(prev_state.cars[car].x)][int(prev_state.cars[car].y) - move + i] = prev_state.cars[car].color[0]

        new_cars[car].y = str(int(new_cars[car].y) - move)                          # update y suradnice pohnuteho auta vlavo v poli aut

                                                                                    # vytvori novy uzol, v ktorom je uz auto pohnute vlavo o 1 krok
        new_state = Node(new_cars, prev_state, "LEFT(" + prev_state.cars[car].color[:] + ", " + str(move) + ")", new_map)
        coded_map = new_state.code_name_of_node(new_map)
        if coded_map not in visited_nodes:                                          # kontrola, ci sme tento stav uz predtym neprehladali
            visited_nodes.append(coded_map)
            return new_state
        else:
            return None                                                             # ak sme ho uz navstivili, tak ho preskocime a nepridame do stacku na dalsie prehladanie
    else:
        return None


def RIGHT(prev_state, car, move):                                                   # princip rovnaky ako pri LEFT()
    if can_move_n_steps(car, prev_state, move, "R"):
        new_map = copy.deepcopy(prev_state.mapa)
        new_cars = []

        for i in range(int(prev_state.cars[car].y), int(prev_state.cars[car].y) + int(prev_state.cars[car].size)):
            new_map[int(prev_state.cars[car].x)][i] = "-"

        for car_copy in prev_state.cars:
            new_cars.append(Car(copy.deepcopy(car_copy.color), copy.deepcopy(car_copy.size), copy.deepcopy(car_copy.x),
                                copy.deepcopy(car_copy.y), copy.deepcopy(car_copy.direction)))

        for i in range(0, int(prev_state.cars[car].size)):
            new_map[int(prev_state.cars[car].x)][int(prev_state.cars[car].y) + i + move] = prev_state.cars[car].color[0]

        new_cars[car].y = str(int(new_cars[car].y) + move)
        new_state = Node(new_cars, prev_state, "RIGHT(" + prev_state.cars[car].color[:] + ", " + str(move) + ")", new_map)
        coded_map = new_state.code_name_of_node(new_map)
        if coded_map not in visited_nodes:
            visited_nodes.append(coded_map)
            return new_state
        else:
            return None

    else:
        return None


def UP(prev_state, car, move):                                                       # princip rovnaky ako pri LEFT()
    if can_move_n_steps(car, prev_state, move, "U"):
        new_map = copy.deepcopy(prev_state.mapa)
        new_cars = []

        for i in range(int(prev_state.cars[car].x), int(prev_state.cars[car].x) + int(prev_state.cars[car].size)):
            new_map[i][int(prev_state.cars[car].y)] = "-"

        for car_copy in prev_state.cars:
            new_cars.append(Car(copy.deepcopy(car_copy.color), copy.deepcopy(car_copy.size), copy.deepcopy(car_copy.x),
                                copy.deepcopy(car_copy.y), copy.deepcopy(car_copy.direction)))

        for i in range(0, int(prev_state.cars[car].size)):
            new_map[int(prev_state.cars[car].x) - 1 + i][int(prev_state.cars[car].y)] = prev_state.cars[car].color[0]

        new_cars[car].x = str(int(new_cars[car].x) - move)
        new_state = Node(new_cars, prev_state, "UP(" + prev_state.cars[car].color[:] + ", " + str(move) + ")", new_map)
        coded_map = new_state.code_name_of_node(new_map)
        if coded_map not in visited_nodes:
            visited_nodes.append(coded_map)
            return new_state
        else:
            return None

    else:
        return None


def DOWN(prev_state, car, move):                                                    # princip rovnaky ako pri LEFT()
    if can_move_n_steps(car, prev_state, move, "D"):
        new_map = copy.deepcopy(prev_state.mapa)
        new_cars = []

        for i in range(int(prev_state.cars[car].x), int(prev_state.cars[car].x) + int(prev_state.cars[car].size)):
            new_map[i][int(prev_state.cars[car].y)] = "-"

        for car_copy in prev_state.cars:
            new_cars.append(Car(copy.deepcopy(car_copy.color), copy.deepcopy(car_copy.size), copy.deepcopy(car_copy.x),
                                copy.deepcopy(car_copy.y), copy.deepcopy(car_copy.direction)))

        for i in range(0, int(prev_state.cars[car].size)):
            new_map[int(prev_state.cars[car].x) + i + move][int(prev_state.cars[car].y)] = prev_state.cars[car].color[0]

        new_cars[car].x = str(int(new_cars[car].x) + move)
        new_state = Node(new_cars, prev_state, "DOWN(" + prev_state.cars[car].color[:] + ", " + str(move) + ")", new_map)
        coded_map = new_state.code_name_of_node(new_map)

        if coded_map not in visited_nodes:
            visited_nodes.append(coded_map)
            return new_state
        else:
            return None

    else:
        return None


def new_node_generated(new_node, algorithm):                                # ukony pokial bol vytvoreny novy uzol
    if int(new_node.cars[0].y) + int(new_node.cars[0].size) == columns:     #ak sa dostalo cervene auto do ciela
        print("Red car in final destination, sequence of moves:")
        find_sequence_to_red_final_position(new_node)                       # vypise postupnost posunov aut
        return 1                                                            # cervene auto v cieli
    else:                                                                   # inak pokracujeme v algoritme
        if algorithm == "bfs":
            stack.appendleft(new_node)                                      # prida novy uzol na zaciatok stacku pre prehladanie do sirky
        else:
            stack.append(new_node)                                          # prida novy uzol na koniec stacku pre prehladanie do hlbky
    return 0


def search(algorithm, root):
    global rows
    print(algorithm + ": ")
    visited_nodes.clear()
    visited_nodes.append(root.code_name_of_node(root.mapa))
    while True:
        if len(stack) == 0:                                                 # ak sme vyprazdnili stack a nenasli sme cervene auto v cieli, riesenie neexistuje
            print("Neexistuje riesenie")
            return 0

        state = stack.pop()                                                 # vyberieme z konca stacku uzol na prehladanie
        for i in range(0, len(root.cars)):
            if state.cars[i].direction == "h":                              # pohyb vlavo alebo vpravo
                new_node = LEFT(state, i, 1)
                if new_node is not None:
                    if new_node_generated(new_node, algorithm):
                        return new_node

                new_node = RIGHT(state, i, 1)
                if new_node is not None:
                    if new_node_generated(new_node, algorithm):
                        return new_node

            elif state.cars[i].direction == "v":                            # pohyb hore alebo dole
                new_node = UP(state, i, 1)
                if new_node is not None:
                    if new_node_generated(new_node, algorithm):
                        return new_node

                new_node = DOWN(state, i, 1)
                if new_node is not None:
                    if new_node_generated(new_node, algorithm):
                        return new_node


def load_cars(file):
    array = []
    for line in file:
        line = line.split()
        array.append(Car(line[0], line[1], line[2], line[3], line[4]))

    return array


stack = collections.deque()
rows = 6
columns = 6
while True:
    print("Zadaj cislo suboru s krizovatkou - 1-13\nPre ukoncenie programu napis 'koniec'")
    n = input()
    if n == "koniec":
        exit()

    file = open(n + ".txt", "r")
    cars = load_cars(file)
    mapa = create_map(cars)

    visited_nodes = []
    root = Node(cars, None, None, mapa)
    stack.append(root)
    start = time.time()
    search("bfs", root)
    end = time.time()
    print("\nTime taken by BFS: ", end - start, "\n")
    stack.clear()
    stack.append(root)
    start = time.time()
    search("dfs", root)
    end = time.time()
    print("\nTime taken by DFS: ", end - start, "\n")
    stack.clear()
    file.close()