from enum import Enum
from itertools import product

from tango_parser import TangoParser


class Cell(Enum):
    EMPTY = "empty"
    MOON = "moon"
    SUN = "sun"


class Edge(Enum):
    NONE = "none"
    CROSS = "cross"
    EQUAL = "equal"


class Line:
    def __init__(self, cells: list[Cell], edges: list[Edge]):
        self.size = 6
        assert len(cells) == self.size and len(edges) == self.size - 1, \
            f"A Line must have exactly {self.size} cells and {self.size - 1} edges."
        self.cells = cells
        self.edges = edges

    def is_filled(self) -> bool:
        return Cell.EMPTY not in self.cells

    def is_valid(self, assigned_cells: list[Cell]) -> bool:
        """
        Check if a given cell assignment is valid according to the constraints.
        """
        for i in range(self.size):
            if i >= 2 and assigned_cells[i - 1] == assigned_cells[i - 2] and assigned_cells[i - 1] != Cell.EMPTY:
                if assigned_cells[i] == assigned_cells[i - 1]:
                    return False
            if i < self.size - 2 and assigned_cells[i + 1] == assigned_cells[i + 2] and assigned_cells[i + 1] != Cell.EMPTY:
                if assigned_cells[i] == assigned_cells[i + 1]:
                    return False
            if 0 < i < self.size - 1 and assigned_cells[i + 1] == assigned_cells[i - 1] and assigned_cells[i + 1] != Cell.EMPTY:
                if assigned_cells[i] == assigned_cells[i + 1]:
                    return False

            if assigned_cells.count(Cell.MOON) > 3 or assigned_cells.count(Cell.SUN) > 3:
                return False

            if i > 0 and self.edges[i - 1] == Edge.CROSS and assigned_cells[i - 1] != Cell.EMPTY:
                if assigned_cells[i] == assigned_cells[i - 1]:
                    return False
            if i > 0 and self.edges[i - 1] == Edge.EQUAL and assigned_cells[i - 1] != Cell.EMPTY:
                if assigned_cells[i] != assigned_cells[i - 1]:
                    return False

            if i < self.size - 1 and self.edges[i] == Edge.CROSS and assigned_cells[i + 1] != Cell.EMPTY:
                if assigned_cells[i] == assigned_cells[i + 1]:
                    return False
            if i < self.size - 1 and self.edges[i] == Edge.EQUAL and assigned_cells[i + 1] != Cell.EMPTY:
                if assigned_cells[i] != assigned_cells[i + 1]:
                    return False

        return True

    def assigning_options(self) -> list[tuple[int, Cell]]:
        """
        Find cells that always have the same value across all valid assignments.
        """
        empty_indices = [i for i, cell in enumerate(self.cells) if cell == Cell.EMPTY]
        all_possible_assignments = product([Cell.MOON, Cell.SUN], repeat=len(empty_indices))

        valid_assignments = []
        for assignment in all_possible_assignments:
            new_cells = self.cells.copy()
            for index, value in zip(empty_indices, assignment):
                new_cells[index] = value

            if self.is_valid(new_cells):
                valid_assignments.append(new_cells)

        if not valid_assignments:
            return []

        assignment_options = [{assign[i] for assign in valid_assignments} for i in empty_indices]

        result = []
        for i, index in enumerate(empty_indices):
            if len(assignment_options[i]) == 1:  # Only one shape was assigned consistently
                result.append((index, assignment_options[i].pop()))
        return result


class TangoSolver:
    def __init__(self, parser: TangoParser):
        self.size = 6
        self.parser = parser
        self.rows = []
        self.columns = []
        board_data: list[list[tuple[str, str, str]]] = self.parser.dump_cells()
        for row_index, row_data in enumerate(board_data):
            cells_row = []
            right_edges_row = []
            for column_index, cell_data in enumerate(row_data):
                filling, _, right_edge_type = cell_data
                cells_row.append(Cell(filling))
                if column_index < self.size - 1:
                    right_edges_row.append(Edge(right_edge_type))
            self.rows.append(Line(cells_row, right_edges_row))

        for column_index in range(self.size):
            cells_column = []
            down_edges_column = []
            for row_index in range(self.size):
                filling, down_edge, _ = board_data[row_index][column_index]
                cells_column.append(Cell(filling))
                if row_index < self.size - 1:
                    down_edges_column.append(Edge(down_edge))
            self.columns.append(Line(cells_column, down_edges_column))

    def is_filled(self) -> bool:
        """ Checks if the entire board is filled. """
        return all(row.is_filled() for row in self.rows) and all(column.is_filled() for column in self.columns)

    def assign(self, row: int, column: int, cell: Cell):
        """ Assigns a cell to the row and column. """
        self.rows[row].cells[column] = cell
        self.columns[column].cells[row] = cell
        if cell == Cell.MOON:
            self.parser.assign_moon(row, column)
        elif cell == Cell.SUN:
            self.parser.assign_sun(row, column)
        else:
            raise ValueError("Invalid cell type")

    def solve(self):
        while not self.is_filled():
            for row_index, row in enumerate(self.rows):
                for column_index, value in row.assigning_options():
                    self.assign(row_index, column_index, value)
            for column_index, column in enumerate(self.columns):
                for row_index, value in column.assigning_options():
                    self.assign(row_index, column_index, value)
        print("Game solved!")


if __name__ == '__main__':
    tango_parser = TangoParser()
    tango_game = TangoSolver(tango_parser)
    tango_game.solve()