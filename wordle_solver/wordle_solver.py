from enum import Enum
from string import ascii_lowercase
from itertools import groupby

from .word_initializers.english_words_initilalizer import EnglishWords

WORDS_LENGTH = 5


class Languages(Enum):
    ENGLISH = EnglishWords


class WordleSolver:
    def __init__(self, words_length: int, language: str):
        self.words_length = words_length
        self.all_words = Languages[language].value(self.words_length).get_words()
        self.keys = None
        self.must_haves = None
        self.reset()

    def reset(self):
        self.keys = {letter: {i for i in range(self.words_length)} for letter in ascii_lowercase}
        self.must_haves = set()  # each character points to the number of times it could occur.

    def insert_green_letter(self, letter: str, index: int):
        self.must_haves.add(letter)
        self.keys[letter] = {index}

    def insert_yellow_letter(self, letter: str, index: int):
        self.must_haves.add(letter)
        self.keys[letter].discard(index)

    def insert_black_letter(self, letter: str, index: int):
        self.keys[letter] = set()

    def valid_word(self, word: str) -> bool:
        return all([index in self.keys[letter] for index, letter in enumerate(word)]) and \
               all([letter in word for letter in self.must_haves])

    def guess_word(self, word: str, colors: str) -> bool:
        if colors == 'G' * self.words_length:
            return True
        else:
            for index, (letter, color) in enumerate(zip(word, colors)):
                match color:
                    case 'G':
                        self.insert_green_letter(letter, index)
                    case 'Y':
                        self.insert_yellow_letter(letter, index)
                    case 'B':
                        self.insert_black_letter(letter, index)
            return False

    def possible_solutions(self):
        return [word for word in self.all_words if word in self]

    def uniqueness_score(self, word: str) -> int:
        return len(set(([c for c in word if c not in self.must_haves and self.keys[c] != set()])))

    def get_most_option_reducing_words(self) -> tuple[int, list[str]]:
        sorted_score_list = sorted([(self.uniqueness_score(word), word) for word in self.all_words], key=lambda pair: pair[0], reverse=True)
        return [(score, [word for score, word in group]) for score, group in groupby(sorted_score_list, lambda pair: pair[0])][0]

    def completely_new_words(self):
        return [word for word in self.all_words if len(set(word)) == self.words_length and
                all([self.keys[letter] == {i for i in range(self.words_length)} for letter in word])]

    def __contains__(self, item: str) -> bool:
        return self.valid_word(word=item)
