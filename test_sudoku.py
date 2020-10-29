import nose.tools
from textwrap import dedent
from sudoku import Sudoku


def test_empty_sudoku_repr():
    s = Sudoku()
    nose.tools.eq_(
        str(s),
        dedent(
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
        ),
    )


def test_set_get_elements():
    s = Sudoku()
    for row, column, value in zip(range(9), range(9), range(10)):
        s[row, column] = value
        nose.tools.eq_(s[row, column], value)


def test_set_elements_repr():
    s = Sudoku()
    s[0, 2] = 1
    s[2, 0] = 2
    s[2, 2] = 3
    s[8, 8] = 4

    nose.tools.eq_(
        str(s),
        dedent(
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
        ),
    )


def test_check_empty_sudoku():
    s = Sudoku()
    nose.tools.ok_(s.check())


def test_check_bad_block_sudoku():
    s = Sudoku()
    s[0, 0] = 1
    s[2, 2] = 1
    nose.tools.ok_(not s.check())


def test_check_bad_row_sudoku():
    s = Sudoku()
    s[0, 0] = 1
    s[0, 1] = 1
    nose.tools.ok_(not s.check())


def test_check_bad_column_sudoku():
    s = Sudoku()
    s[0, 0] = 1
    s[1, 0] = 1
    nose.tools.ok_(not s.check())


def test_completed_sudoku():
    s = Sudoku()
    s.set(
        dedent(
            """\
        -------------
        |123|456|789|
        |456|789|123|
        |789|123|456|
        -------------
        |234|567|891|
        |567|891|234|
        |891|234|567|
        -------------
        |345|678|912|
        |678|912|345|
        |912|345|678|
        -------------
    """
        )
    )
    nose.tools.ok_(s.completed, "Sudoku is not solved")


def test_no_empty_locations():
    s = Sudoku()

    for row in range(9):
        for column in range(9):
            s[row, column] = 1

    nose.tools.eq_(s.empty_locations, [])


def test_some_empty_locations():
    s = Sudoku()

    for row in range(9):
        for column in range(9):
            s[row, column] = 1

    s[1, 1] = 0
    s[2, 0] = 0
    s[0, 3] = 0

    nose.tools.eq_(s.empty_locations, [(0, 3), (1, 1), (2, 0)])
