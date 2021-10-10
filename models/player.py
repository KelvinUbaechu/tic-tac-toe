from abc import ABC, abstractmethod
from random import choice
from models.board import Board
from models.chips import BoardChip


class Player(ABC):
    """An abstract base class representing a player of Tic Tac Toe"""
    def __init__(self, board: Board, chip: BoardChip) -> None:
        self._board = board
        self._chip = chip

    @property
    def chip(self) -> BoardChip:
        return self._chip

    @abstractmethod
    def get_chip_placement(self) -> tuple[int, int]:
        """Returns the coordinates of desired place for chip"""
        pass

    def __repr__(self) -> str:
        return self.__class__.__name__


class Human(Player):
    """A Player where the desired coordinates of where to place its chip
    on the board can be decided by a human user, through an interface"""
    def __init__(self, board: Board, chip: BoardChip) -> None:
        super().__init__(board, chip)
        self.selected_x = self.selected_y = 0

    @property
    def selected_x(self) -> int:
        return self._selected_x

    @selected_x.setter
    def selected_x(self, new_x) -> None:
        if not isinstance(new_x, int):
            raise TypeError(f'can only set to non-negative integer')
        elif new_x < 0 or new_x >= self._board.width:
            raise ValueError(f'{new_x} is out of bounds of board')
        self._selected_x = new_x

    @property
    def selected_y(self) -> int:
        return self._selected_y

    @selected_y.setter
    def selected_y(self, new_y) -> None:
        if not isinstance(new_y, int):
            raise TypeError(f'can only set to non-negative integer')
        elif new_y < 0 or new_y >= self._board.height:
            raise ValueError(f'{new_y} is out of bounds of board')
        self._selected_y = new_y

    def get_chip_placement(self) -> tuple[int, int]:
        return (self.selected_x, self.selected_y)


class Computer(Player):
    """A Player that places its chips in a random empty cell of the board"""
    def _get_available_placements(self) -> list[tuple[int, int]]:
        placements = []
        for x in range(self._board.width):
            for y in range(self._board.height):
                if self._board.get(x, y) == BoardChip.EMPTY:
                    placements.append((x, y))
        return placements

    def get_chip_placement(self) -> tuple[int, int]:
        return choice(self._get_available_placements())