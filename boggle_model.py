from typing import List, Tuple
import boggle_utils
import boggle_board_randomizer


class BoggleModel:
    _board: boggle_utils.BOARD_TYPE
    _words_list: boggle_utils.WORDS_TYPE
    _score: int  # User score
    _is_game_stopped: bool  # Indicates whether a round is over
    _timer: int  # Seconds left until round is over.
    _words_found_list: List[str]  # List of the words the legal words the user
    # have found.
    _current_display: str  # The current word the user is building.
    _cur_path: List[Tuple[int, int]]  # The path of the current word the user
    # is building.
    _message: str

    GAME_DURATION = 180  # In seconds

    BOARD_TYPE = List[List[str]]

    def __init__(self, board: List[List[str]]):
        self._board = board
        self._words_list = boggle_utils.load_words_list()
        self._reset_game(board)
        self._max_score_paths = boggle_utils.max_score_paths(
            self._board, self._words_list
        )

    def get_display(self) -> str:
        """
        Getter method to the current display data member.
        :return:
        """
        return self._current_display

    def get_words_list(self) -> boggle_utils.WORDS_TYPE:
        """
        Getter method to the words list of the current game.
        :return:
        """
        return self._words_list

    def get_words_found_list(self) -> List[str]:
        """
        Getter method for the legal words the user have already found.
        :return:
        """
        return self._words_found_list

    def get_current_path(self) -> boggle_utils.PATH_TYPE:
        """
        Getter method for the current path of the word the user is currently
        building.
        :return:
        """
        return self._cur_path

    def check_time(self) -> bool:
        """
        Checks if there is still time left.
        :return: True/False
        """
        if self._timer > 0:
            return True
        else:
            return False

    def get_time(self) -> str:
        """
        Returns time in minutes:seconds format while reducing the time left.
        :return:
        """
        if self._timer % 60 >= 10:
            return '{0}:{1}'.format(self._timer//60, self._timer%60)
        else:
            return '{0}:0{1}'.format(self._timer//60, self._timer%60)

    def get_timer(self) -> int:
        """
        Getter method returns how many seconds left until round is over.
        :return:
        """
        return self._timer

    def get_score(self) -> int:
        """
        Getter method for the user current score.
        :return:
        """
        return self._score

    def is_game_stopped(self) -> bool:
        """
        Getter method to tell has the game been stopped.
        :return:
        """
        return self._is_game_stopped

    def reduce_time(self) -> None:
        """
        Reduces the time by 1 second.
        :return:
        """
        self._timer -= 1

    def click(self, cell: Tuple[int, int]) -> bool:
        """
        Implement button click logic.
        :param cell: The cell the user has chosen.
        :return: True if the click process finished successfully, False
        otherwise.
        """
        cell_row, cell_col = cell
        letter = self._board[cell_row][cell_col]
        if letter.isalpha():
            return self._do_letter_clicked(letter, cell)
        else:
            raise ValueError("Unsupported type for letter click.")

    def _do_letter_clicked(self, letter: str, cell: Tuple[int, int]) -> bool:
        """
        Processes click process and returns True/False upon success or failure.
        :param letter: The letter appears on the button.
        :param cell: Coorsinatdd of the cell (x, y) - (row, column).
        :return: True upon success, False otherwise.
        """
        if (
                cell not in self._cur_path
                and (
                    len(self._cur_path) == 0
                    or (
                            abs(self._cur_path[-1][0] - cell[0]) <= 1
                            and abs(self._cur_path[-1][1] - cell[1]) <= 1
                    )
                )
        ):
            self._cur_letter = letter
            self._current_display += letter
            self._cur_path.append(cell)
            return True
        return False

    def do_submit(self) -> bool:
        """
        Handles submit process logic.
        :return: True upon success (no problems during submitting and word
        is valid), False otherwise.
        """
        is_path_valid = False
        word = boggle_utils.is_valid_path(self._board, self._cur_path,
                                        self._words_list)
        if word is not None and word not in self._words_found_list:
            self._score += len(self._cur_path) ** 2
            self._words_found_list.append(word)
            is_path_valid = True
        self._do_clear()
        return is_path_valid

    def _do_clear(self) -> None:
        """
        Clears the game state.
        :return:
        """
        self._cur_letter = ""
        self._current_display = ""
        self._cur_path = []

    def _reset_game(self, board: BOARD_TYPE) -> None:
        """
        Resets the game, handling new round logic.
        :param board: Board to initialize the game with.
        :return:
        """
        self._timer = self.GAME_DURATION
        self._score = 0
        self._is_game_stopped = True
        self._words_found_list = []
        self._board = board
        self._do_clear()

    def start_game(self) -> None:
        """
        Setter method for the _is_game_stopped data member.
        :return:
        """
        self._is_game_stopped = False

    def stop_game(self, board: BOARD_TYPE) -> None:
        """
        Stops and resest a currently runnig game / round.
        :param board:
        :return:
        """
        self._is_game_stopped = True
        self._reset_game(board)

    def max_score(self) -> int:
        """
        Returns the highest score can be possibly achieved in the board
        :return:
        """
        return sum(map(lambda path: len(path) ** 2, self._max_score_paths))

    def current_score_percentage(self) -> str:
        """
        Returns score/max possible score ratio in percentage.
        :return:
        """
        return "{:.2%}".format(self._score / self.max_score())
