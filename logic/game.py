from typing import Optional
from errors import CellOccupiedError
from models.board import NonOverlappingBoard, BoardView
from models.chips import BoardChip
from models.player import Player, Human, Computer
from logic.judge import BoardJudge


class TicTacToe:
    def __init__(self) -> None:
        self.initialize()

    @property
    def board(self) -> BoardView:
        return self._board.get_view()

    def initialize(self) -> None:
        self._board = NonOverlappingBoard(3, 3)
        self._human = Human(self._board.get_view(), BoardChip.X)
        self._computer = Computer(self._board.get_view(), BoardChip.O)

    def set_human_placement(self, x: int, y: int) -> None:
        """Allows for an external interface to set a pair
        of coordinates for the human chip"""
        if self._board.get(x, y) != BoardChip.EMPTY:
            raise CellOccupiedError
        self._human.selected_x, self._human.selected_y = x, y

    def are_valid_coords(self, x: int, y: int) -> bool:
        """Returns True if the given coordinates are both
        within the bounds of the board and is unoccupied"""
        try:
            return self._board.get(x, y) == BoardChip.EMPTY
        except IndexError:
            return False

    def place_chips(self) -> None:
        """Places chips of each player on board,
        
        Raises CellOccupiedError if either player tries to place a chip
        on an already played on cell"""
        for player in [self._human, self._computer]:
            self._board.set(*player.get_chip_placement(), player.chip)
            if self.is_game_over():
                return

    def get_winner(self) -> Optional[Player]:
        """Returns the player who has three consecutive chips
        in a row on the board (can be a row, column, or diagonal)
        
        Returns None if there is no winner"""
        winning_chip = BoardJudge.get_winning_chip(self._board)
        if winning_chip == BoardChip.EMPTY:
            return None
        
        for player in [self._human, self._computer]:
            if player.chip == winning_chip:
                return player

    def is_game_over(self) -> bool:
        return self._board.is_full() or self.get_winner() is not None