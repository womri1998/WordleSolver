import time
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.remote.webelement import WebElement


class TangoParser:
    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.debugger_address = "127.0.0.1:9222"
        self.driver: WebDriver = webdriver.Chrome(
            service=Service(),
            options=chrome_options
        )
        self.driver.get("https://www.linkedin.com/games/view/tango/desktop")  # This is the actual page to parse the data from the original https://www.linkedin.com/games/tango
        time.sleep(2)
        self.driver.find_element(By.CLASS_NAME, "artdeco-button--4").click()
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
