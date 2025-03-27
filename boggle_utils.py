from typing import List, Tuple, Optional, Iterable, Union, Set

BOARD_TYPE = List[List[str]]
WORDS_TYPE = Iterable[str]
PATH_TYPE = List[Tuple[int, int]]


def is_valid_path(board: BOARD_TYPE, path: PATH_TYPE,
                  words: WORDS_TYPE) -> Optional[str]:
    """
    Checks if the given path is a valid path of word (each cell is in radius
     of 1 cell from the previous cell), and represents a word from the words
     list.
    Returns the word if is does, None otherwise.
    :param board: Boggle 4x4 board.
    :param path: List of adjacent coordinates on the board.
    :param words: Words list
    :return: As described.
    """
    if len(path) == 0:
        if "" in words:
            return ""
        return
    word = ""
    try:
        prev_cell_row, prev_cell_col = path[0]
        word += board[prev_cell_row][prev_cell_col]
    except IndexError:
        # First cell in path is out of board
        return None
    else:
        for cell_row, cell_col in path[1:]:
            if prev_cell_row == cell_row and prev_cell_col == cell_col:
                return None
            if (
                    abs(cell_row - prev_cell_row) > 1
                    or abs(cell_col - prev_cell_col) > 1
            ):
                return None
            if (
                not 0 <= cell_row < len(board)
                or not 0 <= cell_col < len(board[0])
            ):
                return None
            word += board[cell_row][cell_col]
            prev_cell_row, prev_cell_col = cell_row, cell_col
        if word not in words:
            return None
        return word


def _find_length_n_paths_helper(n: int, board: BOARD_TYPE,
                                words: WORDS_TYPE, start_pos: Tuple[int, int],
                                length_n_paths: List[PATH_TYPE],
                                path: PATH_TYPE) -> Optional[List[PATH_TYPE]]:
    """
    Helper function for find_length_n_paths.
    :param n: Length of the path.
    :param board: Boggle 4x4 board.
    :param words: Word iterable.
    :param start_pos: Start coordinate of the backtracking.
    :param length_n_paths: List of the valid paths already found.
    :param path: The current path the function backtracks.
    :return: length_n_paths - paths in the length of n that holds valid word.
    """
    if len(path) == n:
        word = is_valid_path(board, path, words)
        if word is not None:
            length_n_paths.append(path[:])
        return
    row, col = start_pos
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            current_cell = (row + dx, col + dy)
            if (
                    row + dx < 0
                    or row + dx >= len(board)
                    or col + dy < 0
                    or col + dy >= len(board[0])
                    or (dx == 0 and dy == 0)
            ):
                pass
            elif current_cell in path:
                pass
            else:
                path.append(current_cell)
                _find_length_n_paths_helper(
                    n, board, words, (row + dx, col + dy), length_n_paths,
                    path
                )
                path.pop()


def find_length_n_paths(n: int, board: BOARD_TYPE, words: WORDS_TYPE
                        ) -> List[PATH_TYPE]:
    """
    Returns list of all the legal paths on the board in a given length.
    Legal path is defined in is_valid_path.
    :param n: Length of path.
    :param board: Boggle 4x4 board.
    :param words: Words list.
    :return: As described.
    """
    paths_in_length = []
    for i in range(len(board)):
        for j in range(len(board[0])):
            _find_length_n_paths_helper(
                n, board, words, (i, j), paths_in_length, [(i, j)]
            )
    return paths_in_length


def _find_length_n_words_helper(n: int, board: BOARD_TYPE,
                                words: WORDS_TYPE, start_pos: Tuple[int, int],
                                words_in_length: List[Union[str, PATH_TYPE]],
                                path: PATH_TYPE,
                                word: str,
                                word_append_mode=False
                                ) -> Optional[Union[List[str], List[PATH_TYPE]]]:
    """
    Helper function for find_length_n_words.
    :param n: Length of each word.
    :param board: Boggle 4x4 board.
    :param words: Word iterable.
    :param start_pos: Start position for the backtracking.
    :param words_in_length: List of the words / paths already found.
    :param path: The current path currently backtracked.
    :param word: The accumulated word.
    :param word_append_mode: If set to True, the function will append the
    accumulated words to the return list. Otherwise, it will append the path,
    as was requested in the exercise.
    :return: As described in words_append_mode.
    """
    if len(word) > n:
        return
    if len(word) == n:
        if is_valid_path(board, path, words) is not None:
            if word not in words_in_length:
                if not word_append_mode:
                    words_in_length.append(path[:])
                else:
                    words_in_length.append(word)
        return
    row, col = start_pos
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            current_cell = (row + dx, col + dy)
            if (
                    row + dx < 0
                    or row + dx >= len(board)
                    or col + dy < 0
                    or col + dy >= len(board[0])
                    or (dx == 0 and dy == 0)
            ):
                pass
            elif current_cell in path:
                pass
            else:
                path.append(current_cell)
                word += board[row + dx][col + dy]
                _find_length_n_words_helper(
                    n, board, words, (row + dx, col + dy), words_in_length,
                    path, word, word_append_mode
                )
                path.pop()
                word = word[:-len(board[row + dx][col + dy])]


def find_length_n_words(n: int, board: BOARD_TYPE, words: WORDS_TYPE):
    """
    Returns list of the paths of n-length words on the board that appear in
    the given words iterable.
    :param n: The length of the words.
    :param board: Boggle 4x4 board.
    :param words: Word iterable.
    :return: As described.
    """
    words_in_length = []
    for i in range(len(board)):
        for j in range(len(board[0])):
            _find_length_n_words_helper(
                n, board, words, (i, j), words_in_length, [(i, j)], board[i][j]
            )
    return words_in_length


def _find_n_length_path_for_word_helper(n: int, board: BOARD_TYPE,
                                        wished_word: str,
                                        start_pos: Tuple[int, int],
                                        word: str,
                                        path: PATH_TYPE
                                        ) -> Optional[PATH_TYPE]:
    """
    Helper function for find_n_length_path_for_word.
    :param n: Length of the desired path.
    :param board: Boggle 4x4 board.
    :param wished_word: The word to look for.
    :param start_pos: Start position for the backtracking.
    :param word: Accumulated word.
    :param path: Accumulated path.
    :return: n-length path to the word if found, None otherwise.
    """
    if len(path) == n:
        if word == wished_word:
            return path
        return
    if len(word) > 0 and word != wished_word[:len(word)]:
        # Stop backtracking, word won't match.
        return
    row, col = start_pos
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            current_cell = (row + dx, col + dy)
            if (
                    not(0 <= row + dx < len(board))
                    or not(0 <= col + dy < len(board[0]))
                    or (dx == 0 and dy == 0)
            ):
                continue
            elif current_cell in path:
                continue
            else:
                # Add cell to backtracking
                path.append(current_cell)
                word += board[row + dx][col + dy]

                # Assume receiving length n path, starting with the current
                # affix
                n_len_path = _find_n_length_path_for_word_helper(
                    n, board, wished_word, (row + dx, col + dy), word,
                    path
                )

                # Validate backtracking result
                if n_len_path is not None:
                    return n_len_path

                # Undo backtracking step
                path.pop()
                word = word[:-len(board[row + dx][col + dy])]


def find_n_length_path_for_word(board: BOARD_TYPE, word: str, n: int
                                ) -> Optional[PATH_TYPE]:
    """
    Gets word length and finds the first path in the board with the given
    length that holds the word.
    :param board: Boggle 4x4 board.
    :param word: Word to look for.
    :param n: The length of the requested path.
    :return: Path if found, None otherwise.
    """
    for i in range(len(board)):
        for j in range(len(board[0])):
            path = _find_n_length_path_for_word_helper(
                        n, board, word, (i, j), board[i][j], [(i, j)]
                    )
            if path is not None:
                return path


def _max_score_paths_helper(board: BOARD_TYPE, word: str
                            ) -> Optional[PATH_TYPE]:
    """
    Helper function to max_score_paths.
    :param board: Boggle 4x4 board.
    :param word: Word to look for in the board.
    :return: Highest score path in the board for the word if found, None
    otherwise.
    """
    for n in range(len(word), 0, -1):
        path = find_n_length_path_for_word(board, word, n)
        if path is not None:
            return path


def max_score_paths(board: BOARD_TYPE, words: WORDS_TYPE) -> List[PATH_TYPE]:
    """
    Returns list of all the paths which are paths of words from the words list
     appear on the board, and granting the highest score for the word they
     represent.
    :param board: Boggle game board
    :param words: Words list
    :return: List of paths, as described.
    """
    max_score_paths_list = []
    for word in words:
        path = _max_score_paths_helper(board, word)
        if path is not None:
            max_score_paths_list.append(path)
    return max_score_paths_list


def load_words_list(file: str = "boggle_dict.txt") -> Set[str]:
    """
    Loads words from file.
    :param file: File path.
    :return: List of the words.
    """
    with open(file) as file_obj:
        words = {line.strip(" \n\r") for line in file_obj}
        return words
