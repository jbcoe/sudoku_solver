import pytest
from textwrap import dedent
from sudoku import Sudoku


def test_empty_sudoku_repr():
    s = Sudoku()
    assert str(s) == dedent(
        """\
        -------------
        |   |   |   |
        |   |   |   |
        |   |   |   |
        -------------
        |   |   |   |
        |   |   |   |
        |   |   |   |
        -------------
        |   |   |   |
        |   |   |   |
        |   |   |   |
        -------------\n"""
    )


def test_set_get_elements():
    s = Sudoku()
    for row, column, value in zip(range(9), range(9), range(10)):
        s[row, column] = value
        assert s[row, column] == value


def test_set_elements_repr():
    s = Sudoku()
    s[0, 2] = 1
    s[2, 0] = 2
    s[2, 2] = 3
    s[8, 8] = 4

    assert str(s) == dedent(
        """\
        -------------
        |  1|   |   |
        |   |   |   |
        |2 3|   |   |
        -------------
        |   |   |   |
        |   |   |   |
        |   |   |   |
        -------------
        |   |   |   |
        |   |   |   |
        |   |   |  4|
        -------------\n"""
    )


def test_check_empty_sudoku():
    s = Sudoku()
    assert s.check()


def test_check_bad_block_sudoku():
    s = Sudoku()
    s[0, 0] = 1
    s[2, 2] = 1
    assert not s.check()


def test_check_bad_row_sudoku():
    s = Sudoku()
    s[0, 0] = 1
    s[0, 1] = 1
    assert not s.check()


def test_check_bad_column_sudoku():
    s = Sudoku()
    s[0, 0] = 1
    s[1, 0] = 1
    assert not s.check()


def test_completed_sudoku():
    s = Sudoku(Sudoku.COMPLETED_GRID)
    assert s.completed


def test_broken_sudoku():
    s = Sudoku(Sudoku.COMPLETED_GRID)
    s[5, 5] = 1
    assert not s.completed


def test_no_empty_locations():
    s = Sudoku()

    for row in range(9):
        for column in range(9):
            s[row, column] = 1

    assert s.empty_locations == []


def test_some_empty_locations():
    s = Sudoku()

    for row in range(9):
        for column in range(9):
            s[row, column] = 1

    s[1, 1] = 0
    s[2, 0] = 0
    s[0, 3] = 0

    assert s.empty_locations == [(0, 3), (1, 1), (2, 0)]


def test_possibilities_when_completed():
    s = Sudoku(Sudoku.COMPLETED_GRID)
    for row in range(9):
        for column in range(9):
            assert [s[row, column]] == s.possible_entries(row, column)


def test_possibilities_when_empty():
    s = Sudoku()

    for row in range(9):
        for column in range(9):
            assert list(range(1, 10)) == s.possible_entries(row, column)


def test_possibilities_when_incomplete():
    s = Sudoku()
    # Remove '1', '2' and the top-left block from a completed Sudoku.
    s.set(
        dedent(
            """\
        -------------
        |000|456|789|
        |000|789|003|
        |000|003|456|
        -------------
        |034|567|890|
        |567|890|034|
        |890|034|567|
        -------------
        |345|678|900|
        |678|900|345|
        |900|345|678|
        -------------
        """
        )
    )

    assert s.possible_entries(0, 0) == [1, 2]
    assert s.possible_entries(0, 1) == [1, 2]
    assert s.possible_entries(0, 2) == [1, 2, 3]

    assert s.possible_entries(1, 0) == [1, 2, 4]
    assert s.possible_entries(1, 1) == [1, 2, 5]
    assert s.possible_entries(1, 2) == [1, 2, 6]

    assert s.possible_entries(2, 0) == [1, 2, 7]
    assert s.possible_entries(2, 1) == [1, 2, 8]
    assert s.possible_entries(2, 2) == [1, 2, 9]
