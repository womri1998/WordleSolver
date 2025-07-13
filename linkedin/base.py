GAME_URL_TEMPLATE = "https://www.linkedin.com/games/view/{game_name}/desktop"

import time
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service


class BaseParser:
    def __init__(self, game_name: str):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.debugger_address = "127.0.0.1:9222"
        self.driver: WebDriver = webdriver.Chrome(
            service=Service(),
            options=chrome_options,
        )
        self.driver.get(GAME_URL_TEMPLATE.format(game_name=game_name))
        time.sleep(2)
        self.driver.find_element(By.CLASS_NAME, "artdeco-button--4").click()
