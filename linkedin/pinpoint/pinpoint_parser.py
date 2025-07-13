import os
import sys
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from general_parser import GeneralParser


class PinpointParser(GeneralParser):
    def __init__(self):
        super().__init__("pinpoint")
        self.cards: list[WebElement] | None = None

    def load_cards(self):
        self.cards = []
        for i in range(5):
            card = self.driver.find_element(By.CLASS_NAME, f"pinpoint__card__{i}")
            inner = card.find_element(By.CLASS_NAME, "pinpoint__card__inner")
            card_element = inner.find_element(By.CLASS_NAME, "pinpoint__card")
            self.cards.append(card_element)

    def dump_clues(self) -> list[str | None]:
        self.load_cards()
        clues: list[str | None] = []
        for card in self.cards:
            try:
                span = card.find_element(By.TAG_NAME, "span")
                text = span.text.strip()
                clues.append(text if text else None)
            except Exception:
                clues.append(None)
        return clues

    def submit_guess(self, guess: str):
        body = self.driver.find_element(By.TAG_NAME, "body")
        body.send_keys(guess)
        body.send_keys(Keys.RETURN)
        time.sleep(1)
