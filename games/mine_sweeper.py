from collections import deque
import numpy as np
from time import sleep
import sys
sys.path.append('../myutil')
from input_filtered import int_input, true_or_false_input


class Board(object):
    def __init__(self, shape, mine_rate):
        """
        Initialize Board.

        Parameters
        ----------
        shape : tuple or list
            Board shape, like (height, width).
        mine_rate : float
            Rate of number of mines to number of board cells.

        """
        self.h, self.w = shape
        self.mine_rate = mine_rate
        self.n = self.h * self.w
        self._create_mine_board()
        self._create_number_board()
        self._create_mask_board()

    def _create_mine_board(self):
        self._mine_board = np.zeros((self.h, self.w), dtype=np.int)
        all_pos = np.random.permutation(self.n)
        mine_pos = all_pos[:int(self.n * self.mine_rate)]
        mine_x = mine_pos % self.w
        mine_y = mine_pos // self.w
        self._mine_board[mine_y, mine_x] = 1

    def _around(self, x, y):
        left = max(x - 1, 0)
        top = max(y - 1, 0)
        right = min(x + 2, self.w)
        bottom = min(y + 2, self.h)
        return self._mine_board[top:bottom, left:right]

    def _count_mine_around(self, x, y):
        count = np.sum(self._around(x, y))
        return count

    def _create_number_board(self):
        self._number_board = np.zeros_like(self._mine_board, dtype=np.int)
        for y in range(self.h):
            for x in range(self.w):
                if self._mine_board[y, x] == 0:
                    self._number_board[y, x] = self._count_mine_around(x, y)
                else:
                    self._number_board[y, x] = -1

    def _create_mask_board(self):
        self._mask_board = np.ones_like(self._mine_board, dtype=np.int)

    def show(self, show_index=True):
        """
        Show current Board.

        Parameters
        ----------
        show_index : bool
            If True, print index around board.

        """
        end_pad = ''
        if show_index:
            n_digit_x = int(np.log10(self.w - 1) + 1) if show_index else 0
            n_digit_y = int(np.log10(self.h - 1) + 1) if show_index else 0
            end_pad = ' ' * max(0, (n_digit_x - 2)) if show_index else 0
            print(' ' * (n_digit_y) +
                  ''.join(["{:{}d}".format(x, max(2, n_digit_x))
                           for x in range(self.w)]))
        for y in range(self.h):
            if show_index:
                print("{:{}d}".format(y, n_digit_y), end='')
            for x in range(self.w):
                if self._mask_board[y, x] == 1:
                    print('■', end=end_pad)
                elif self._mask_board[y, x] == -1:
                    print('Ｆ', end=end_pad)
                elif self._mine_board[y, x] == 1:
                    print('＊', end=end_pad)
                else:
                    print("{:2d}".format(self._number_board[y, x]),
                          end=end_pad)
            print()

    def sweep(self, x, y):
        """
        Sweep mine.

        If mine doesn't exists around sweep point, sweep all around.

        Parameters
        ----------
        x : int
            X-Coodinate.
        y : int
            Y-Coodinate

        Returns
        -------
        isMine : bool
            If mine exists in (x, y) return True, otherwise False.

        """
        if self._mask_board[y, x] == -1:  # If flag stand
            return True

        if self._mine_board[y, x] == 1:  # If mine exists here
            self._mask_board[y, x] = 0
            return False

        if self._number_board[y, x] != 0:  # If mine exists arouund
            self._mask_board[y, x] = 0
            return True

        # BFS
        sweepqueue = deque()
        sweepqueue.append((x, y))

        while True:
            if len(sweepqueue) == 0:
                return True
            x, y = sweepqueue.popleft()

            if self._mask_board[y, x] != 1:
                continue

            self._mask_board[y, x] = 0

            if self._number_board[y, x] == 0:  # If mine doesn't exist around
                left = max(x - 1, 0)
                top = max(y - 1, 0)
                right = min(x + 2, self.w)
                bottom = min(y + 2, self.h)
                print(x, y)
                print("l: {} t: {} r: {} b: {}".format(left, top,
                                                       right, bottom))
                print()
                sweepqueue += [(x, y)
                               for y in range(top, bottom)
                               for x in range(left, right)
                               if (x, y) not in sweepqueue and
                               self._mask_board[y, x] == 1]

    def put_flag(self, x, y):
        """
        Put flag on (x, y).

        Parameters
        ----------
        x : int
            X-Coodinate
        y : int
            Y-Coodinate

        Returns
        -------
        couldPutFlag : bool
            If could put return True, otherwise False

        """
        if x < 0 or x >= self.w or y < 0 or y >= self.h:
            return False
        self._mask_board[y, x] *= -1
        return True

    def isClear(self):
        """
        Judge clear.

        Returns
        -------
        isClear : bool
            If it's clear return True, otherwise False.

        """
        if np.sum(np.abs(self._mask_board + self._mine_board)) == 0:
            return True
        return False

    def all_open(self):
        """Remove each masks on board."""
        self._mask_board = np.zeros_like(self._mask_board, dtype=np.int)


if __name__ == '__main__':
    shape = (10, 10)
    mine_rate = 0.1

    board = Board(shape, mine_rate)
    board.show()

    # main loop
    x, y = int_input(min_val=0, max_val=10, nargs=2, description=">")
    while board.sweep(x, y):
        board.show()
        if true_or_false_input('f', 'o', description="Open(o) or Flag(f)>"):
            x, y = int_input(min_val=0, max_val=10, nargs=2, description=">")
            board.put_flag(x, y)
        else:
            x, y = int_input(min_val=0, max_val=10, nargs=2, description=">")
        if board.isClear():
            break

    board.show()
    sleep(1)

    if board.isClear():
        print('Congratulations!')
    else:
        print('Failed to sweep mine...')
        print('Boooooomb!!')

    board.all_open()
    board.show()
