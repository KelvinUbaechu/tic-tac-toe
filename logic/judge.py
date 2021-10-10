from typing import Sequence
from models.board import Board
from models.chips import BoardChip


class BoardJudge:
    @staticmethod
    def _get_chip_winning_line(line: Sequence[BoardChip]) -> BoardChip:
        """If the sequence only contains one unique chip, that chip is returned.
        Otherwise, it returns an empty chip.
        
        The sequence should represent a single straight line of chips from the board."""
        unique_chips = set(line)
        if BoardChip.EMPTY in unique_chips or len(unique_chips) != 1:
            return BoardChip.EMPTY
        return unique_chips.pop()

    @staticmethod
    def _get_chip_winning_row(board: Board) -> BoardChip:
        """If there is a row that contains only one unique chip, it returns that chip.
        Otherwise, return an empty chip"""
        for i in range(board.height):
            winning_chip = BoardJudge._get_chip_winning_line(board.get_row(i))
            if winning_chip != BoardChip.EMPTY:
                return winning_chip
        return BoardChip.EMPTY

    @staticmethod
    def _get_chip_winning_col(board: Board) -> BoardChip:
        """If there is a column that contains only one unique chip, it returns that chip.
        Otherwise, return an empty chip"""
        for i in range(board.width):
            winning_chip = BoardJudge._get_chip_winning_line(board.get_col(i))
            if winning_chip != BoardChip.EMPTY:
                return winning_chip
        return BoardChip.EMPTY

    @staticmethod
    def _get_chip_winning_diagonal(board: Board) -> BoardChip:
        """If there is a diagonal that contains only one unique chip, it returns that chip.
        Otherwise, it returns an empty chip"""
        winning_chip = BoardJudge._get_chip_winning_line(board.get_left_diagonal(0, 0))
        if winning_chip != BoardChip.EMPTY:
            return winning_chip
        return BoardJudge._get_chip_winning_line(board.get_right_diagonal(board.width - 1, 0))

    @staticmethod
    def get_winning_chip(board: Board) -> BoardChip:
        """Returns that chip that forms a line three elements long, if there is one.
        Otherwise, it returns an empty chip"""
        chip_winner_checkers = [
            BoardJudge._get_chip_winning_row,
            BoardJudge._get_chip_winning_col,
            BoardJudge._get_chip_winning_diagonal
        ]

        for checker in chip_winner_checkers:
            winning_chip = checker(board)
            if winning_chip != BoardChip.EMPTY:
                return winning_chip
        return BoardChip.EMPTY