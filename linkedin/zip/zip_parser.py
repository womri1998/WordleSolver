import time
from math import sqrt
from pathlib import Path
import sys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By

sys.path.append(str(Path(__file__).resolve().parents[2]))
from linkedin.base import BaseParser


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

    def do_step(self, row: int, column: int):
        self.cells[row][column].click()
