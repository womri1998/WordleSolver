import time
from math import sqrt
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.remote.webelement import WebElement


class QueensParser:
    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.debugger_address = "127.0.0.1:9222"
        self.driver: WebDriver = webdriver.Chrome(
            service=Service(),
            options=chrome_options
        )
        self.driver.get("https://www.linkedin.com/games/view/queens/desktop")  # This is the actual page to parse the data from the original https://www.linkedin.com/games/queens
        time.sleep(2)
        self.driver.find_element(By.CLASS_NAME, "artdeco-button--4").click()
        self.cells: list[list[WebElement]] | None = None
        self.size: int | None = None

    def load_cells(self):
        cell_elements = self.driver.find_elements(By.CLASS_NAME, 'queens-cell-with-border')
        self.size = round(sqrt(len(cell_elements)))
        self.cells: list[list[WebElement]] = [cell_elements[i:i + self.size] for i in range(0, self.size ** 2, self.size)]

    def dump_cells(self) -> list[list[tuple[str, str, WebElement]]]:
        self.load_cells()
        raw_game = []
        for row_index, row_elements in enumerate(self.cells):
            row = []
            for column_index, cell in enumerate(row_elements):
                aria_label = cell.get_attribute("aria-label").split()
                content = aria_label[0]
                color_aria_index = aria_label.index('color')
                row_aria_index = aria_label.index('row')
                color = ''.join(aria_label[color_aria_index + 1: row_aria_index]).strip(',')
                assert row_index + 1 == int(aria_label[-3].strip(','))
                assert column_index + 1 == int(aria_label[-1])
                row.append((content.lower(), color, cell))
            raw_game.append(row)
        return raw_game

    def assign_cross(self, row: int, column: int):
        self.cells[row][column].click()

    def assign_queen(self, row: int, column: int):
        self.cells[row][column].click()
        self.cells[row][column].click()
