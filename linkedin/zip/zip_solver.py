from .zip_parser import ZipParser


class ZipSolver:
    def __init__(self, parser: ZipParser):
        self.parser = parser
        self.parser.load_cells()
        # include wall information when parsing the board
        board_data = self.parser.dump_cells_with_walls()
        self.size = len(board_data)

        # store numeric values separate from wall locations
        self.board: list[list[int | None]] = []
        self.right_walls: list[list[bool]] = []  # walls between (r,c) and (r,c+1)
        self.down_walls: list[list[bool]] = []   # walls between (r,c) and (r+1,c)

        for r, row_data in enumerate(board_data):
            values_row = []
            right_row = []
            for c, (value, down, right) in enumerate(row_data):
                values_row.append(value)
                if c < self.size - 1:
                    right_row.append(right)
            self.board.append(values_row)
            self.right_walls.append(right_row)

        for r in range(self.size - 1):
            down_row = []
            for c in range(self.size):
                down_row.append(board_data[r][c][1])
            self.down_walls.append(down_row)

    def find_solution(self) -> list[tuple[int, int]]:
        """
        Finds the solution path starting from the '1' labeled cell,
        moving in single horizontal/vertical steps, crossing all
        cells exactly once, and passing through numbers in order.
        """

        total_cells = self.size * self.size

        # Find the starting cell that is labeled '1'
        start = None
        for r in range(self.size):
            for c in range(self.size):
                if self.board[r][c] == 1:
                    start = (r, c)
                    break
            if start:
                break

        if start is None:
            raise ValueError("No starting cell '1' found in the board.")

        # path will track the current move sequence
        path: list[tuple[int, int]] = []
        visited: set[tuple[int, int]] = set()

        # The DFS function tries to find a Hamiltonian path while ensuring that if a cell
        # contains a number it must come in the right order.
        def dfs(row: int, column: int, last_number: int) -> bool:
            # If we have visited every cell, we've found a solution.
            if len(path) == total_cells:
                return True

            # Neighbors: right, down, left, up (order can be tuned for performance)
            for delta_r, delta_c in ((0, 1), (1, 0), (0, -1), (-1, 0)):
                new_r, new_c = row + delta_r, column + delta_c

                # Skip if out of bounds or already visited.
                if not (0 <= new_r < self.size and 0 <= new_c < self.size):
                    continue
                if (new_r, new_c) in visited:
                    continue

                # check for walls blocking the movement
                blocked = False
                if delta_r == 0 and delta_c == 1:
                    if self.right_walls[row][column]:
                        blocked = True
                elif delta_r == 0 and delta_c == -1:
                    if self.right_walls[row][column - 1]:
                        blocked = True
                elif delta_r == 1 and delta_c == 0:
                    if self.down_walls[row][column]:
                        blocked = True
                elif delta_r == -1 and delta_c == 0:
                    if self.down_walls[row - 1][column]:
                        blocked = True
                if blocked:
                    continue

                cell_val = self.board[new_r][new_c]
                new_last = last_number

                # If the neighbor cell contains a digit then enforce ordering.
                if isinstance(cell_val, int):
                    num = cell_val
                    # The next expected numbered cell should be last_number+1.
                    # If the found number is greater than that, then we are skipping a required number.
                    if num > last_number + 1:
                        continue
                    # If the neighbor is the next number (last_number+1) then update new_last.
                    if num == last_number + 1:
                        new_last = num
                    # If it equals last_number (which, aside from the starting cell, should not happen)
                    # we can still allow it but often boards contain each number only once.
                # Mark the move and continue the DFS.
                visited.add((new_r, new_c))
                path.append((new_r, new_c))
                if dfs(new_r, new_c, new_last):
                    return True
                # Backtrack since no valid path was found from the neighbor.
                path.pop()
                visited.remove((new_r, new_c))
            return False

        # Initialize with the starting cell.
        visited.add(start)
        path.append(start)
        # Set initial number based on the starting cell value.
        start_value = self.board[start[0]][start[1]]
        initial_number = start_value if isinstance(start_value, int) else 0

        if dfs(start[0], start[1], initial_number):
            return path
        else:
            raise ValueError("No valid solution path found.")

    def solve(self):
        path = self.find_solution()
        for row, col in path:
            self.parser.do_step(row, col)


if __name__ == '__main__':
    zip_parser = ZipParser()
    zip_game = ZipSolver(zip_parser)
    zip_game.solve()