from abc import ABCMeta, abstractmethod


class WordInitializer(metaclass=ABCMeta):
    @abstractmethod
    def get_words(self) -> set[str]:
        pass
