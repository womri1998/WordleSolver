import pytest
from unittest.mock import Mock
from zip_solver import ZipSolver
from zip_parser import ZipParser

EXAMPLE_BOARD = [
    [  11, None, None,    6, None,    7],
    [None, None,   10, None,    1, None],
    [None,    3, None,     5, None, None],
    [   9, None,    4, None, None, None],
    [None,    2, None, None, None, None],
    [   8, None, None, None, None, None]
]

SOLUTION_PATH = [
    (1, 4),
    (2, 4), (3, 4), (4, 4), (4, 3), (4, 2), (4, 1),
    (3, 1), (2, 1),
    (2, 2), (3, 2),
    (3, 3), (2, 3),
    (1, 3), (0, 3),
    (0, 4), (0, 5),
    (1, 5), (2, 5), (3, 5), (4, 5), (5, 5), (5, 4), (5, 3), (5, 2), (5, 1), (5, 0),
    (4, 0), (3, 0),
    (2, 0), (1, 0), (1, 1), (1, 2),
    (0, 2), (0, 1), (0, 0)
]


def test_zip_solver_solve():
    mock_parser = Mock(spec=ZipParser)
    # The solver expects load_cells to initialise internal data and dump_cells
    # to return the current board state. When mocking we simply return the
    # example board for dump_cells and ignore the result of load_cells.
    mock_parser.load_cells.return_value = None
    mock_parser.dump_cells.return_value = EXAMPLE_BOARD

    zip_solver = ZipSolver(mock_parser)
    result = zip_solver.find_solution()

    assert result == SOLUTION_PATH, print(f"Expected: {SOLUTION_PATH}\nActual: {result}")
