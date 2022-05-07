from .wordle_solver import WordleSolver


class MultiSolver:
    def __init__(self, keyboard_count: int, words_length: int, language: str):
        self.solvers: list[WordleSolver] = [WordleSolver(words_length, language) for _ in range(keyboard_count)]

    def reset(self):
        for solver in self.solvers:
            solver.reset()

    def valid_word(self, index: int, word: str) -> bool:
        return self.solvers[index].valid_word(word)

    def guess_word(self, word: str, colors: list[str]):
        for wordle_solver, color_list in zip(self.solvers, colors):
            wordle_solver.guess_word(word, color_list)

    def possible_solutions(self, index: int) -> set[str]:
        return self.solvers[index].possible_solutions()

    def get_most_option_reducing_words(self) -> tuple[int, list[str]]:
        return self.solvers[0].get_most_option_reducing_words()
