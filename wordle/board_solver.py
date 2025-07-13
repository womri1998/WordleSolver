from collections import defaultdict
from wordle.game_state import Row, Board


class BoardSolver:
    def __init__(self, all_words: set[str]):
        self.all_words = all_words
        self.relevant_words = list(all_words)

    def position_filter(self, greens: dict[int, str], yellows: dict[int, list[str]]):
        for position, letter in greens.items():
            self.relevant_words = [word for word in self.relevant_words if word[position] == letter]
        for position, letters in yellows.items():
            for letter in letters:
                self.relevant_words = [word for word in self.relevant_words if letter in word and word[position] != letter]

    def count_filter(self, greens: dict[int, str], yellows: dict[int, list[str]], grays: set[str]):
        letter_lower_constraints = defaultdict(lambda: 0)
        letter_upper_constraints = defaultdict(lambda: 0)
        for position, letter in greens.items():
            letter_lower_constraints[letter] += 1
        for position, letters in yellows.items():
            for letter in letters:
                letter_lower_constraints[letter] += 1
        for letter in grays:
            letter_upper_constraints[letter] = letter_lower_constraints[letter] + 1
        for letter, min_count in letter_lower_constraints.items():
            self.relevant_words = [word for word in self.relevant_words if word.count(letter) >= min_count]
        for letter, max_count in letter_upper_constraints.items():
            self.relevant_words = [word for word in self.relevant_words if word.count(letter) < max_count]

    def parse_row(self, row: Row):
        greens = {}
        yellows = {}
        grays = set()
        letter_counts = {}
        for i, cell in enumerate(row.cells):
            letter = cell.letter
            letter_counts[letter] = letter_counts.get(letter, 0) + 1
            if cell.color == "green":
                greens[i] = letter
            elif cell.color == "yellow":
                yellows.setdefault(i, []).append(letter)
            elif cell.color == "gray":
                grays.add(letter)
        return greens, yellows, grays

    def insert_guess(self, guess: Row):
        greens, yellows, grays = self.parse_row(guess)
        self.position_filter(greens, yellows)
        self.count_filter(greens, yellows, grays)

    def possible_guesses(self, board: Board) -> list[str]:
        self.relevant_words = list(self.all_words)
        for row in board.rows:
            self.insert_guess(row)
        return self.relevant_words