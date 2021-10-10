from logic.game import TicTacToe
from ui.cli import CommandLineInterface
from ui.ui import UserInterface


def main(ui: UserInterface):
    ui.start()


if __name__ == '__main__':
    main(CommandLineInterface(TicTacToe()))