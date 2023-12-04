import numpy as np

from minimax import minimax
from two_player_game import TwoPlayerGameAgent
from ..tic_tac_toe_game import TicTacToeBoard, X, O


class TicTacToeMiniMaxAgent(TwoPlayerGameAgent):

    def __init__(self, name):
        self.name = name

    def get_move(self, board: TicTacToeBoard):
        evaluation, move = minimax(board, board.next_player == X)
        return move


if __name__ == "__main__":
    # Test minimax player
    board = TicTacToeBoard()
    agent = TicTacToeMiniMaxAgent("minimax")

    # Play against self--must result in cat's game
    while not board.is_game_over:
        best_move = agent.get_move(board)
        board.play_move(best_move)
    print(board)
    print(board.move_history)

    # Load a lost state for O and get O's move. It should block
    state = np.array([[0, 1, 0], [0, 0, 1], [2, 2, 1]])
    board.load_state(state, O)
    print(board)
    print(agent.get_move(board))
