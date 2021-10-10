from errors import CellOccupiedError
from models.chips import BoardChip


class Board:
    """A 2D board of BoardChips"""
    def __init__(self, width: int, height: int):
        self._width = width
        self._height = height
        self._cells = [[BoardChip.EMPTY] * width for _ in range(height)]

    @property
    def width(self) -> int:
        return self._width

    @property
    def height(self) -> int:
        return self._height

    def get(self, x: int, y: int) -> BoardChip:
        return self._cells[y][x]

    def get_row(self, y: int) -> list[BoardChip]:
        return [self.get(i, y) for i in range(self.width)]

    def get_col(self, x: int) -> list[BoardChip]:
        return [self.get(x, i) for i in range(self.height)]

    def get_left_diagonal(self, x: int, y: int) -> list[BoardChip]:
        """Returns the chips that are contained by the diagonal
        that goes down and right to the end of the board starting at
        the given coordinates"""
        diagonal = []
        cur_x, cur_y = x, y

        while cur_x < self.width and cur_y < self.height:
            diagonal.append(self.get(cur_x, cur_y))
            cur_x += 1
            cur_y += 1
        return diagonal

    def get_right_diagonal(self, x: int, y: int) -> list[BoardChip]:
        """Returns the chips that are contained by the diagonal
        that goes down and left to the end of the board starting at
        the given coordinates"""
        diagonal = []
        cur_x, cur_y = x, y

        while cur_x >= 0 and cur_y < self.height:
            diagonal.append(self.get(cur_x, cur_y))
            cur_x -= 1
            cur_y += 1
        return diagonal

    def set(self, x: int, y: int, chip: BoardChip) -> None:
        if not isinstance(chip, BoardChip):
            raise TypeError('can only add chips to board')
        self._cells[y][x] = chip

    def delete(self, x: int, y: int) -> None:
        """Replaces the chip in this cell with an empty chip"""
        self._cells[y][x] = BoardChip.EMPTY

    def clear_row(self, y: int) -> None:
        """Replaces all chips in this row with empty chips"""
        for x in range(self.width):
            self.delete(x, y)

    def clear_col(self, x: int) -> None:
        """Replaces all chips in this column with empty chips"""
        for y in range(self.height):
            self.delete(x, y)

    def clear(self) -> None:
        """Replaces all chips in the board with empty chips"""
        for x in range(self.width):
            for y in range(self.height):
                self.delete(x, y)

    def is_full(self) -> bool:
        # Iterate through entire board to find an empty chip
        # If one is found return False, else return True
        for i in range(self.height):
            for chip in self.get_row(i):
                if chip == BoardChip.EMPTY:
                    return False
        return True

    def is_empty(self) -> bool:
        # Iterate through entire board to find a non-empty chip
        # If one is found return False, else return True
        for i in range(self.height):
            for chip in self.get_row(i):
                if chip != BoardChip.EMPTY:
                    return False
        return True

    def get_view(self) -> 'BoardView':
        return BoardView(self)

    def __repr__(self) -> str:
        return f'Board(width={self.width}, height={self.height})'

    def __str__(self) -> str:
        return '\n'.join(str(self.get_row(y)) for y in range(self.height))


class NonOverlappingBoard(Board):
    """A board where non-empty cells cannot be set to another chip
    without first removing the chip within the cells"""
    def set(self, x: int, y: int, chip: BoardChip) -> None:
        if self.get(x, y) != BoardChip.EMPTY:
            raise CellOccupiedError(f'{x, y} is occupied')
        return super().set(x, y, chip)

    def __repr__(self) -> str:
        return f'NonOverlappingBoard(width={self.width}, height={self.height})'


class BoardView(Board):
    """An unmodifiable view of a board"""
    def __init__(self, board: Board):
        self._board = board

    @property
    def width(self) -> int:
        return self._board.width

    @property
    def height(self) -> int:
        return self._board.height

    def get(self, x: int, y: int) -> BoardChip:
        return self._board.get(x, y)

    def set(self, x: int, y: int, chip: BoardChip) -> None:
        raise NotImplementedError('cannot modify BoardView')

    def delete(self, x: int, y: int) -> None:
        raise NotImplementedError('cannot modify BoardView')

    def __repr__(self) -> str:
        return f'BoardView(board={self._board!r})'

    def __str__(self) -> str:
        return str(self._board)