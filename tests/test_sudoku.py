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
    s = Sudoku(Sudoku.COMPLETED_GRID)
    nose.tools.ok_(s.completed, "Sudoku is not solved")


def test_broken_sudoku():
    s = Sudoku(Sudoku.COMPLETED_GRID)
    s[5, 5] = 1
    nose.tools.ok_(not s.completed, "Sudoku should be broken")


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


def test_possibilities_when_completed():
    s = Sudoku(Sudoku.COMPLETED_GRID)
    for row in range(9):
        for column in range(9):
            nose.tools.eq_([s[row, column]], s.possible_entries[row, column])


def test_possibilities_when_empty():
    s = Sudoku()

    for row in range(9):
        for column in range(9):
            nose.tools.eq_(list(range(1, 10)), s.possible_entries[row, column])


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

    nose.tools.eq_(s.possible_entries[0, 0], [1, 2])
    nose.tools.eq_(s.possible_entries[0, 1], [1, 2])
    nose.tools.eq_(s.possible_entries[0, 2], [1, 2, 3])

    nose.tools.eq_(s.possible_entries[1, 0], [1, 2, 4])
    nose.tools.eq_(s.possible_entries[1, 1], [1, 2, 5])
    nose.tools.eq_(s.possible_entries[1, 2], [1, 2, 6])

    nose.tools.eq_(s.possible_entries[2, 0], [1, 2, 7])
    nose.tools.eq_(s.possible_entries[2, 1], [1, 2, 8])
    nose.tools.eq_(s.possible_entries[2, 2], [1, 2, 9])
