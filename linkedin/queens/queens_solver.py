from enum import Enum
from typing import Callable
from selenium.webdriver.remote.webelement import WebElement

from queens_parser import QueensParser


class CellContent(Enum):
    EMPTY = "empty"
    QUEEN = "queen"
    CROSS = "cross"


class Cell:
    def __init__(self, row_index: int, column_index: int, content: CellContent, color: str, cell_element: WebElement):
        self.row_index = row_index
        self.column_index = column_index
        self.content = content
        self.color = color
        self.web_element = cell_element
        self.row: Row | None = None
        self.column: Column | None = None
        self.color_group: ColorGroup | None = None

    def assign_groups(self, row: 'Row', column: 'Column', color_group: 'ColorGroup'):
        self.row = row
        self.column = column
        self.color_group = color_group

    def click(self):
        self.web_element.click()
        if self.content == CellContent.EMPTY:
            self.content = CellContent.CROSS
        elif self.content == CellContent.CROSS:
            self.content = CellContent.QUEEN


class CellGroup:
    def __init__(self, cells: list[Cell]):
        self.cells = cells

    def is_filled(self) -> bool:
        return all(cell.content != CellContent.EMPTY for cell in self.cells)

    def contains_queen(self) -> bool:
        return any(cell.content == CellContent.QUEEN for cell in self.cells)

    def trivial_solution(self) -> Cell | None:
        if sum(cell.content == CellContent.EMPTY for cell in self.cells) > 1 or self.contains_queen():
            return None
        for cell in self.cells:
            if cell.content == CellContent.EMPTY:
                cell.click()
                cell.click()
                return cell

    def optional_rows(self) -> set[int]:
        return {cell.row_index for cell in self.cells if cell.content == CellContent.EMPTY}

    def optional_columns(self) -> set[int]:
        return {cell.column_index for cell in self.cells if cell.content == CellContent.EMPTY}

    def optional_colors(self) -> set[str]:
        return {cell.color for cell in self.cells if cell.content == CellContent.EMPTY}

    def cross_all(self):
        for cell in self.cells:
            if cell.content == CellContent.EMPTY:
                cell.click()

    def groups_sharing_row(self, other_groups: list['CellGroup']) -> list['CellGroup']:
        return [other_group for other_group in other_groups if self.optional_rows() & other_group.optional_rows()]

    def groups_sharing_column(self, other_groups: list['CellGroup']) -> list['CellGroup']:
        return [other_group for other_group in other_groups if self.optional_columns() & other_group.optional_columns()]

    def groups_sharing_color(self, other_groups: list['CellGroup']) -> list['CellGroup']:
        return [other_group for other_group in other_groups if self.optional_colors() & other_group.optional_colors()]


class ColorGroup(CellGroup):
    def __init__(self, cells: list[Cell]):
        super().__init__(cells)
        self.color = cells[0].color
        assert all(cell.color == cells[0].color for cell in cells)

    def __repr__(self):
        return f"{self.__class__.__name__} {self.cells[0].color}: ({[(cell.content.value, cell.row_index, cell.column_index) for cell in self.cells]})"


class Row(CellGroup):
    def __init__(self, cells: list[Cell]):
        super().__init__(cells)
        assert all(cell.row_index == cells[0].row_index for cell in cells)

    def __repr__(self):
        return f"{self.__class__.__name__} {self.cells[0].row_index}: ({[(cell.content.value, cell.color) for cell in self.cells]})"


class Column(CellGroup):
    def __init__(self, cells: list[Cell]):
        super().__init__(cells)
        assert all(cell.column_index == cells[0].column_index for cell in cells)

    def __repr__(self):
        return f"{self.__class__.__name__} {self.cells[0].column_index}: ({[(cell.content.value, cell.color) for cell in self.cells]})"


class QueensSolver:
    def __init__(self, queens_parser: QueensParser):
        self.queens_parser = queens_parser
        cells_data = queens_parser.dump_cells()
        self.size = queens_parser.size
        cells = []
        for row_index in range(self.size):
            cells.append([])
            for column_index in range(self.size):
                content, color, cell_element = cells_data[row_index][column_index]
                cell = Cell(row_index, column_index, CellContent(content), color, cell_element)
                cells[row_index].append(cell)
        self.rows = [Row(row_cells) for row_cells in cells]
        self.columns = []
        for column_index in range(self.size):
            column = Column([cells[row_index][column_index] for row_index in range(self.size)])
            self.columns.append(column)
        color_groups_lists = {}
        for row_index in range(self.size):
            for column_index in range(self.size):
                cell = cells[row_index][column_index]
                if cell.color not in color_groups_lists:
                    color_groups_lists[cell.color] = [cell]
                else:
                    color_groups_lists[cell.color].append(cell)
        self.color_groups = {color: ColorGroup(color_groups_list) for color, color_groups_list in color_groups_lists.items()}
        for row_index, row_group in enumerate(self.rows):
            for column_index, cell in enumerate(row_group.cells):
                column_group = self.columns[column_index]
                color_group = self.color_groups[cell.color]
                cell.assign_groups(row_group, column_group, color_group)
        for row in self.rows:
            for cell in row.cells:
                if cell.content == CellContent.QUEEN:
                    self.cross_all(cell)

    def is_filled(self) -> bool:
        return all(cell.content != CellContent.EMPTY for row in self.rows for cell in row.cells)

    def cross_all(self, cell: Cell):
        cell.row.cross_all()
        cell.column.cross_all()
        cell.color_group.cross_all()
        row_index = cell.row_index
        column_index = cell.column_index
        nontrivial_adjacent_cells = []
        if row_index > 0 and column_index > 0:
            nontrivial_adjacent_cells.append(self.rows[row_index - 1].cells[column_index - 1])
        if row_index > 0 and column_index < self.size - 1:
            nontrivial_adjacent_cells.append(self.rows[row_index - 1].cells[column_index + 1])
        if row_index < self.size - 1 and column_index > 0:
            nontrivial_adjacent_cells.append(self.rows[row_index + 1].cells[column_index - 1])
        if row_index < self.size - 1 and column_index < self.size - 1:
            nontrivial_adjacent_cells.append(self.rows[row_index + 1].cells[column_index + 1])
        for adjacent_cell in nontrivial_adjacent_cells:
            if adjacent_cell.content == CellContent.EMPTY:
                adjacent_cell.click()

    def solve(self):
        while not self.is_filled():
            for row_index, row in enumerate(self.rows):
                cell = row.trivial_solution()
                if cell is not None:
                    self.cross_all(cell)
                color_options = row.optional_colors()
                if len(color_options) == 1:
                    color = color_options.pop()
                    for cell in self.color_groups[color].cells:
                        if cell.row_index != row_index and cell.content == CellContent.EMPTY:
                            cell.click()

            for column_index, column in enumerate(self.columns):
                cell = column.trivial_solution()
                if cell is not None:
                    self.cross_all(cell)
                color_options = column.optional_colors()
                if len(color_options) == 1:
                    color = color_options.pop()
                    for cell in self.color_groups[color].cells:
                        if cell.column_index != column_index and cell.content == CellContent.EMPTY:
                            cell.click()

            for color, color_group in self.color_groups.items():
                cell = color_group.trivial_solution()
                if cell is not None:
                    self.cross_all(cell)
                row_options = color_group.optional_rows()
                if len(row_options) == 1:
                    row_index = row_options.pop()
                    for cell in self.rows[row_index].cells:
                        if cell.color != color and cell.content == CellContent.EMPTY:
                            cell.click()
                column_options = color_group.optional_columns()
                if len(column_options) == 1:
                    column_index = column_options.pop()
                    for cell in self.columns[column_index].cells:
                        if cell.color != color and cell.content == CellContent.EMPTY:
                            cell.click()


def bfs(start_node: CellGroup, get_neighbors: Callable) -> set[CellGroup]:
    queue = [start_node]
    component = set(queue)
    while queue:
        node = queue.pop(0)
        for neighbor in get_neighbors(node):
            if neighbor not in component:
                component.add(neighbor)
                queue.append(neighbor)
    return component


def get_connected_components(nodes: list[CellGroup], get_neighbors: Callable) -> list[set[CellGroup]]:
    connected_components = []
    visited = set()
    for cell in nodes:
        if cell not in visited:
            component = bfs(cell, get_neighbors)
            connected_components.append(component)
            visited.update(component)
    return connected_components


class QueensSolver2(QueensSolver):
    def solve(self):
        while not self.is_filled():
            for row_index, row in enumerate(self.rows):
                cell = row.trivial_solution()
                if cell is not None:
                    self.cross_all(cell)
            for column_index, column in enumerate(self.columns):
                cell = column.trivial_solution()
                if cell is not None:
                    self.cross_all(cell)
            for color, color_group in self.color_groups.items():
                cell = color_group.trivial_solution()
                if cell is not None:
                    self.cross_all(cell)
            row2column_components = get_connected_components(self.rows, CellGroup.groups_sharing_column)
            for component in row2column_components:
                mapped_component = set().union(*(row.optional_columns() for row in component))
                if len(mapped_component) == len(component):
                    for column_index in mapped_component:
                        column = self.columns[column_index]
                        for cell in column.cells:
                            if cell.row_index not in component and cell.content == CellContent.EMPTY:
                                cell.click()
            row2color_components = get_connected_components(self.rows, CellGroup.groups_sharing_color)
            for component in row2color_components:
                mapped_component = set().union(*(row.optional_colors() for row in component))
                if len(mapped_component) == len(component):
                    for color in mapped_component:
                        color_group = self.color_groups[color]
                        for cell in color_group.cells:
                            if cell.row_index not in component and cell.content == CellContent.EMPTY:
                                cell.click()
            column2row_components = get_connected_components(self.columns, CellGroup.groups_sharing_row)
            for component in column2row_components:
                mapped_component = set().union(*(column.optional_rows() for column in component))
                if len(mapped_component) == len(component):
                    for row_index in mapped_component:
                        row = self.rows[row_index]
                        for cell in row.cells:
                            if cell.column_index not in component and cell.content == CellContent.EMPTY:
                                cell.click()
            column2color_components = get_connected_components(self.columns, CellGroup.groups_sharing_color)
            for component in column2color_components:
                mapped_component = set().union(*(column.optional_colors() for column in component))
                if len(mapped_component) == len(component):
                    for color in mapped_component:
                        color_group = self.color_groups[color]
                        for cell in color_group.cells:
                            if cell.column_index not in component and cell.content == CellContent.EMPTY:
                                cell.click()
            color2row_components = get_connected_components(list(self.color_groups.values()), CellGroup.groups_sharing_row)
            for component in color2row_components:
                mapped_component = set().union(*(color_group.optional_rows() for color_group in component))
                if len(mapped_component) == len(component):
                    for row_index in mapped_component:
                        row = self.rows[row_index]
                        for cell in row.cells:
                            if cell.color not in component and cell.content == CellContent.EMPTY:
                                cell.click()
            color2column_components = get_connected_components(list(self.color_groups.values()), CellGroup.groups_sharing_column)
            for component in color2column_components:
                mapped_component = set().union(*(color_group.optional_columns() for color_group in component))
                if len(mapped_component) == len(component):
                    for column_index in mapped_component:
                        row = self.columns[column_index]
                        for cell in row.cells:
                            if cell.color not in component and cell.content == CellContent.EMPTY:
                                cell.click()



if __name__ == '__main__':
    queens_parser = QueensParser()
    queens_game = QueensSolver2(queens_parser)
    queens_game.solve()