import numpy as np
from time import sleep
import random


isPlay = 1  # player vs player: 1 cpu vs cpu: 2


def init_board():
    board = np.zeros((8, 8))
    board[3, 3] = board[4, 4] = 1
    board[3, 4] = board[4, 3] = -1
    return board


board = init_board()

dirs = [[i, j]
        for i in range(-1, 2)
        for j in range(-1, 2) if i != 0 or j != 0]


def show_board():
    """Print Board."""
    print('  ' + ' '.join([str(i) for i in range(8)]))
    print(" " + "-" * (9 * 2 - 1))
    for idx, line in enumerate(board):
        print(idx, end='|')
        for cell in line:
            if cell == 0:
                print(' ', end='|')
            elif cell == 1:
                print('o', end='|')
            else:
                print('x', end='|')
        print()
        print(" " + "-" * (9 * 2 - 1))


def show_help_board(can_put_list):
    """
    Print Board with help mark(*).

    * is putable cell.

    Parameters
    ----------
    can_put_list : list
        Includes putable cell coordinates like [[1, 2], [3, 4], ..., [x, y]]

    """
    print('HELP BOARD(* is putable cell)')
    print('  ' + ' '.join([str(x) for x in range(8)]))
    print(" " + "-" * (9 * 2 - 1))
    for y in range(8):
        print(y, end='|')
        for x in range(8):
            if [x, y] in can_put_list:
                print('*', end='|')
            elif board[y][x] == 0:
                print(' ', end='|')
            elif board[y][x] == 1:
                print('o', end='|')
            else:
                print('x', end='|')
        print()
        print(" " + "-" * (9 * 2 - 1))


def can_put(x, y, turn):
    """
    Return if Board[y][x] is putable cell.

    Parameters
    ----------
    x : int
        X coordinate
    y: int
        Y coordinate
    turn: int
        1 or -1

    Returns
    -------
    can_put : bool
        True if board[y][x] is putable cell, else False

    """
    if out_of_board(x, y):
        return False
    if board[y][x] != 0:
        return False
    for dirX, dirY in dirs:
        if can_put_dir(x, y, dirX, dirY, turn):
            return True
    return False


def out_of_board(x, y):
    """
    Return if X and Y coordinates is out of board.

    Parameters
    ----------
    x : int
        X coordinate
    y : int
        Y coordinate

    Returns
    -------
    out_of_board : bool
        If Coordinates is out of board

    """
    if x < 0 or x >= len(board[0]) or y < 0 or y >= len(board):
        return True
    else:
        return False


def can_put_dir(x, y, dirX, dirY, turn):
    """
    Return can reverese (dirX, dirY) direction from (x, y).

    Parameters
    ----------
    x : int
        X coordinate
    y : int
        Y coordinate
    dirX : int
        -1 or 0 or 1
    dirY : int
        -1 or 0 or 1
    turn : int
        -1 or 1

    Returns
    -------
    can_put_dir : bool
        Can reverese (dirX, dirY) direction from (x, y)

    """
    x += dirX
    y += dirY
    if out_of_board(x, y):
        return False
    if board[y][x] != -turn:
        return False

    x += dirX
    y += dirY
    while not out_of_board(x, y):
        if board[y][x] == 0:
            return False
        if board[y][x] == turn:
            return True
        x += dirX
        y += dirY
    return False


def create_can_put_list(turn):
    """
    Create putable cells list.

    Parameters
    ----------
    turn : int
        -1 or 1

    Returns
    -------
    can_put_list : list
        Putable cells list like [[1, 2], [3, 4], ..., [x, y]]

    """
    can_put_list = [[x, y]
                    for x in range(8)
                    for y in range(8)
                    if can_put(x, y, turn)]
    return can_put_list


def put(x, y, turn):
    """
    Put o or x on board[y][x] forcibly.

    Parameters
    ----------
    x : int
        X coordinate
    y : int
        Y coordinate
    turn : int
        -1 or 1

    """
    board[y, x] = turn


def reverse(x, y, turn):
    """
    Reverse [o to x] or [x to o].

    Parameters
    ----------
    x : int
        X coordinate of put-cell
    y : int
        Y coordinate of put-cell
    turn : int
        -1 or 1

    """
    for dirX, dirY in dirs:
        if can_put_dir(x, y, dirX, dirY, turn):
            put_x = x + dirX
            put_y = y + dirY
            while board[put_y][put_x] != turn:
                put(put_x, put_y, turn)
                put_x += dirX
                put_y += dirY


def ox_count():
    """
    Count o and x on board.

    Returns
    -------
    ox_count : taple
        (number of o, number of x)

    """
    count_o = np.sum(board == 1)
    count_x = np.sum(board == -1)
    return count_o, count_x


is_pre_pass = True  # Was the opponent passed on the last turn
turn = np.random.choice([-1, 1])
print('You are o')
print('First turn is {}'.format('o' if turn == 1 else 'x'))
show_board()

# Main loop
while True:
    # Search putable cells
    can_put_list = create_can_put_list(turn)
    if len(can_put_list) == 0:  # no putable cell
        print('pass')
        turn *= -1
        if not is_pre_pass:
            break
        is_pre_pass = True
        continue
    else:
        is_pre_pass = False

    if turn == isPlay:  # player turn
        try:
            inputs = input('"x y" or help or quit>')
            if inputs.lower() == "help":
                show_help_board(can_put_list)
                continue
            if inputs.lower() == 'quit':
                break
            x, y = [int(c) for c in inputs.split()]
        except ValueError:
            continue
        if [x, y] not in can_put_list:
            continue
        put(x, y, turn)

    else:  # CPU turn
        sleep(1)
        x, y = random.choice(can_put_list)
        put(x, y, turn)

    # Reverse
    reverse(x, y, turn)
    # Change turn
    turn *= -1

    print()
    show_board()
    print('o: {} x: {}'.format(*ox_count()))

# Winning / losing judgment
co, cx = ox_count()
print('o: {} x: {}'.format(co, cx))
if co > cx:
    print('Winner!!')
elif co == cx:
    print('Draw')
else:
    print('Loser...')
