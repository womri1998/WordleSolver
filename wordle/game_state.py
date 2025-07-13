from pydantic import BaseModel

RESET = "\033[0m"
COLOR_MAP = {
    "green": "\033[42m",  # Green background
    "yellow": "\033[43m",  # Yellow background
    "gray": "\033[100m",  # Gray background
    "unknown": "\033[100m"  # Default to gray
}


class Cell(BaseModel):
    letter: str
    color: str


class Row(BaseModel):
    cells: list[Cell]

    def print(self):
        print("".join(f"{COLOR_MAP[cell.color]} {cell.letter} {RESET}" for cell in self.cells))

    def is_correct(self) -> bool:
        return all(cell.color == "green" for cell in self.cells)


class Board(BaseModel):
    rows: list[Row]

    def print(self):
        for row in self.rows:
            row.print()

    def is_correct(self) -> bool:
        return self.rows[-1].is_correct()


class GameBoard(BaseModel):
    boards: list[Board]

    def print(self):
        for i, board in enumerate(self.boards):
            print(f"Board {i + 1}:")
            board.print()
            print()
