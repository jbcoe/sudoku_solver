import sudoku
from sudoku import Sudoku
import numpy as np


def switch_rows(
    s: Sudoku, row_block: int, first: int, second: int, inplace: bool = False
) -> Sudoku:
    assert row_block in list(
        range(3)
    ), f"row_block '{row_block}' must be a block index [0,1,2]"

    assert first in list(range(3)), f"first '{first}' must be a sub-block index [0,1,2]"

    assert second in list(
        range(3)
    ), f"second '{second}' must be a sub-block index [0,1,2]"

    swap = np.array([0] * 9, dtype=np.uint8)

    if not inplace:
        s = s.clone()

    for i in range(9):
        swap[i] = s[row_block * 3 + first, i]

    for i in range(9):
        s[row_block * 3 + first, i] = s[row_block * 3 + second, i]

    for i in range(9):
        s[row_block * 3 + second, i] = swap[i]

    return s


def switch_columns(
    s: Sudoku, column_block: int, first: int, second: int, inplace: bool = False
) -> Sudoku:
    assert column_block in list(
        range(3)
    ), f"column_block '{column_block}' must be a block index [0,1,2]"

    assert first in list(range(3)), f"first '{first}' must be a sub-block index [0,1,2]"

    assert second in list(
        range(3)
    ), f"second '{second}' must be a sub-block index [0,1,2]"

    if not inplace:
        s = s.clone()

    swap = np.array([0] * 9, dtype=np.uint8)

    for i in range(9):
        swap[i] = s[i, column_block * 3 + first]

    for i in range(9):
        s[i, column_block * 3 + first] = s[i, column_block * 3 + second]

    for i in range(9):
        s[i, column_block * 3 + second] = swap[i]

    return s


def switch_column_blocks(
    s: Sudoku, first: int, second: int, inplace: bool = False
) -> Sudoku:
    assert first in list(
        range(3)
    ), f"first '{first}' must be a block index index [0,1,2]"

    assert second in list(
        range(3)
    ), f"second '{second}' must be a block index index [0,1,2]"

    if not inplace:
        s = s.clone()

    swap = np.array([0] * 9, dtype=np.uint8)

    for j in range(3):
        for i in range(9):
            swap[i] = s[i, first * 3 + j]

        for i in range(9):
            s[i, first * 3 + j] = s[i, second * 3 + j]

        for i in range(9):
            s[i, second * 3 + j] = swap[i]

    return s


def switch_row_blocks(
    s: Sudoku, first: int, second: int, inplace: bool = False
) -> Sudoku:
    assert first in list(
        range(3)
    ), f"first '{first}' must be a block index index [0,1,2]"

    assert second in list(
        range(3)
    ), f"second '{second}' must be a block index index [0,1,2]"

    if not inplace:
        s = s.clone()

    swap = np.array([0] * 9, dtype=np.uint8)

    for j in range(3):
        for i in range(9):
            swap[i] = s[first * 3 + j, i]

        for i in range(9):
            s[first * 3 + j, i] = s[second * 3 + j, i]

        for i in range(9):
            s[second * 3 + j, i] = swap[i]

    return s


def switch_numbers(s: Sudoku, first: int, second: int, inplace: bool = False) -> Sudoku:
    assert first in list(
        range(1, 10)
    ), f"first '{first}' must be a number in {range(1,10)}"
    assert second in list(
        range(1, 10)
    ), f"second '{second}' must be a number in {range(1,10)}"

    if not inplace:
        s = s.clone()

    for i in range(9):
        for j in range(9):
            if s[i, j] == first:
                s[i, j] = 10
            if s[i, j] == second:
                s[i, j] = 20

    for i in range(9):
        for j in range(9):
            if s[i, j] == 10:
                s[i, j] = second
            if s[i, j] == 20:
                s[i, j] = first

    return s