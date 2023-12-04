from abc import ABC, abstractmethod

from printing_utils import require_input_and_clear


class TwoPlayerGameMove(ABC):
    """
    Represents a move in a two player game. For example, would contain a row, column for tic-tac-toe.
    """

    @abstractmethod
    def __init__(self):
        pass


class TwoPlayerGameBoard(ABC):
    name: str
    is_game_over: bool
    winning_player: str

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def reset(self):
        pass

    @abstractmethod
    def play_move(self, move: TwoPlayerGameMove):
        pass

    @abstractmethod
    def undo_move(self):
        pass

    @abstractmethod
    def get_possible_moves(self):
        pass

    @abstractmethod
    def load_state(self, *args, **kwargs):
        pass

    @abstractmethod
    def depth(self):
        pass

    def static_evaluation(self):
        raise NotImplementedError()


class TwoPlayerGameAgent(ABC):
    name: str

    @abstractmethod
    def __init__(self, name, *args, **kwargs):
        pass

    @abstractmethod
    def get_move(self, board: TwoPlayerGameBoard):
        pass


class TwoPlayerGame:
    """
    Plays a game between two opponents. The strategy can be different between them.
    """

    def __init__(self,
                 board: TwoPlayerGameBoard,
                 player_1_agent: TwoPlayerGameAgent,
                 player_2_agent: TwoPlayerGameAgent,
                 silent=False):
        """
        Initialize the game with two players.
        :param board: TwoPlayerGameBoard of the game to be played.
        :param player_1_agent: TwoPlayerGameAgent which will receive a TwoPlayerGameBoard as input and should return
                            TwoPlayerGameMove. The onus is on the agent to ensure that the move is valid.
        :param player_2_agent: Similar to player_1_agent.
        :param silent: If True, will not print anything as the game proceeds; else, will print moves and winning info.
                        After printing something, it will wait for user input (eg, enter) to move on.
        """
        self.board = board
        self.player_1 = player_1_agent
        self.player_2 = player_2_agent
        self.silent = silent

    def swap_player_1_and_player_2(self):
        self.player_1, self.player_2 = self.player_2, self.player_1

    def play_in_terminal(self):
        self.board.reset()
        self._maybe_print("Press enter at each stage to move on.\n"
                          f"Beginning a game of {self.board.name} between {self.player_1.name} and {self.player_1.name}!\n\n",
                          clear=False)

        # Main game loop
        player, next_player = self.player_1, self.player_2
        while not self.board.is_game_over:
            # Get and announce move
            self._maybe_print(self.board)
            move = player.get_move(self.board)
            self._maybe_print(f"Player {player.name} chose to play {move}.")
            self.board.play_move(move)

            # Swap roles
            player, next_player = next_player, player

        self._maybe_print(self.board, clear=False)
        if self.board.winning_player != "":
            self._maybe_print(f"Player {self.board.winning_player} wins!", clear=False)
        else:
            self._maybe_print("It's a tie!", clear=False)

    def _maybe_print(self, s, clear=True):
        if not self.silent:
            if clear:
                require_input_and_clear(s)
            else:
                print(s)
