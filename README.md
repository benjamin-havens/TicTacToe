# TicTacToe
TicTacToe board utility, game player, and various computer agents.

The board utility, `TicTacToeBoard`, has the ability to play moves, check for wins, undo moves, reset, load arbitrary states, and return possible moves. It has `__hash__`, `__eq__`, and `__str__` methods.

The centerpiece of the minimax file is `get_best_tictactoe_move`, which intakes a `TicTacToeBoard` and returns the best move as a `(row, column)` tuple.

The player utility, `TicTacToeGamePlayer`, allows arbitrary callables to be used as a tic-tac-toe strategy, provided they can accept a `TicTacToeBoard` as input and return a `(row, column)` tuple.
It has rudimentary UI through the terminal, which can be disabled for silence.

### TODO
- Doc strings
- Little RL agent :)

### Credits
Thanks to [never stop building](https://www.neverstopbuilding.com/blog/minimax) for help improving the minimax algorithm, so that delays losing for as long as possible on a rigged starting board!
