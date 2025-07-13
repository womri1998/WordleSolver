import time
from math import sqrt

from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.remote.webelement import WebElement


class ZipParser:
    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.debugger_address = "127.0.0.1:9222"
        self.driver: WebDriver = webdriver.Chrome(
            service=Service(),
            options=chrome_options
        )
        self.driver.get("https://www.linkedin.com/games/view/zip/desktop")  # This is the actual page to parse the data from the original https://www.linkedin.com/games/zip
        time.sleep(2)
        self.driver.find_element(By.CLASS_NAME, "artdeco-button--4").click()
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
