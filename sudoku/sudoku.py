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

    def dump_py(self, name="s") -> str:
        dump = ""
        for row, line in enumerate(self.grid):
            for column, number in enumerate(line):
                if number != 0:
                    dump += f"{name}[{row}, {column}] = {number}\n"
        return dump

    def set(self, grid_string: str):
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

    @property
    def possible_entries(self):
        assert self.check(), "Sudoku fails a self-check"

        class PossibleEntries:
            def __init__(self, sudoku: "Soduku"):
                self.sudoku = sudoku

            def __getitem__(self, row_column):
                row, column = row_column
                if self.sudoku[row, column] != 0:
                    return [self.sudoku[row, column]]

                possibilities = set(range(10))
                for i in range(9):
                    possibilities.discard(self.sudoku[i, column])
                for j in range(9):
                    possibilities.discard(self.sudoku[row, j])

                block_row = row // 3
                block_column = column // 3
                for i in range(3):
                    for j in range(3):
                        possibilities.discard(
                            self.sudoku[block_row + i, block_column + j]
                        )
                return sorted(list(possibilities))

        return PossibleEntries(self)

    def _check_row(self, row):
        number_count = {x + 1: 0 for x in range(9)}
        for number in self.grid[row, 0:]:
            if number in number_count.keys():
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
        number_count = {x + 1: 0 for x in range(9)}
        for number in self.grid[0:, column]:
            if number in number_count.keys():
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
        number_count = {x + 1: 0 for x in range(9)}
        for row in [0, 1, 2]:
            for column in [0, 1, 2]:
                number: int = self[row_offset + row, column_offset + column]
                if number in number_count.keys():
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
    def empty_locations(self):
        locations = []
        for column, line in enumerate(self.grid):
            for row, number in enumerate(line):
                if number == 0:
                    locations.append((column, row))
        return sorted(locations)

    @property
    def completed(self):
        return self.check() and not self.empty_locations

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
