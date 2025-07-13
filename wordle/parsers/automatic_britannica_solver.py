import itertools
import json
import time
from collections import defaultdict
from random import choice
from string import ascii_uppercase
from tqdm import tqdm
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from wordle.game_state import GameBoard
from wordle.board_solver import BoardSolver
from wordle.parsers.brintannica_parser import get_game_board, is_current_guess_valid
from wordle.word_fetchers.merriam_webster_fetcher import MerriamWebsterFetcher


def init_driver() -> WebDriver:
    chrome_options = webdriver.ChromeOptions()
    chrome_options.debugger_address = "127.0.0.1:9222"
    driver = webdriver.Chrome(
        service=Service(),
        options=chrome_options
    )
    return driver


def get_current_game_board(driver: WebDriver) -> GameBoard:
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    return get_game_board(soup)


def find_input_box(driver: WebDriver) -> WebElement:
    return driver.find_element(By.TAG_NAME, 'body')


def insert_guess(input_box: WebElement, guess: str):
    input_box.send_keys(guess)
    input_box.send_keys(Keys.RETURN)


def get_best_guess(game_board: GameBoard, solver: BoardSolver) -> str:
    word_scores = defaultdict(int)
    for board in game_board.boards:
        if board.is_correct():
            continue
        current_options = solver.possible_guesses(board)
        for guess in current_options:
            word_scores[guess] += 1 / len(current_options)
    max_score = max(word_scores.values())
    best_options = [key for key, value in word_scores.items() if value == max_score]
    return choice(best_options)


def play_wordle():
    driver = init_driver()
    input_box = find_input_box(driver)
    all_words = EnglishFetcher(5).get_filtered_words()
    solver = BoardSolver(all_words)
    game_board = get_current_game_board(driver)
    while True:
        best_guess = get_best_guess(game_board, solver)
        insert_guess(input_box, best_guess)
        game_board = get_current_game_board(driver)
        if all(board.is_correct() for board in game_board.boards):
            print("Game solved!")
            break
        time.sleep(0.01)


def get_site_dict(driver: WebDriver) -> list[str]:
    # TOO SLOW
    valid_words = []
    input_box = find_input_box(driver)
    for raw_guess in tqdm(itertools.product(ascii_uppercase, repeat=5)):
        guess = "".join(raw_guess)
        input_box.send_keys(guess)
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        if is_current_guess_valid(soup):
            valid_words.append(guess)
        input_box.send_keys(Keys.BACKSPACE * 5)
    return valid_words



if __name__ == '__main__':
    play_wordle()