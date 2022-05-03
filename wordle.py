from enum import Enum
from string import ascii_lowercase

from word_initializers.english_words_initilalizer import EnglishWords

WORDS_LENGTH = 5


class Languages(Enum):
    ENGLISH = EnglishWords


class Keyboard:
    def __init__(self, words_length: int, language: str):
        self.words_length = words_length
        self.all_words = Languages[language].value.get_words()
        self.keys = None
        self.must_haves = None
        self.reset()

    def reset(self):
        self.keys = {letter: {i for i in range(self.words_length)} for letter in ascii_lowercase}
        self.must_haves = set()  # each character points to the number of times it could occur.

    def green_letter(self, letter: str, index: int):
        self.must_haves.add(letter)
        self.keys[letter] = {index}

    def yellow_letter(self, letter: str, index: int):
        self.must_haves.add(letter)
        self.keys[letter].discard(index)

    def black_letter(self, letter: str, index: int):
        self.keys[letter] = set()

    def update_letter(self, letter: str, indices: dict[int, str]):
        """
        :param letter: the letter we update
        :param indices: a mapping between index in which it was inserted to the color it has.
        """
        pass

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
                        self.green_letter(letter, index)
                    case 'Y':
                        self.yellow_letter(letter, index)
                    case 'B':
                        self.black_letter(letter, index)
            return False

    def possible_words(self):
        return [word for word in self.all_words if word in self]

    def completely_new_words(self):
        return [word for word in self.all_words if len(set(word)) == self.words_length and
                all([self.keys[letter] == {i for i in range(self.words_length)} for letter in word])]

    def __contains__(self, item: str) -> bool:
        return self.valid_word(word=item)
