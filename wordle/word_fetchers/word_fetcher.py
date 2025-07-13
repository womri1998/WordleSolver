from abc import ABCMeta, abstractmethod


class WordFetcher(metaclass=ABCMeta):
    def __init__(self, length: int, strip: str):
        self.length = length
        self.strip = strip

    @abstractmethod
    def get_words(self) -> set[str]:
        pass

    def filter(self, all_words: set[str]) -> set[str]:
        return {word for word in all_words if len(word) == self.length and all([c in self.strip for c in word])}

    def get_filtered_words(self) -> set[str]:
        return self.filter(self.get_words())
