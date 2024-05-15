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


class Colors(object):
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'


def colorize(s, color):
    return '{}{}{}'.format(color, s, Colors.ENDC)


def get_index(i, j):
    if 0 > i or i >= COLUMNS or 0 > j or j >= ROWS:
        return None
    return i * ROWS + j


def create_board():
    squares = ROWS * COLUMNS

    # Create board
    for _ in range(squares):
        BOARD.append('[ ]')

    # Create mines
    while True:
        if len(MINES) >= MINE_COUNT:
            break
        MINES.add(int(math.floor(random.random() * squares)))


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
            return
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
            return
        else:
            BOARD[index] = '   '

            for asquare in squares:
                aindex = get_index(*asquare)
                if aindex in EXTENDED:
                    continue
                EXTENDED.add(aindex)
                update_board(asquare, False)


def reveal_mines():
    for index in MINES:
        if index in EXTENDED:
            continue
        BOARD[index] = colorize(' X ', Colors.YELLOW)


def has_won():
    return len(EXTENDED | MINES) == len(BOARD)

def brute_force_solver():
    squares = [(i, j) for i in range(COLUMNS) for j in range(ROWS)]
    non_mine_squares = [square for square in squares if get_index(*square) not in MINES]
    
    def is_safe_move(board_state, move):
        return get_index(*move) not in MINES
    
    def backtrack(board_state, moves):
        if len(moves) == len(non_mine_squares):
            return True
        
        for square in non_mine_squares:
            if square in moves:
                continue
            
            if is_safe_move(board_state, square):
                moves.append(square)
                if update_board(square, selected=True) is not True:
                    if backtrack(board_state, moves):
                        return True
                    moves.pop()
                else:
                    moves.pop()
                    return False

        return False

    initial_board_state = list(BOARD)
    moves = []
    if backtrack(initial_board_state, moves):
        print("Game Solved")
        print(draw_board())
    else:
        print("No Solution Found")

if __name__ == '__main__':
    create_board()
    print(draw_board())
    brute_force_solver()