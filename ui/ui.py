from abc import ABC, abstractmethod
from logic.game import TicTacToe


class UserInterface(ABC):
    """An interface for ui that plays Tic-Tac-Toe"""
    def __init__(self, game: TicTacToe) -> None:
        self._game = game

    @abstractmethod
    def start(self) -> None:
        """Starts up the user interface with the game"""
        raise NotImplementedError