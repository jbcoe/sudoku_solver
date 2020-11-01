from sudoku import transformer
import nose.tools
from textwrap import dedent
from sudoku import (
    Sudoku,
    switch_rows,
    switch_columns,
    switch_column_blocks,
    switch_row_blocks,
    switch_numbers,
)

import numpy as np


def test_switch_numbers():
    s = Sudoku(Sudoku.COMPLETED_GRID)
    ones = []
    sevens = []
    for row in range(9):
        for column in range(9):
            if s[row, column] == 1:
                ones.append((row, column))
            elif s[row, column] == 7:
                sevens.append((row, column))

    new_s = transformer.switch_numbers(s, 1, 7)
    nose.tools.ok_(s != new_s)

    for row, column in sevens:
        nose.tools.eq_(new_s[row, column], 1)

    for row, column in ones:
        nose.tools.eq_(new_s[row, column], 7)

    nose.tools.ok_(True)


def test_switch_numbers_inplace():
    s = Sudoku(Sudoku.COMPLETED_GRID)
    ones = []
    sevens = []
    for row in range(9):
        for column in range(9):
            if s[row, column] == 1:
                ones.append((row, column))
            elif s[row, column] == 7:
                sevens.append((row, column))

    new_s = transformer.switch_numbers(s, 1, 7, inplace=True)
    nose.tools.eq_(s, new_s)

    for row, column in sevens:
        nose.tools.eq_(new_s[row, column], 1)

    for row, column in ones:
        nose.tools.eq_(new_s[row, column], 7)


def test_switch_rows():
    s = Sudoku(Sudoku.COMPLETED_GRID)
    new_s = transformer.switch_rows(s, 0, 0, 1)
    nose.tools.ok_(s != new_s)

    for column in range(9):
        nose.tools.eq_(s[0, column], new_s[1, column])
        nose.tools.eq_(s[1, column], new_s[0, column])


def test_switch_rows_inplace():
    s = Sudoku(Sudoku.COMPLETED_GRID)
    old_s = s.clone()

    new_s = transformer.switch_rows(s, 0, 0, 1, inplace=True)
    nose.tools.ok_(s is new_s)

    for column in range(9):
        nose.tools.eq_(old_s[0, column], new_s[1, column])
        nose.tools.eq_(old_s[1, column], new_s[0, column])


def test_switch_columns():
    s = Sudoku(Sudoku.COMPLETED_GRID)
    new_s = transformer.switch_columns(s, 0, 0, 1)
    nose.tools.ok_(s != new_s)

    for row in range(9):
        nose.tools.eq_(s[row, 0], new_s[row, 1])
        nose.tools.eq_(s[row, 1], new_s[row, 0])


def test_switch_columns_inplace():
    s = Sudoku(Sudoku.COMPLETED_GRID)
    old_s = s.clone()

    new_s = transformer.switch_columns(s, 0, 0, 1, inplace=True)
    nose.tools.ok_(s is new_s)

    for row in range(9):
        nose.tools.eq_(old_s[row, 0], new_s[row, 1])
        nose.tools.eq_(old_s[row, 1], new_s[row, 0])


def test_switch_row_blocks():
    s = Sudoku(Sudoku.COMPLETED_GRID)

    new_s = transformer.switch_row_blocks(s, 0, 1)
    nose.tools.ok_(s != new_s)

    for row in range(3):
        for column in range(9):
            nose.tools.eq_(s[row, column], new_s[row + 3, column])
            nose.tools.eq_(s[row + 3, column], new_s[row, column])


def test_switch_row_blocks_inplace():
    s = Sudoku(Sudoku.COMPLETED_GRID)
    old_s = s.clone()

    new_s = transformer.switch_row_blocks(s, 0, 1, inplace=True)
    nose.tools.ok_(s is new_s)

    for row in range(3):
        for column in range(9):
            nose.tools.eq_(old_s[row, column], new_s[row + 3, column])
            nose.tools.eq_(old_s[row + 3, column], new_s[row, column])


def test_switch_column_blocks():
    s = Sudoku(Sudoku.COMPLETED_GRID)

    new_s = transformer.switch_column_blocks(s, 0, 1)
    nose.tools.ok_(s != new_s)

    for column in range(3):
        for row in range(9):
            nose.tools.eq_(s[row, column + 3], new_s[row, column])
            nose.tools.eq_(s[row, column], new_s[row, column + 3])


def test_switch_column_blocks_inplace():
    s = Sudoku(Sudoku.COMPLETED_GRID)
    old_s = s.clone()

    new_s = transformer.switch_column_blocks(s, 0, 1, inplace=True)
    nose.tools.ok_(s is new_s)

    for column in range(3):
        for row in range(9):
            nose.tools.eq_(old_s[row, column + 3], new_s[row, column])
            nose.tools.eq_(old_s[row, column], new_s[row, column + 3])
