import math
import random
from itertools import combinations

ROWS = 10
COLUMNS = 10
MINE_COUNT = 10

BOARD = []
MINES = set()
EXTENDED = set()

MATRIX = [['?'] * COLUMNS for _ in range(ROWS)]


class Colors(object):
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'


def colorize(s, color):
    return '{}{}{}'.format(color, s, Colors.ENDC)


def get_index(i, j):
    if 0 > i or i >= ROWS or 0 > j or j >= COLUMNS:
        return None
    return i * COLUMNS + j


def create_board():
    squares = ROWS * COLUMNS

    # Create board
    for _ in range(squares):
        BOARD.append('[ ]')

    # Create mines
    while len(MINES) < MINE_COUNT:
        MINES.add(int(math.floor(random.random() * squares)))


def brute_force_solve():
    options = []
    for i in range(ROWS):
        for j in range(COLUMNS):
            if MATRIX[i][j] == '?':
                options.append((i, j))

    for r in range(1, len(options) + 1):
        for combination in combinations(options, r):
            # Create a copy of the board and mines
            board_copy = BOARD.copy()
            mines_copy = MINES.copy()
            extended_copy = EXTENDED.copy()
            matrix_copy = [row.copy() for row in MATRIX]

            # Update the board with the selected combination
            mine_hit = False
            for square in combination:
                if update_board(square):
                    mine_hit = True
                    break

            # Check if all mines have been found
            if not mine_hit and all(MATRIX[i][j] != '?' for i, j in options):
                # Print the solution
                print(draw_board())
                print('Solution found!')
                return

            # Reset the board and mines for the next combination
            BOARD[:] = board_copy
            MINES.clear()
            MINES.update(mines_copy)
            EXTENDED.clear()
            EXTENDED.update(extended_copy)
            for r in range(ROWS):
                MATRIX[r][:] = matrix_copy[r]

    print('No solution found.')


def draw_board():
    lines = []

    for j in range(ROWS):
        if j == 0:
            lines.append('   ' + ''.join(' {} '.format(x) for x in range(COLUMNS)))

        line = [' {} '.format(j)]
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
            return False
        BOARD[index] = colorize(' X ', Colors.RED)
        return True
    else:
        num_mines, squares = adjacent_squares(i, j)
        MATRIX[i][j] = num_mines
        if num_mines:
            if num_mines == 1:
                text = colorize(num_mines, Colors.BLUE)
            elif num_mines == 2:
                text = colorize(num_mines, Colors.GREEN)
            else:
                text = colorize(num_mines, Colors.RED)

            BOARD[index] = ' {} '.format(text)
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


def make_random_move():
    while True:
        i = random.randint(0, ROWS - 1)
        j = random.randint(0, COLUMNS - 1)
        if MATRIX[i][j] == '?':
            return (i, j)


if __name__ == '__main__':
    create_board()

    # Realizar un movimiento aleatorio inicial
    initial_square = make_random_move()
    update_board(initial_square)

    print('Movimiento inicial realizado en:', initial_square)
    print(draw_board())

    print('El jugador de fuerza bruta intentará resolver el tablero...')

    brute_force_solve()
