from sudoku import Sudoku
from typing import *
import numpy as np

RNG_2_10 = np.array([2, 3, 4, 5, 6, 7, 8, 9])
RNG_9 = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8])


def solve(s: Sudoku, exhaustive: bool = False):
    solutions: List[Sudoku] = []
    _rsolve(
        s.clone(), solutions=solutions, explored_branches=set(), exhaustive=exhaustive
    )
    return solutions


def _complete_unambiguous_cells(s: Sudoku) -> bool:
    updated = False
    for row in RNG_9:
        for column in RNG_9:
            if s[row, column] != 0:
                continue
            possible_entries = s.possible_entries(row, column)
            if len(possible_entries) == 1:
                s[row, column] = possible_entries[0]
                updated = True
    return updated


def _rsolve(
    s: Sudoku,
    *,
    solutions: List[Sudoku],
    explored_branches: Set[Sudoku],
    exhaustive: bool,
):
    # Fill in unambiguous cells
    while _complete_unambiguous_cells(s):
        ...
    if s.completed:
        solutions.append(s)
        if not exhaustive:
            return

    # Branch and solve for ambiguous cells
    for max_branches in RNG_2_10:
        for row in RNG_9:
            for column in RNG_9:
                if s[row, column] != 0:
                    continue
                possible_entries = s.possible_entries(row, column)
                if len(possible_entries) > max_branches:
                    continue
                for entry in possible_entries:
                    if solutions and not exhaustive:
                        return
                    s2 = s.clone()
                    s2[row, column] = entry
                    if s2 in explored_branches:
                        continue
                    else:
                        explored_branches.add(s2)
                        _rsolve(
                            s2,
                            solutions=solutions,
                            explored_branches=explored_branches,
                            exhaustive=exhaustive,
                        )
