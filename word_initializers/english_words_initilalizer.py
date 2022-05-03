from nltk.corpus import words
from english_words import english_words_lower_alpha_set
from json import loads

from word_initializers.word_initializer import WordInitializer


class EnglishWords(WordInitializer):
    def get_words(self) -> set[str]:
        all_words = set()
        all_words.update(english_words_lower_alpha_set)
        all_words.update(self._nltk_words())
        all_words.update(self._words_alpha())
        return all_words

    @staticmethod
    def _nltk_words() -> set[str]:
        return set([word.lower() for word in words.words()])

    @staticmethod
    def _words_alpha() -> set[str]:
        with open("word_initializers/english_data/words_dictionary.json", 'r') as f:
            words_dictionary = loads(f.read())
            return set(words_dictionary.keys())
