from itertools import product

import pygame

from two_player_game import TwoPlayerGameGUI
from .tic_tac_toe_game import TicTacToeBoard, TicTacToeMove, X, O

# Constants
WIDTH, HEIGHT = 600, 600
LINE_WIDTH = min(WIDTH, HEIGHT) // 20
LINE_OFFSET = LINE_WIDTH * 2 / 3
BOARD_ROWS = 3
BOARD_COLS = 3
O_LINE_WIDTH = LINE_WIDTH // 3
O_CIRCLE_RADIUS = min(WIDTH, HEIGHT) / 6 - 2 * O_LINE_WIDTH
X_LINE_WIDTH = LINE_WIDTH // 3
X_OFFSET = 3 / 2 * LINE_OFFSET

# Colors
X_COLOR = (255, 0, 0)
O_COLOR = (0, 0, 255)
BG_COLOR = (255, 255, 255)
LINE_COLOR = (0, 0, 0)


class TicTacToeGUI(TwoPlayerGameGUI):

    def __init__(self, board: TicTacToeBoard):
        self.board = board

        pygame.init()
        self.screen = None
        self.reset()

    def reset(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Tic Tac Toe")

    def update_display(self):
        # Clear the screen
        self.screen.fill(BG_COLOR)

        # Draw board lines
        pygame.draw.line(self.screen, LINE_COLOR, (LINE_OFFSET, HEIGHT / 3),
                         (WIDTH - LINE_OFFSET, HEIGHT / 3), LINE_WIDTH)
        pygame.draw.line(self.screen, LINE_COLOR, (LINE_OFFSET, HEIGHT * 2 / 3),
                         (WIDTH - LINE_OFFSET, HEIGHT * 2 / 3), LINE_WIDTH)
        pygame.draw.line(self.screen, LINE_COLOR, (WIDTH / 3, LINE_OFFSET),
                         (WIDTH / 3, HEIGHT - LINE_OFFSET), LINE_WIDTH)
        pygame.draw.line(self.screen, LINE_COLOR, (WIDTH * 2 / 3, LINE_OFFSET),
                         (WIDTH * 2 / 3, HEIGHT - LINE_OFFSET), LINE_WIDTH)

        # Draw X's and O's
        for row, column in product(range(3), range(3)):
            if self.board.state[row, column] == X.value:
                pygame.draw.line(self.screen, X_COLOR,
                                 (column * WIDTH / 3 + X_OFFSET, (row + 1) * HEIGHT / 3 - X_OFFSET),
                                 ((column + 1) * WIDTH / 3 - X_OFFSET, row * HEIGHT / 3 + X_OFFSET), X_LINE_WIDTH)
                pygame.draw.line(self.screen, X_COLOR, (column * WIDTH / 3 + X_OFFSET, row * HEIGHT / 3 + X_OFFSET),
                                 ((column + 1) * WIDTH / 3 - X_OFFSET, (row + 1) * HEIGHT / 3 - X_OFFSET), X_LINE_WIDTH)
            elif self.board.state[row, column] == O.value:
                pygame.draw.circle(self.screen, O_COLOR, ((column + 1 / 2) * WIDTH / 3, (row + 1 / 2) * HEIGHT / 3),
                                   O_CIRCLE_RADIUS, O_LINE_WIDTH)

        # Update the display
        pygame.display.update()

    def get_user_move(self) -> TicTacToeMove:
        input_received = False
        move = None
        while not input_received:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    move = TicTacToeMove(y // (HEIGHT / 3), x // (WIDTH / 3))
                    if move in self.board.get_possible_moves():
                        input_received = True
                        break

        return move

    def display_winner(self, winner: str):
        # Display the winner on the screen
        pass

    def display_message(self, message: str):
        # Use PyGame to display messages like "Player X's Turn"
        pass

    def clear(self):
        self.board.reset()
        self.reset()
        self.update_display()

    def await_exit(self):
        # Process PyGame events
        user_has_quit = False
        while not user_has_quit:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    user_has_quit = True
                    break
        self.reset()


# Example of using the GUI
if __name__ == "__main__":
    board = TicTacToeBoard()
    gui = TicTacToeGUI(board)
    gui.update_display()
    print(gui.get_user_move())
