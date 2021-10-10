from errors import CellOccupiedError
from ui.ui import UserInterface


class CommandLineInterface(UserInterface):
    """Allows user to play Tic-Tac-Toe via a command line interface"""
    def start(self) -> None:
        start_menu = ['Play', 'Quit']
        print('Welcome to Tic-Tac-Toe!')
        while True:
            self._display_menu(start_menu)
            command = input('Choose an option: ')
            match command:
                case '1':
                    self._game.initialize()
                    self._play()
                case '2':
                    break
                case _:
                    print('Invalid command')
            print()
        print('Goodbye!')
        
    def _play(self) -> None:
        play_menu = ['Place Chip', 'Quit']
        while not self._game.is_game_over():
            self._display_board()
            self._display_menu(play_menu)
            command = input('Choose an option: ')
            match command:
                case '1':
                    self._set_human_chip_placement()
                case '2':
                    break
                case _:
                    print('Invalid command')
            print()
        else:
            self._display_game_result()
        print('Thanks for playing!')

    def _set_human_chip_placement(self) -> None:
        print('Enter coordinates to indicate where you want to place your chip')
        while True:
            try:
                coords = self._get_coordinates_from_user()
                self._game.set_human_placement(*coords)
            except CellOccupiedError:
                print('That cell is occupied')
            except ValueError:
                print('Invalid coordinate')
            except IndexError:
                print('Those coordinates are out of bounds')
            else:
                self._game.place_chips()
                return
            
            answer = input('Would you like to try again? (y for yes): ').lower()
            if answer != 'y':
                break
        
    def _get_coordinates_from_user(self) -> tuple[int, int]:
        x = int(input('Enter x-coordinate: '))
        y = int(input('Enter y-coordinate: '))
        return x, y

    def _display_menu(self, menu: list[str]) -> None:
        for i, item in enumerate(menu, start=1):
            print(f'{i}) {item}')

    def _display_board(self) -> None:
        board = self._game.board
        border_width = 2 * board.width + 1
        board_str = '-' * border_width
        for i in range(board.height):
            board_str += '\n|' + '|'.join(map(str, board.get_row(i))) + '|'
            board_str += '\n' + '-' * border_width
        print(board_str)

    def _display_game_result(self) -> None:
        self._display_board()
        winner = self._game.get_winner()
        if winner:
            print(f'{winner} wins!')
        else:
            print("It's a tie!")