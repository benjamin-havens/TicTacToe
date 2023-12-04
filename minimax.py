from functools import cache

from two_player_game import *


@cache
def minimax(board, is_maximizing_player, max_depth=float("inf")):
    return _minimax_helper(board, 0, is_maximizing_player, float("-inf"), float("inf"), max_depth)


@cache
def _minimax_helper(board: TwoPlayerGameBoard, current_search_depth, is_maximizing_player, alpha, beta,
                    max_depth=float("inf")):
    if board.is_game_over or current_search_depth >= max_depth:
        return board.static_evaluation(), None

    if is_maximizing_player:
        best_outcome = float("-inf")
        best_move = None
        for candidate_move in board.get_possible_moves():
            board.play_move(candidate_move)
            candidate_move_value, _ = _minimax_helper(board, current_search_depth + 1, not is_maximizing_player, alpha,
                                                      beta,
                                                      max_depth)
            board.undo_move()

            if candidate_move_value > best_outcome:
                best_move = candidate_move
            best_outcome = max(best_outcome, candidate_move_value)
            alpha = max(alpha, best_outcome)
            if beta <= alpha:
                break

        return best_outcome, best_move

    else:
        best_outcome = float("inf")
        best_move = None
        for candidate_move in board.get_possible_moves():
            board.play_move(candidate_move)
            candidate_move_value, _ = _minimax_helper(board, current_search_depth + 1, not is_maximizing_player, alpha,
                                                      beta,
                                                      max_depth)
            board.undo_move()

            if candidate_move_value < best_outcome:
                best_move = candidate_move
            best_outcome = min(best_outcome, candidate_move_value)
            beta = min(beta, best_outcome)
            if beta <= alpha:
                break

        return best_outcome, best_move
