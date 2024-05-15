import math
import random
import itertools

ROWS = 10
COLUMNS = 10
MINE_COUNT = 10

BOARD = []
MINES = set()
EXTENDED = set()


MATRIX = [['?'] * COLUMNS for i in range(ROWS)]


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
    squares = ROWS * COLUMNS

    # Create board
    for _ in range(squares):
        BOARD.append('[ ]')

    # Create mines
    while len(MINES) < MINE_COUNT:
        MINES.add(random.randint(0, squares - 1))


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


def parse_selection(raw_selection):
    try:
        return [int(x.strip(','), 10) for x in raw_selection.split(' ')]
    except Exception:
        return None


def adjacent_squares(i, j):
    num_mines = 0
    squares_to_check = []
    for di in [-1, 0, 1]:
        for dj in [-1, 0, 1]:
            # Skip current square
            if di == dj == 0:
                continue

            coordinates = i + di, j + dj

            # Skip squares off the board
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

    # Check if we hit a mine, and if it was selected by the user or merely traversed
    if index in MINES:
        if not selected:
            return True
        BOARD[index] = colorize(' X ', Colors.RED)
        return True
    else:
        num_mines, squares = adjacent_squares(i, j)
        MATRIX[i][j] = num_mines
        if num_mines:
            # Use colorize function to color the number of mines
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

MINAS_MARCADAS = set()
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
                        print('Juego terminado')
                    else:
                        print('¡Ganaste!')
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
    casillas_desconocidas = []

    for i in range(ROWS):
        for j in range(COLUMNS):
            if MATRIX[i][j] == '?':
                casillas_desconocidas.append((i, j))
            else:
                casilla_completada = revisar_casilla_completada(i, j)
                if casilla_completada:
                    casillas_seguras.append(casilla_completada)

    if has_won():
        return casillas_seguras[0]
    detectar_minas()
    for tamano_combinacion in range(1, len(casillas_desconocidas) + 1):
        for combinacion in itertools.combinations(casillas_desconocidas, tamano_combinacion):
            for casilla in combinacion:
                if get_index(*casilla) not in MINAS_MARCADAS:
                    return casilla

    return jugador_aleatorio()





def jugador_aleatorio():
    available_squares = [(i, j) for i in range(ROWS) for j in range(COLUMNS) if MATRIX[i][j] == '?']
    return random.choice(available_squares)

if __name__ == '__main__':
    create_board()
    print(draw_board())

    # Realizar un movimiento aleatorio al principio
    i, j = jugador_aleatorio()
    juego_terminado = update_board((i, j))

    if juego_terminado:
        ()
        print("Juego terminado!")
    else:
        while not has_won():
            movimiento = solver_fuerza_bruta()
            if movimiento is None:
                print("No quedan movimientos.")
                break

            i, j = movimiento
            juego_terminado = update_board((i, j))

            if juego_terminado:
                reveal_mines()
                print("Juego terminado!")
                break

    print(draw_board())
