import math
import random

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

    if index in MINES:
        if selected:
            BOARD[index] = colorize(' X ', Colors.RED)
            return True  # Indicate that a mine was hit
        return False  # Do nothing if it's traversed non-selected

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
    else:
        BOARD[index] = '   '
        for asquare in squares:
            aindex = get_index(*asquare)
            if aindex in EXTENDED:
                continue
            result = update_board(asquare, False)
            if result:  # If a mine is hit during traversal, propagate the hit
                return True
    return False


def reveal_mines():
    for index in MINES:
        if index in EXTENDED:
            continue
        BOARD[index] = colorize(' X ', Colors.YELLOW)


def has_won():
    return len(EXTENDED | MINES) == len(BOARD)

def check_completed_square(i, j):
    num_mines, squares = adjacent_squares(i, j)
    flagged_mines = sum(1 for sq in squares if MATRIX[sq[0]][sq[1]] == 'F')

    if flagged_mines == num_mines:
        for sq in squares:
            if MATRIX[sq[0]][sq[1]] == '?':
                hit_mine = update_board(sq, True)
                if hit_mine:
                    return sq
                if has_won():
                    return sq
    return None


def detect_mines():
    for i in range(ROWS):
        for j in range(COLUMNS):
            if MATRIX[i][j] != '?':
                continue
            
            num_mines, squares = adjacent_squares(i, j)
            covered_squares = [sq for sq in squares if MATRIX[sq[0]][sq[1]] == '?']
            
            if len(covered_squares) == num_mines:
                for sq in covered_squares:
                    MATRIX[sq[0]][sq[1]] = 'F'

def information_gained_algorithm():
    info_gain = []
    for i in range(ROWS):
        for j in range(COLUMNS):
            if MATRIX[i][j] != '?':
                continue
            
            num_mines, squares = adjacent_squares(i, j)
            info_gain.append((len(squares), (i, j)))
    
    info_gain.sort(reverse=True)
    return info_gain


def find_play(sorted_information_gain, squ):
    for _, (i, j) in sorted_information_gain:
        if MATRIX[i][j] == '?' and (i, j) not in squ:
            return (i, j)
    return None

def heuristic_player_directed():
    detect_mines()
    
    while True:
        for i in range(ROWS):
            for j in range(COLUMNS):
                if MATRIX[i][j] != '?' and MATRIX[i][j] != 'F':
                    continue
                
                result = check_completed_square(i, j)
                if result:
                    if has_won():
                        print(draw_board())
                        print("You won!")
                        return result
                    continue

        info_gain = information_gained_algorithm()
        play = find_play(info_gain, EXTENDED)
        
        if play:
            hit_mine = update_board(play, True)
            if hit_mine:
                reveal_mines()
                print(draw_board())
                print("Game Over!")
                return play
            if has_won():
                print(draw_board())
                print("You won!")
                return play
        else:
            break
        
    # If no moves are found by heuristics, choose a random move
    while True:
        i, j = random.randint(0, ROWS - 1), random.randint(0, COLUMNS - 1)
        if MATRIX[i][j] == '?':
            hit_mine = update_board((i, j), True)
            if hit_mine:
                reveal_mines()
                print(draw_board())
                print("Game Over!")
                return (i, j)
            if has_won():
                print(draw_board())
                print("You won!")
                return (i, j)



if __name__ == '__main__':
    create_board()
    print(draw_board())
    while not has_won():
        move = heuristic_player_directed()
        if move:
            if BOARD[get_index(*move)] == colorize(' X ', Colors.RED):
                print("Game Over!")
                break
            if has_won():
                print("You won!")
                break
        print(draw_board())


