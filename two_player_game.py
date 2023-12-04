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


class TwoPlayerGameBoardWithGUI(TwoPlayerGameBoard, ABC):
    @abstractmethod
    def initialize_GUI(self):
        pass

    @abstractmethod
    def show_welcome(self):
        pass

    @abstractmethod
    def show_winner(self):
        pass


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
        """
        self.board = board
        self.player_1 = player_1_agent
        self.player_2 = player_2_agent

    def swap_player_1_and_player_2(self):
        self.player_1, self.player_2 = self.player_2, self.player_1

    def play_in_terminal(self, silent=False):
        self.board.reset()
        self._maybe_print("Press enter at each stage to move on.\n"
                          f"Beginning a game of {self.board.name} between {self.player_1.name} and {self.player_2.name}!\n",
                          silent=silent,
                          clear=False)

        # Main game loop
        player, next_player = self.player_1, self.player_2
        while not self.board.is_game_over:
            # Get and announce move
            self._maybe_print(self.board, silent=silent)
            move = player.get_move(self.board)
            self._maybe_print(f"Player {player.name} played {move}.", silent=silent)
            self.board.play_move(move)

            # Swap roles
            player, next_player = next_player, player

        self._maybe_print(self.board, clear=False, silent=silent)
        if self.board.winning_player != "":
            self._maybe_print(f"Player {self.board.winning_player} wins!\n", silent=silent, clear=False)
        else:
            self._maybe_print("It's a tie!\n", silent=silent, clear=False)

    def play_in_GUI(self):
        assert isinstance(self.board,
                          TwoPlayerGameBoardWithGUI), "The game board must have GUI functions implemented to play in GUI"
        self.board.reset()
        self.board.initialize_GUI()
        self.board.show_welcome()

        # Main game loop
        player, next_player = self.player_1, self.player_2
        while not self.board.is_game_over:
            # Get and play move
            move = player.get_move(self.board)
            self.board.play_move(move)

            # Swap roles
            player, next_player = next_player, player

        self.board.show_winner()

    @staticmethod
    def _maybe_print(s, silent=False, clear=True):
        if not silent:
            if clear:
                require_input_and_clear(s)
            else:
                print(s)
