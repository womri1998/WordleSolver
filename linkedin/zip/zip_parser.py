import time
from math import sqrt
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By

from ..base import BaseParser


class ZipParser(BaseParser):
    def __init__(self):
        super().__init__("zip")
        time.sleep(2)
        self.cells: list[list[WebElement]] | None = None
        self.size = None

    def load_cells(self):
        cell_elements = self.driver.find_elements(By.CLASS_NAME, 'trail-cell')
        self.size = round(sqrt(len(cell_elements)))
        self.cells: list[list[WebElement]] = [
            cell_elements[i:i + self.size] for i in range(0, self.size ** 2, self.size)
        ]

    def dump_cells(self) -> list[list[int | None]]:
        self.load_cells()
        raw_game = []
        for row_elements in self.cells:
            row = []
            for cell in row_elements:
                try:
                    content_element = cell.find_element(By.CLASS_NAME, 'trail-cell-content')
                    content_value = int(content_element.text)
                except Exception:
                    content_value = None
                row.append(content_value)
            raw_game.append(row)
        return raw_game

    def extract_walls(self, cell: WebElement) -> tuple[bool, bool]:
        """Return which walls are present for the given cell.

        Only ``right`` and ``down`` walls are parsed to avoid
        duplication.  The walls are detected by looking for elements
        with the ``trail-cell-wall`` class and the directional
        subclass ``trail-cell-wall-<direction>``.
        """
        right_wall = False
        down_wall = False
        for wall in cell.find_elements(By.CLASS_NAME, "trail-cell-wall"):
            classes = wall.get_attribute("class").split()
            if "trail-cell-wall-right" in classes:
                right_wall = True
            if "trail-cell-wall-down" in classes:
                down_wall = True
        return down_wall, right_wall

    def dump_cells_with_walls(self) -> list[list[tuple[int | None, bool, bool]]]:
        """Dump the board state including wall information."""
        self.load_cells()
        board = []
        for row_elements in self.cells:
            row = []
            for cell in row_elements:
                try:
                    content_element = cell.find_element(By.CLASS_NAME, "trail-cell-content")
                    content_value = int(content_element.text)
                except Exception:
                    content_value = None
                down_wall, right_wall = self.extract_walls(cell)
                row.append((content_value, down_wall, right_wall))
            board.append(row)
        return board

    def do_step(self, row: int, column: int):
        self.cells[row][column].click()
