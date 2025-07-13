import requests
from english_words import english_words_lower_alpha_set
from string import ascii_uppercase

from wordle.word_fetchers.word_fetcher import WordFetcher


WORDS_ALPHA_URL = "https://raw.githubusercontent.com/dwyl/english-words/master/words_alpha.txt"


class EnglishFetcher(WordFetcher):
    def __init__(self, length: int):
        super().__init__(length, ascii_uppercase)

    def get_words(self) -> set[str]:
        all_words = set()
        all_words.update(english_words_lower_alpha_set)
        all_words.update(set(requests.get(WORDS_ALPHA_URL).text.splitlines()))
        return {word.upper() for word in all_words}
