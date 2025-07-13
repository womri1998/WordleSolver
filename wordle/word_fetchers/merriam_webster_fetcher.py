import json
from string import ascii_lowercase, ascii_uppercase
from selenium.webdriver import ChromeOptions, Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

from wordle.word_fetchers.word_fetcher import WordFetcher


class MerriamWebsterFetcher(WordFetcher):
    def __init__(self):
        super().__init__(5, ascii_uppercase)
        chrome_options = ChromeOptions()
        chrome_options.debugger_address = "127.0.0.1:9222"
        self.driver = Chrome(
            service=Service(),
            options=chrome_options
        )

    def get_words_from_page(self, page_url: str) -> set[str]:
        self.driver.get(page_url)
        ul_element = self.driver.find_elements(By.CLASS_NAME, "paginated-list-results")[0]
        return {a_element.text.upper() for a_element in ul_element.find_elements(By.TAG_NAME, "a")}

    def get_words_by_start(self, start_letter: str) -> set[str]:
        page_index = 1
        found_empty_page = False
        fetched_words = set()
        while not found_empty_page:
            page_url = f"https://www.merriam-webster.com/wordfinder/classic/begins/all/5/{start_letter}/{page_index}"
            new_words = self.get_words_from_page(page_url)
            if len(new_words) == 0:
                found_empty_page = True
            fetched_words.update(new_words)
            page_index += 1
        return fetched_words

    def get_words(self) -> set[str]:
        all_words = set()
        for letter in ascii_lowercase:
            all_words.update(self.get_words_by_start(letter))
        return all_words

    @staticmethod
    def get_saved_words() -> set[str]:
        with open(r'/wordle\word_fetchers\merriam_webster.json') as f:
            all_words = json.load(f)
        return set(all_words)


if __name__ == '__main__':
    words = MerriamWebsterFetcher().get_words()
    with open('words.txt', 'w') as f:
        json.dump(words, f)
