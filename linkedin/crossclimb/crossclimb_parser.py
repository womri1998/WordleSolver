from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from ..base import BaseParser


class CrossClimbParser(BaseParser):
    def __init__(self):
        super().__init__("crossclimb")
        self.guess_elements: dict[int, WebElement] = {}
        for element in self.driver.find_elements(By.CLASS_NAME, "crossclimb__guess"):
            guess_id = int(element.get_attribute("data-guess-id"))
            self.guess_elements[guess_id] = element

    def get_guess_length(self, guess_id: int) -> int:
        element = self.guess_elements[guess_id]
        return len(element.find_elements(By.CLASS_NAME, "crossclimb__guess_box"))

    def get_clue(self, guess_id: int) -> str:
        element = self.guess_elements[guess_id]
        element.find_element(By.CLASS_NAME, "crossclimb__guess__inner").click()
        clue_el = self.driver.find_element(By.CLASS_NAME, "crossclimb__clue")
        return clue_el.text.strip()

    def submit_guess(self, guess_id: int, word: str):
        element = self.guess_elements[guess_id]
        input_el = element.find_element(By.CLASS_NAME, "crossclimb__guess__inner")
        input_el.click()
        input_el.send_keys(word)
