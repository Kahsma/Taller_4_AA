import math
import random
import itertools
import time
import csv

ROWS = 10
COLUMNS = 10
MINE_COUNT = 10

class Colors:
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'

def colorize(s, color):
    return f"{color}{s}{Colors.ENDC}"

def get_index(i, j):
    if 0 <= i < ROWS and 0 <= j < COLUMNS:
        return i * COLUMNS + j
    return None

def create_board():
    global BOARD, MINES, EXTENDED, MATRIX, MINAS_MARCADAS
    BOARD = []
    MINES = set()
    EXTENDED = set()
    MINAS_MARCADAS = set()
    MATRIX = [['?'] * COLUMNS for _ in range(ROWS)]
    
    squares = ROWS * COLUMNS
    for _ in range(squares):
        BOARD.append('[ ]')
    while len(MINES) < MINE_COUNT:
        MINES.add(int(math.floor(random.random() * squares)))

def draw_board():
    lines = []
    for j in range(ROWS):
        if j == 0:
            lines.append('   ' + ''.join(f' {x} ' for x in range(COLUMNS)))
        line = [f' {j} ']
        for i in range(COLUMNS):
            line.append(BOARD[get_index(i, j)])
        lines.append(''.join(line))
    return '\n'.join(reversed(lines))

def adjacent_squares(i, j):
    num_mines = 0
    squares_to_check = []
    for di in [-1, 0, 1]:
        for dj in [-1, 0, 1]:
            if di == dj == 0:
                continue
            coordinates = i + di, j + dj
            proposed_index = get_index(*coordinates)
            if proposed_index is None:
                continue
            if proposed_index in MINES:
                num_mines += 1
            squares_to_check.append(coordinates)
    return num_mines, squares_to_check

def update_board(square, selected=True):
    i, j = square
    index = get_index(i, j)
    EXTENDED.add(index)
    if index in MINES:
        if not selected:
            return True
        BOARD[index] = colorize(' X ', Colors.RED)
        return True
    else:
        num_mines, squares = adjacent_squares(i, j)
        MATRIX[i][j] = num_mines
        if num_mines:
            BOARD[index] = colorize(f' {num_mines} ', Colors.GREEN if num_mines == 1 else Colors.YELLOW if num_mines == 2 else Colors.RED)
            return False
        else:
            BOARD[index] = '   '
            for asquare in squares:
                aindex = get_index(*asquare)
                if aindex in EXTENDED:
                    continue
                EXTENDED.add(aindex)
                update_board(asquare, False)
            return False

def reveal_mines():
    for index in MINES:
        if index in EXTENDED:
            continue
        BOARD[index] = colorize(' X ', Colors.YELLOW)

def has_won():
    return len(EXTENDED | MINES) == len(BOARD)

def revisar_casilla_completada(i, j):
    num_minas = MATRIX[i][j]
    num, casillas_adyacentes = adjacent_squares(i, j)
    casillas_adyacentes_marcadas = [(x, y) for x, y in casillas_adyacentes if get_index(x, y) in MINAS_MARCADAS]
    casillas_adyacentes_no_marcadas = [(x, y) for x, y in casillas_adyacentes if get_index(x, y) not in MINAS_MARCADAS]
    
    if len(casillas_adyacentes_marcadas) == num_minas:
        for casilla_vacia in casillas_adyacentes_no_marcadas:
            x, y = casilla_vacia
            if MATRIX[x][y] == "?":
                mina_encontrada = update_board(casilla_vacia)
                if mina_encontrada or has_won():
                    if mina_encontrada:
                        reveal_mines()
                    return casilla_vacia
    return casillas_adyacentes_no_marcadas[0]

def detectar_minas():
    opciones = [(i, j) for i in range(ROWS) for j in range(COLUMNS) if MATRIX[i][j] == '?']
    for casilla in opciones:
        i, j = casilla
        num_minas, casillas_adyacentes = adjacent_squares(i, j)
        casillas_reveladas = [(x, y) for x, y in casillas_adyacentes if MATRIX[x][y] != '?']
        for casilla_adyacente in casillas_reveladas:
            adj_i, adj_j = casilla_adyacente
            num_minas_adyacentes, casillas_adyacentes_adyacentes = adjacent_squares(adj_i, adj_j)
            casillas_desconocidas = [(x, y) for x, y in casillas_adyacentes_adyacentes if MATRIX[x][y] == '?']
            if len(casillas_desconocidas) == num_minas_adyacentes and len(casillas_desconocidas) > 0 and get_index(*casilla) not in MINAS_MARCADAS:
                MINAS_MARCADAS.add(get_index(*casilla))

def solver_fuerza_bruta():
    detectar_minas()
    casillas_seguras = []
    casillas_pendientes = []
    for i in range(ROWS):
        for j in range(COLUMNS):
            if MATRIX[i][j] == '?':
                casillas_pendientes.append((i, j))
            else:
                casilla_completada = revisar_casilla_completada(i, j)
                if casilla_completada:
                    casillas_seguras.append(casilla_completada)
    if has_won():
        return casillas_seguras[0]
    detectar_minas()
    for tamano_combinacion in range(1, len(casillas_pendientes) + 1):
        for combinacion in itertools.combinations(casillas_pendientes, tamano_combinacion):
            combinacion_valida = True
            for casilla in combinacion:
                if get_index(*casilla) in MINAS_MARCADAS:
                    combinacion_valida = False
                    break
            if combinacion_valida:
                return combinacion[0]
    return jugador_aleatorio()

def jugador_aleatorio():
    available_squares = [(i, j) for i in range(ROWS) for j in range(COLUMNS) if MATRIX[i][j] == '?']
    return random.choice(available_squares)

def ejecutar_simulacion():
    create_board()
    i, j = jugador_aleatorio()
    juego_terminado = update_board((i, j))
    if juego_terminado:
        return False, time.time()
    while not has_won():
        movimiento = solver_fuerza_bruta()
        if movimiento is None:
            break
        i, j = movimiento
        juego_terminado = update_board((i, j))
        if juego_terminado:
            reveal_mines()
            return False, time.time()
    return has_won(), time.time()

def main():
    resultados = []
    for _ in range(100):
        inicio = time.time()
        ganado, fin = ejecutar_simulacion()
        duracion = fin - inicio
        resultados.append((ganado, duracion))
    with open('resultados_simulacion_fb.csv', 'w', newline='') as archivo_csv:
        escritor_csv = csv.writer(archivo_csv)
        escritor_csv.writerow(['Ganado', 'Duracion'])
        escritor_csv.writerows(resultados)

if __name__ == '__main__':
    main()
