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
def check_completed_square(i, j):
    num_mines = MATRIX[i][j]
    num, adjacent_squares_list = adjacent_squares(i, j)
    flagged_adjacent_squares = [(x, y) for x, y in adjacent_squares_list if get_index(x, y) in MINAS_MARCADAS]
    not_flagged_adjacent_squares = [(x, y) for x, y in adjacent_squares_list if get_index(x, y) not in MINAS_MARCADAS]
    if len(flagged_adjacent_squares) == num_mines:
        for limp_square in not_flagged_adjacent_squares:
            x, y = limp_square
            if MATRIX[x][y] == "?":
                mine_hit = update_board(limp_square)
                if mine_hit or has_won():
                    if mine_hit:
                        reveal_mines()
                        print('Game over')
                    else:
                        print('You won!')
                    return limp_square
    return not_flagged_adjacent_squares[0]



def detect_mines():
    options = []
    for i in range(ROWS):
        for j in range(COLUMNS):
            if MATRIX[i][j] == '?':
                options.append((i, j))
    for square in options:
        i, j = square
        num_mines, adjacent_squares_list = adjacent_squares(i, j)
        revealed_adjacent_squares = [(x, y) for x, y in adjacent_squares_list if MATRIX[x][y] != '?']
        for adj_square in revealed_adjacent_squares:
            adj_i, adj_j = adj_square
            adj_num_mines, adj_adjacent_squares_list = adjacent_squares(adj_i, adj_j)
            unknown_adjacent_squares = [(x, y) for x, y in adj_adjacent_squares_list if MATRIX[x][y] == '?']
            if len(unknown_adjacent_squares) == adj_num_mines and len(unknown_adjacent_squares) > 0 and get_index(
                    *square) not in MINAS_MARCADAS:
                MINAS_MARCADAS.add(get_index(*square))


def solver_fuerza_bruta():
    detect_mines()

    safe_squares = []
    unknown_squares = []

    for i in range(ROWS):
        for j in range(COLUMNS):
            if MATRIX[i][j] == '?':
                unknown_squares.append((i, j))
            else:
                completed_square = check_completed_square(i, j)
                if completed_square:
                    safe_squares.append(completed_square)

    if has_won():
        return safe_squares[0]
    detect_mines()
    for combination_size in range(1, len(unknown_squares) + 1):
        for combination in itertools.combinations(unknown_squares, combination_size):
            for square in combination:
                if get_index(*square) not in MINAS_MARCADAS:
                    return square

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
