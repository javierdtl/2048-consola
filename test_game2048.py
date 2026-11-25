# -*- coding: utf-8 -*-
"""
Tests for game2048.py. Run them with:  python -m pytest
"""

from game2048 import Game2048, generate_board


def test_merge_row_left():
    game = Game2048([[2, 2, 2, 2],
                     [2, 0, 2, 4],
                     [0, 0, 0, 0],
                     [4, 4, 8, 8]])
    assert game.left()
    assert game.board == [[4, 4, 0, 0],
                          [4, 4, 0, 0],
                          [0, 0, 0, 0],
                          [8, 16, 0, 0]]
    assert game.score() == 4 + 4 + 4 + 8 + 16


def test_merge_column_down():
    game = Game2048([[2, 0, 0, 0],
                     [2, 0, 0, 0],
                     [4, 0, 0, 0],
                     [0, 0, 0, 0]])
    assert game.down()
    assert [row[0] for row in game.board] == [0, 0, 4, 4]
    assert game.score() == 4


def test_cell_is_not_summed_twice():
    game = Game2048([[4, 2, 2, 0],
                     [0, 0, 0, 0],
                     [0, 0, 0, 0],
                     [0, 0, 0, 0]])
    game.left()
    assert game.board[0] == [4, 4, 0, 0]


def test_move_that_changes_nothing_returns_false():
    # This was the bug in the original down() and left().
    board = [[2, 4, 0, 0],
             [8, 2, 0, 0],
             [4, 8, 0, 0],
             [2, 4, 0, 0]]
    game = Game2048([row[:] for row in board])
    assert not game.left()
    assert not game.up()
    assert not game.down()
    assert game.board == board
    assert game.right()


def test_is_blocked():
    full = [[2, 4, 2, 4],
            [4, 2, 4, 2],
            [2, 4, 2, 4],
            [4, 2, 4, 2]]
    assert Game2048([row[:] for row in full]).is_blocked()

    # Empty bottom-right corner: the original version said "blocked" here.
    corner = [row[:] for row in full]
    corner[3][3] = 0
    assert not Game2048(corner).is_blocked()

    # Two equal cells in the last column.
    last_col = [row[:] for row in full]
    last_col[3][3] = 4
    assert not Game2048(last_col).is_blocked()


def test_new_cell_and_full_board():
    game = Game2048(generate_board(4))
    assert sum(v != 0 for row in game.board for v in row) == 2
    for _ in range(14):
        assert game.add_new_cell()
    assert all(v in (2, 4) for row in game.board for v in row)
    assert not game.add_new_cell()


def test_other_sizes():
    game = Game2048([[2, 2, 0, 0, 0],
                     [0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0]])
    assert game.right()
    assert game.board[0] == [0, 0, 0, 0, 4]
    assert game.max_cell() == 4
