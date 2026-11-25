# -*- coding: utf-8 -*-
"""
2048 for the console.

Original version: May 2017, university assignment (Practica 4).
Revised: November 2026.

@author: javierdtl
"""

import random

WINNING_VALUE = 2048


class Game2048(object):
    """
    Game2048 contains all the functions needed to play the 2048 game. It
    allows the player to make every move allowed in the game and to check the
    total score and the maximum value in a cell at any time. It also lets you
    change the value of a given cell and play on a board of any size.
    """
    def __init__(self, matrix):
        self.board = matrix
        self.total = 0
        self.maximum = maximum_value(self.board)

    def __str__(self):
        res = ""
        size = self.get_size()
        for row in range(size):
            for col in range(size):
                value = self.get_value(row, col)
                res += "{0:>6}".format(value if value != 0 else ".")
            res += "\n"
        res += "Max: {0}   Score: {1}".format(self.max_cell(), self.score())
        return res

    def _merge_line(self, line):
        """
        Moves the non-zero values of a line (a row or a column, already in
        the direction of the move) to the front and adds equal neighbours.
        A cell that is the result of a sum is not summed again in the same
        move. Returns the new line and the points earned.
        -----
        Example: [2, 2, 2, 0] -> [4, 2, 0, 0], 4 points.
        """
        values = [v for v in line if v != 0]
        merged = []
        points = 0
        i = 0
        while i < len(values):
            if i + 1 < len(values) and values[i] == values[i + 1]:
                merged.append(2 * values[i])
                points += 2 * values[i]
                i += 2
            else:
                merged.append(values[i])
                i += 1
        merged += [0] * (len(line) - len(merged))
        return merged, points

    def _move(self, lines):
        """
        Applies a move. 'lines' is a list with the coordinates of every row
        or column, ordered in the direction the cells move to.
        Returns True if the board changed and False otherwise.
        """
        changed = False
        for coords in lines:
            old = [self.board[r][c] for r, c in coords]
            new, points = self._merge_line(old)
            if new != old:
                changed = True
                self.total += points
                for (r, c), value in zip(coords, new):
                    self.board[r][c] = value
        self.maximum = maximum_value(self.board)
        return changed

    def up(self):
        """
        Moves every non-zero cell upwards. If two equal cells meet, they are
        added and the result stays in the upper one. A cell is never summed
        twice in the same move, but several sums can happen at once.
        The score increases by the value of every sum.
        Returns True if the board changed.
        """
        n = self.get_size()
        return self._move([[(r, c) for r in range(n)] for c in range(n)])

    def down(self):
        """
        Same as up(), but the cells move downwards.
        Returns True if the board changed.
        """
        n = self.get_size()
        return self._move([[(r, c) for r in range(n - 1, -1, -1)]
                           for c in range(n)])

    def left(self):
        """
        Same as up(), but the cells move to the left.
        Returns True if the board changed.
        """
        n = self.get_size()
        return self._move([[(r, c) for c in range(n)] for r in range(n)])

    def right(self):
        """
        Same as up(), but the cells move to the right.
        Returns True if the board changed.
        """
        n = self.get_size()
        return self._move([[(r, c) for c in range(n - 1, -1, -1)]
                           for r in range(n)])

    def add_new_cell(self):
        """
        After a move, a new number appears in a random empty cell. It is a 2
        75% of the time and a 4 the other 25%.
        Returns False if there was no empty cell.
        """
        empty = []
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if self.board[i][j] == 0:
                    empty.append((i, j))
        if not empty:
            return False
        row, col = random.choice(empty)
        self.board[row][col] = random.choice([2, 2, 2, 4])
        self.maximum = maximum_value(self.board)
        return True

    def get_value(self, row, col):
        """
        Returns the value of the cell at (row, col).
        """
        return self.board[row][col]

    def put_value(self, row, col, value):
        """
        Puts the given value in the cell at (row, col) and updates the
        maximum value of the board.
        """
        self.board[row][col] = value
        self.maximum = maximum_value(self.board)

    def get_size(self):
        """
        Returns the size of the board. A 4 means the board is 4x4.
        """
        return len(self.board)

    def is_blocked(self):
        """
        Tells whether the game is over. The board is blocked when there are
        no empty cells and no two adjacent cells have the same value.
        """
        n = self.get_size()
        for i in range(n):
            for j in range(n):
                value = self.board[i][j]
                if value == 0:
                    return False
                if j + 1 < n and value == self.board[i][j + 1]:
                    return False
                if i + 1 < n and value == self.board[i + 1][j]:
                    return False
        return True

    def max_cell(self):
        """
        Returns the maximum value on the board.
        """
        self.maximum = maximum_value(self.board)
        return self.maximum

    def score(self):
        """
        Returns the current score. At the start of the game it is 0.
        """
        return self.total


def maximum_value(matrix):
    """
    Auxiliary function that returns the biggest value on the board.
    """
    return max(max(row) for row in matrix)


def generate_board(order):
    """
    Creates a new order x order board full of zeros, with a 2 in two random
    cells, ready to start a game.
    """
    gameboard = [[0 for x in range(order)] for y in range(order)]
    cells = [(i, j) for i in range(order) for j in range(order)]
    for row, col in random.sample(cells, min(2, len(cells))):
        gameboard[row][col] = 2
    return gameboard


# Console game

MOVES = {
    "w": "up",
    "a": "left",
    "s": "down",
    "d": "right",
}


def play(size=4):
    """
    Plays a game of 2048 in the console. Use w/a/s/d to move and q to quit.
    """
    game = Game2048(generate_board(size))
    already_won = False
    print("2048. Move with w (up), a (left), s (down), d (right). q quits.\n")
    while True:
        print(game)
        if game.is_blocked():
            print("\nNo moves left. Game over.")
            break
        key = input("\nMove: ").strip().lower()
        if key == "q":
            print("Bye.")
            break
        if key not in MOVES:
            print("Use w, a, s, d or q.")
            continue
        moved = getattr(game, MOVES[key])()
        if not moved:
            print("That move doesn't change the board, try another one.")
            continue
        game.add_new_cell()
        if game.max_cell() >= WINNING_VALUE and not already_won:
            already_won = True
            print("\nYou reached {0}! You can keep playing.".format(WINNING_VALUE))
        print()
    return game.score()


if __name__ == "__main__":
    import sys
    board_size = 4
    if len(sys.argv) > 1:
        board_size = int(sys.argv[1])
    play(board_size)
