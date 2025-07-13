import time
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


class GeneralParser:
    """Shared setup for LinkedIn games using Selenium."""

    def __init__(self, game_slug: str):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.debugger_address = "127.0.0.1:9222"
        self.driver: WebDriver = webdriver.Chrome(service=Service(), options=chrome_options)
        self.driver.get(f"https://www.linkedin.com/games/view/{game_slug}/desktop")
        time.sleep(2)
        try:
            self.driver.find_element(By.CLASS_NAME, "artdeco-button--4").click()
            time.sleep(2)
        except Exception:
            pass

