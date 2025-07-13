from pathlib import Path
import sys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By

sys.path.append(str(Path(__file__).resolve().parents[2]))
from linkedin.base import BaseParser


class TangoParser(BaseParser):
    def __init__(self):
        super().__init__("tango")
        self.cells: list[list[WebElement]] | None = None
        self.size = 6

    def load_cells(self):
        cell_elements = self.driver.find_elements(By.CLASS_NAME, 'lotka-cell')
        self.cells: list[list[WebElement]] = [cell_elements[i:i + self.size] for i in range(0, self.size ** 2, self.size)]

    def dump_cells(self) -> list[list[tuple[str, str, str]]]:
        self.load_cells()
        raw_game = []
        for row_index, row_elements in enumerate(self.cells):
            row = []
            for column_index, cell in enumerate(row_elements):
                svg_element = cell.find_element(By.TAG_NAME, 'svg')
                filling = svg_element.get_attribute('aria-label')
                if filling is None:
                    filling = "none"
                try:
                    down_edge = cell.find_element(By.CLASS_NAME, 'lotka-cell-edge--down')
                    down_edge_type = down_edge.find_element(By.TAG_NAME, 'svg').get_attribute('aria-label')
                except:
                    down_edge_type = "none"
                if down_edge_type is None:
                    down_edge_type = "none"
                try:
                    right_edge = cell.find_element(By.CLASS_NAME, 'lotka-cell-edge--right')
                    right_edge_type = right_edge.find_element(By.TAG_NAME, 'svg').get_attribute('aria-label')
                except:
                    right_edge_type = "none"
                if right_edge_type is None:
                    right_edge_type = "none"
                row.append((filling.lower(), down_edge_type.lower(), right_edge_type.lower()))
            raw_game.append(row)
        return raw_game

    def assign_sun(self, row: int, column: int):
        self.cells[row][column].click()

    def assign_moon(self, row: int, column: int):
        self.cells[row][column].click()
        self.cells[row][column].click()
