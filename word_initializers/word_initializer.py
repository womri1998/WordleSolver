from abc import ABCMeta, abstractmethod


class WordInitializer(metaclass=ABCMeta):
    def __init__(self, length: int):
        self.length = length

    @abstractmethod
    def get_words(self) -> set[str]:
        pass
