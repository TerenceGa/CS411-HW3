import logging

from flask import Response

from tictactoe import Board, configure_logger, INVALID_MOVE_ERROR_MSG
from tictactoe.model import Model
from tictactoe.view import View


MODEL = Model()
VIEW = View()


logger = logging.getLogger(__name__)
configure_logger()


def get_board_state() -> Response:
    """
    Retrieves the current state of the board.

    Returns
    -------
    Response
        A Flask response object containing the board state as JSON.
    """
    return VIEW.board_state(MODEL.board)

def get_winner() -> Response:
    """
    Retrieves the winner of the game, if there is one.

    Returns
    -------
    Response
        A Flask response object containing the winner as JSON.
    """
    return VIEW.get_winner(MODEL.get_winner())

def validate_index(index: str) -> int:
    """
    Validates the provided index for a move.

    Parameters
    ----------
    index : str
        The index to validate.

    Returns
    -------
    int
        The validated index.

    Raises
    ------
    ValueError
        If the index is not a valid integer or is out of bounds.
    """
    try:
        index = int(index)
    except ValueError:
        raise ValueError(INVALID_MOVE_ERROR_MSG)
    
    if index < 0 or index > 8:
        raise ValueError(INVALID_MOVE_ERROR_MSG)
    
    return index

def make_move(index: str) -> Response:
    """
    ##Makes a move at the specified index.

    Parameters
    ----------
    index : str
        The index at which to make the move.

    Returns
    -------
    Response
        A Flask response object indicating success or failure.
    """
    try:
        index_fine = validate_index(index)
        MODEL.move(index_fine)
        return VIEW.board_state(MODEL.board)
    except ValueError as e:
        logger.error(f"Error making move: {e}")
        return VIEW.error(str(e), 400)