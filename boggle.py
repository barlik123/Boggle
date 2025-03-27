from typing import Callable, List
from boggle_gui import (
    BoggleGUI, COORDS_TYPE, SUBMIT_BUTTON_COORD,
    WRONG_WORD_BG, RIGHT_WORD_BG, ACTIVE_BUTTON_COLOR
)
from boggle_model import BoggleModel
from boggle_board_randomizer import randomize_board


class BoggleController:
    def __init__(self) -> None:
        board = randomize_board()
        self._gui = BoggleGUI(board)
        self._model = BoggleModel(board)
        for button in self._gui.get_buttons_info():
            action = self.create_button_action(button[1])
            self._gui.set_button_command(button[1], action)

    def create_button_action(self, button_cord: COORDS_TYPE
                             ) -> Callable[[], None]:
        """
        Method that create the actions of the button clicking, connecting
        the model actions and the gui display of the actions
        :param button_cord: the coodinates of the button that is making the
        action
        :return: Method that does the current action
        """
        def submit_func() -> None:
            """
            Method that does the action of when the submit button is clicked
            :return:
            """
            if self._model.is_game_stopped():
                self._model.start_game()
                self._gui.set_buttons_text()
                self.reduce_time()
            else:
                current_path: List[COORDS_TYPE] = self._model.get_current_path()
                is_submit_succeeded = self._model.do_submit()
                if is_submit_succeeded:
                    self._gui.set_buttons_color(
                        current_path, RIGHT_WORD_BG, is_submit=True
                    )
                else:
                    self._gui.set_buttons_color(
                        current_path, WRONG_WORD_BG, is_submit=True
                    )
            self._gui.set_display_cur(self._model.get_display())
            self._gui.set_display_used(self._model.get_words_found_list())
            self._gui.set_score_display(
                self._model.get_score(), self._model.current_score_percentage()
            )

        def letter_func() -> None:
            """
            Method that does the action of when a 'letter' button is clicked
            :return:
            """
            if self._model.is_game_stopped():
                self._model.start_game()
                self._gui.set_display_used(self._model.get_words_found_list())
                self._gui.set_buttons_text()
                self._gui.set_score_display(
                    self._model.get_score(),
                    self._model.current_score_percentage()
                )
                self.reduce_time()
            else:
                _is_success_click = self._model.click(button_cord)
                if _is_success_click:
                    self._gui.set_button_is_active(button_cord, True)
                    self._gui.set_buttons_color(self._model.get_current_path(),
                                                ACTIVE_BUTTON_COLOR,
                                                is_submit=False)
            self._gui.set_display_cur(self._model.get_display())

        if button_cord == SUBMIT_BUTTON_COORD:
            return submit_func
        return letter_func

    def reduce_time(self):
        """
        Method that reduces the time of the game and ends the current round
        of the game if the time hits 0
        :return:
        """
        self._gui.set_timer_display(self._model.get_time())
        if self._model.get_timer() > 0:
            self._model.reduce_time()
            self._gui.get_main_window().after(1000, self.reduce_time)
        else:
            self.reset_game()

    def reset_game(self):
        """
        Method that reset the game in the model and gui files. in other words
        it prepares the ground for another round of the game and ask the player
        if he wants to play again
        :return:
        """
        board = randomize_board()

        # Reset model
        self._model.stop_game(board)

        # Reset gui
        self._gui.reset_gui(board)
        self._gui.display_is_reset_to_user()
        for button in self._gui.get_buttons_info():
            action = self.create_button_action(button[1])
            self._gui.set_button_command(button[1], action)

    def run(self) -> None:
        """
        Method that runs the gui of game
        :return:
        """
        self._gui.run()


if __name__ == "__main__":
    BoggleController().run()
