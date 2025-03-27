import tkinter as tki
from typing import Callable, Dict, List, Any, Tuple, Union

# PROGRAM DATA-STRUCTURES #
BOARD_TYPE = List[List[str]]
COORDS_TYPE = Tuple[int, int]
BUTTONS_INNER_DICT = Dict[str, Union[tki.Button, bool]]

# COLOR SETTING #
BUTTON_HOVER_COLOR = 'gray'
WINDOW_BG_COLOR = 'light gray'
BUTTON_COLOR = "misty rose"
BUTTON_ACTIVE_COLOR = 'slateblue'
WRONG_WORD_BG = "red"
RIGHT_WORD_BG = "green"
ACTIVE_BUTTON_COLOR = "yellow"  # Active button color (clicked button)

# BUTTONS SETTINGS #
BUTTON_STYLE = {"font": ("Courier", 30),
                "borderwidth": 1,
                "relief": tki.RAISED,
                "bg": BUTTON_COLOR,
                "activebackground": BUTTON_ACTIVE_COLOR,
                "width": 2,
                "height": 1}
SUBMIT_BUTTON_TEXT = "Submit"
SUBMIT_BUTTON_COORD = (4, 1)
DISPLAY_LABEL_FONT = ("Courier", 30)
USED_WORDS_FONT = ("Courier", 20)

# MESSAGES #
RESET_MESSAGE = """Time is up!
Would you like to play 
another round?
(Click any button to restart)"""

# dimensions #
DETAILS_LABEL_WIDTH = 10
DETAILS_LABEL_HEIGHT = 8
FONT_SIZE = 15

class BoggleGUI:
    _buttons: Dict[COORDS_TYPE, BUTTONS_INNER_DICT] = {}

    def __init__(self, board):
        # Tkinter / OS window settings
        self.__board = board
        root = tki.Tk()
        root.title("Boggle")
        root.resizable(False, False)
        self._main_window = root

        # Display setting
        self._top_frame = tki.Frame(root, bg="mint cream",
                                    highlightbackground=WINDOW_BG_COLOR,
                                    highlightthickness=5)
        self._top_frame.pack(side=tki.TOP, fill=tki.BOTH, expand=True)

        self._display_label = tki.Label(self._top_frame,
                                        text="Welcome to Boggle!",
                                        font=DISPLAY_LABEL_FONT,
                                        bg=WINDOW_BG_COLOR, width=30, height=4,
                                        relief="ridge")
        self._display_label.pack(side=tki.TOP, fill=tki.BOTH, expand=True)

        self._used_words = tki.Label(self._top_frame, text="Guessed Words",
                                     font=USED_WORDS_FONT,
                                     bg=WINDOW_BG_COLOR, width=30, height=3,
                                     relief="ridge", wraplengt=700)
        self._used_words.pack(side=tki.TOP, fill=tki.BOTH)

        self._timer_label = tki.Label(self._top_frame, text="Timer",
                                      font=("Courier", FONT_SIZE),
                                      bg="LightBlue1", width=DETAILS_LABEL_WIDTH, height=DETAILS_LABEL_HEIGHT,
                                      relief="ridge")
        self._timer_label.pack(side=tki.RIGHT, fill=tki.X)

        self._score_label = tki.Label(self._top_frame, text="Score",
                                      font=("Courier", FONT_SIZE),
                                      bg="LightBlue1", width=DETAILS_LABEL_WIDTH, height=DETAILS_LABEL_HEIGHT,
                                      relief="ridge")
        self._score_label.pack(side=tki.RIGHT, fill=tki.X)

        self._score_percent_label = tki.Label(self._top_frame, text="Score %",
                                              font=("Courier", FONT_SIZE),
                                              bg="LightBlue1", width=DETAILS_LABEL_WIDTH,
                                              height=DETAILS_LABEL_HEIGHT,
                                              relief="ridge")
        self._score_percent_label.pack(side=tki.RIGHT, fill=tki.X)

        self._middle_frame = tki.Frame(self._top_frame, bg="mint cream")
        self._middle_frame.pack(side=tki.TOP, fill=tki.BOTH)  # Buttons frame

        self.reset_gui(board)

    def set_display_cur(self, display_text: str) -> None:
        """
        Method that sets the display (label) of the current built word
        :param display_text: string of the in proccess word
        :return:
        """
        self._display_label["text"] = display_text

    def set_display_used(self, display_text: list) -> None:
        """
        Method that sets the display of the used word list
        :param display_text: list of strings of the used words
        :return:
        """
        self._used_words["text"] = display_text

    def set_timer_display(self, display_text: str) -> None:
        """
        Method that sets the display of the timer label
        :param display_text: string of the current time
        :return:
        """
        self._timer_label["text"] = "Time left:\n" + display_text

    def set_score_display(self, score_display: int,
                          score_percent_display: str) -> None:
        """
        Method that sets the display of the score label
        :param score_display: string of the current score
        :param score_percent_display: string of the current score percent
        :return:
        """
        self._score_label["text"] = "Score:\n" + str(score_display)
        self._score_percent_label["text"] = "%Scored:\n" + score_percent_display

    def set_button_command(self, coord: COORDS_TYPE, cmd: Callable[[], None]
                           ) -> None:
        """
        Method that sets the command of a given button
        :param coord: cordinates of the wanted button
        :param cmd: action enacted
        :return:
        """
        self._buttons[coord]["button"].configure(command=cmd)

    def _set_board(self, board: BOARD_TYPE):
        """
        Method that sets the initialized board to a given board type
        :param board: a nested list of the board (containing strings)
        :return:
        """
        self.__board = board

    def get_button_cords(self) -> List[COORDS_TYPE]:
        """
        Method that returns a list of all the buttons coordinates
        :return: list of tuples
        """
        return list(self._buttons.keys())

    def get_buttons_info(self) -> List[Tuple[str, COORDS_TYPE]]:
        """
        Method that returns a tuple containing all the button characters
        and their corresponding coordinates
        :return: list of tuples of button names and coordinates
        """
        buttons_cords = []
        for cord in self._buttons.keys():
            buttons_cords.append((self._buttons[cord]["button"]['text'], cord))
        return buttons_cords

    def _create_buttons_in_middle_frame(self) -> None:
        """
        Method that creates the grid of all buttons (characters buttons and
        submit button).
        :return:
        """
        for i in range(4):
            tki.Grid.columnconfigure(self._middle_frame, i, weight=1)

        for i in range(4):
            tki.Grid.rowconfigure(self._middle_frame, i, weight=1)

        for x in range(len(self.__board)):
            for y in range(len(self.__board[x])):
                self._make_button("", x, y)
        self._make_button("", *SUBMIT_BUTTON_COORD, columnspan=2)

    def _make_button(self, button_char: str, row: int, col: int,
                     rowspan: int = 1, columnspan: int = 1) -> tki.Button:
        """
        Method that creates a button, placing it on a grid, and creates
        its clicked visual characteristics
        :param button_char: string of the button string content
        :param row: row of the button's location
        :param col: column of the button's location
        :param rowspan: the grid row span of the button
        :param columnspan: the grid column span of the button
        :return: the button type that is made
        """
        button = tki.Button(self._middle_frame, text=button_char,
                            **BUTTON_STYLE)
        button.grid(row=row, column=col, rowspan=rowspan,
                    columnspan=columnspan, sticky=tki.NSEW)
        self._buttons[(row, col)] = {}
        self._buttons[(row, col)]["button"] = button
        self._buttons[(row, col)]["is_active"] = False

        def _on_enter(event: Any) -> None:
            if not self._buttons[(row, col)]["is_active"]:
                button['background'] = BUTTON_HOVER_COLOR

        def _on_leave(event: Any) -> None:
            if not self._buttons[(row, col)]["is_active"]:
                button['background'] = BUTTON_COLOR
        button.bind("<Enter>", _on_enter)
        button.bind("<Leave>", _on_leave)
        return button

    def display_is_reset_to_user(self):
        """
        Method that sets the display message for when a round of the game is
        finished
        :return:
        """
        self._display_label["text"] = RESET_MESSAGE

    def set_buttons_text(self):
        """
        Method that sets the button text for the gui button list for it to
        be displayed on the screen
        :return:
        """
        for x in range(len(self.__board)):
            for y in range(len(self.__board[x])):
                self._buttons[(x, y)]["button"]["text"] = self.__board[x][y]
        self._buttons[SUBMIT_BUTTON_COORD]["button"]["text"] = SUBMIT_BUTTON_TEXT

    def set_buttons_color(self, buttons_coords: List[COORDS_TYPE],
                          color: str, is_submit: bool) -> None:
        """
        Set the buttons color after submitting.
        :param buttons_coords: list of tuples of all the button cords
        :param color: the color of the buttons in the list
        :param is_submit: boolean that checks the situation (whether the submit
        button was pressed or not)
        :return:
        """
        def _handle_submit_logic() -> None:
            self.set_buttons_color(buttons_coords, BUTTON_COLOR,
                                   is_submit=False)
            for button in buttons_coords:
                self.set_button_is_active(button, False)

        for button_coord in buttons_coords:
            self._buttons[button_coord]["button"].configure(bg=color)
        if is_submit:
            self._main_window.after(
                1000,
                lambda: _handle_submit_logic()
            )

    def set_button_is_active(self, coord: COORDS_TYPE, is_active: bool):
        """
        sets the button situation, whether the button is currently active or not.
        active button means that the button was legally pressed in the current
        word round (after the last clicked on the submit button and before the
        next)
        :param coord: coordinates of the button clicked
        :param is_active: boolean that updates the button's activity status
        :return:
        """
        self._buttons[coord]["is_active"] = is_active

    def reset_gui(self, board: BOARD_TYPE):
        """
        Method that resets the gui board
        :param board: board, nested list of string (button characters)
        :return:
        """
        self._set_board(board)
        self._create_buttons_in_middle_frame()

    def get_main_window(self):
        """
        Method that returns the main window of the gui
        :return: the main window of the gui
        """
        return self._main_window

    def run(self):
        """
        Method that runs the main loop of the gui display
        :return:
        """
        self._main_window.mainloop()
