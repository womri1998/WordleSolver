from bs4 import BeautifulSoup

from wordle.game_state import Cell, Row, Board, GameBoard


def get_cell_color(cell):
    if cell['aria-label'].endswith('is correct'):
        return 'green'
    elif cell['aria-label'].endswith('is in a different spot'):
        return 'yellow'
    elif cell['aria-label'].endswith('is incorrect'):
        return 'gray'
    raise ValueError("What color is this?")


def get_game_board(octordle_html: BeautifulSoup) -> GameBoard:
    boards = []
    board_elements = octordle_html.find_all("div", attrs={"class": "board"})
    for board_element in board_elements:
        rows = []
        row_elements = [
            row for row in board_element.find_all("div", attrs={"class": "board-row"})
            if "Guess" in row['aria-label'] and "Guess ." not in row['aria-label']
        ]
        for row_element in row_elements:
            cell_elements = row_element.find_all("div", attrs={"role": "cell"})
            cells = [
                Cell(
                    letter=cell['aria-label'][1],
                    color=get_cell_color(cell)
                ) for cell in cell_elements
            ]
            rows.append(Row(cells=cells))
        boards.append(Board(rows=rows))
    return GameBoard(boards=boards)


def is_current_guess_valid(octordle_html: BeautifulSoup) -> bool:
    board_elements = octordle_html.find_all("div", attrs={"class": "board"})
    for board_element in board_elements:
        row_elements = [
            row for row in board_element.find_all("div", attrs={"class": "board-row"})
            if "Current guess" in row['aria-label']
        ]
        for row_element in row_elements:
            cell_elements = row_element.find_all("div", attrs={"role": "cell", "class": "invalid-word"})
            if len(cell_elements) != 0:
                return False
    return True
