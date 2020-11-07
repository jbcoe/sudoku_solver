from typing import *
import numpy as np
from textwrap import dedent


class Sudoku:
    COMPLETED_GRID = dedent(
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

    def __init__(self, grid_string=None):
        self.grid = np.array([[0] * 9] * 9, dtype=np.uint8)
        if grid_string:
            self.set(grid_string)
        self._bool_buffer = np.array([False] * 10)
        self._int_buffer = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])

    def __hash__(self):
        return hash(self.grid.tobytes())

    def __eq__(self, other):
        return (self.grid == other.grid).all()

    def dump_py(self, name="s") -> str:
        dump = ""
        for row, line in enumerate(self.grid):
            for column, number in enumerate(line):
                if number != 0:
                    dump += f"{name}[{row}, {column}] = {number}\n"
        return dump

    def set(self, grid_string: str):
        grid_string.replace(" ", "0")
        values = [int(c) for c in grid_string if c.isnumeric()]
        self.grid[:] = np.reshape(values, (9, 9))

    def clone(self):
        s = Sudoku()
        s.grid = self.grid.copy()
        return s

    def __repr__(self):
        line_break = "-------------\n"
        repr = ""
        for row, line in enumerate(self.grid):
            if row % 3 == 0:
                repr += line_break
            for column, number in enumerate(line):
                if column % 3 == 0:
                    repr += "|"
                if number == 0:
                    repr += " "
                else:
                    repr += str(number)
            repr += "|\n"
        repr += line_break
        return repr

    def block(self, row, column):
        block_row = (row // 3) * 3
        block_column = (column // 3) * 3
        return self.grid[block_row : block_row + 3, block_column : block_column + 3]

    def row(self, index):
        return self.grid[index, :]

    def column(self, index):
        return self.grid[:, index]

    def possible_entries(self, row: int, column: int) -> List[int]:
        if self.grid[row, column] != 0:
            return [self.grid[row, column]]

        possibilities = self._bool_buffer
        possibilities[1:] = True

        for element in self.row(row):
            possibilities[element] = False
        for element in self.column(column):
            possibilities[element] = False
        for element in list(self.block(row, column)):
            possibilities[element] = False

        rv = np.array(self._int_buffer[possibilities == True])
        possibilities[1:] = False
        return rv

    def _check_row(self, row):
        number_count = np.zeros(10)
        for number in self.grid[row, 0:]:
            if number > 0:
                number_count[number] += 1
                if number_count[number] > 1:
                    return False
        return True

    def _check_rows(self):
        for row in range(9):
            if not self._check_row(row):
                return False
        return True

    def _check_column(self, column):
        number_count = np.zeros(10)
        for number in self.grid[0:, column]:
            if number > 0:
                number_count[number] += 1
                if number_count[number] > 1:
                    return False
        return True

    def _check_columns(self):
        for column in range(9):
            if not self._check_column(column):
                return False
        return True

    def _check_block(self, row_offset, column_offset):
        number_count = np.zeros(10)
        for row in [0, 1, 2]:
            for column in [0, 1, 2]:
                number: int = self.grid[row_offset + row, column_offset + column]
                if number > 0:
                    number_count[number] += 1
                    if number_count[number] > 1:
                        return False
        return True

    def _check_blocks(self):
        for row_offset in [0, 3, 6]:
            for column_offset in [0, 3, 6]:
                if not self._check_block(row_offset, column_offset):
                    return False
        return True

    def check(self) -> bool:
        if not self._check_blocks():
            return False
        if not self._check_rows():
            return False
        if not self._check_columns():
            return False
        return True

    @property
    def ok(self):
        return self.check()

    @property
    def empty_locations(self):
        locations = []
        for column, line in enumerate(self.grid):
            for row, number in enumerate(line):
                if number == 0:
                    locations.append((column, row))
        return sorted(locations)

    @property
    def completed(self):
        return not 0 in self.grid and self.ok

    def __getitem__(self, row_column):
        row, column = row_column
        assert row >= 0 and row < 9
        assert column >= 0 and column < 9
        return self.grid[row, column]

    def __setitem__(self, row_column, value):
        row, column = row_column
        assert row >= 0 and row < 9
        assert column >= 0 and column < 9
        self.grid[row, column] = value
