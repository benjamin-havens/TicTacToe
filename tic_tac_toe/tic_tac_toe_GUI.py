from itertools import product

import pygame

from two_player_game import TwoPlayerGameGUI
from .tic_tac_toe_game import TicTacToeBoard, TicTacToeMove, X, O

# Constants
BOARD_WIDTH, BOARD_HEIGHT = 600, 600
TEXT_BOX_HEIGHT = BOARD_HEIGHT // 4
SCREEN_WIDTH, SCREEN_HEIGHT = BOARD_WIDTH, BOARD_HEIGHT + TEXT_BOX_HEIGHT
LINE_WIDTH = min(BOARD_WIDTH, BOARD_HEIGHT) // 20
LINE_OFFSET = LINE_WIDTH * 2 / 3
BOARD_ROWS = 3
BOARD_COLS = 3
O_LINE_WIDTH = LINE_WIDTH // 3
O_CIRCLE_RADIUS = min(BOARD_WIDTH, BOARD_HEIGHT) / 6 - 2 * O_LINE_WIDTH
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

        self.screen = None
        self.reset()

    def reset(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Tic Tac Toe")

    def update_display(self):
        # Clear the board area
        board_rect = pygame.Rect(0, 0, BOARD_WIDTH, BOARD_HEIGHT)
        self.screen.fill(BG_COLOR, board_rect)

        # Draw board lines
        pygame.draw.line(self.screen, LINE_COLOR, (LINE_OFFSET, BOARD_HEIGHT / 3),
                         (BOARD_WIDTH - LINE_OFFSET, BOARD_HEIGHT / 3), LINE_WIDTH)
        pygame.draw.line(self.screen, LINE_COLOR, (LINE_OFFSET, BOARD_HEIGHT * 2 / 3),
                         (BOARD_WIDTH - LINE_OFFSET, BOARD_HEIGHT * 2 / 3), LINE_WIDTH)
        pygame.draw.line(self.screen, LINE_COLOR, (BOARD_WIDTH / 3, LINE_OFFSET),
                         (BOARD_WIDTH / 3, BOARD_HEIGHT - LINE_OFFSET), LINE_WIDTH)
        pygame.draw.line(self.screen, LINE_COLOR, (BOARD_WIDTH * 2 / 3, LINE_OFFSET),
                         (BOARD_WIDTH * 2 / 3, BOARD_HEIGHT - LINE_OFFSET), LINE_WIDTH)

        # Draw X's and O's
        for row, column in product(range(3), range(3)):
            if self.board.state[row, column] == X.value:
                pygame.draw.line(self.screen, X_COLOR,
                                 (column * BOARD_WIDTH / 3 + X_OFFSET, (row + 1) * BOARD_HEIGHT / 3 - X_OFFSET),
                                 ((column + 1) * BOARD_WIDTH / 3 - X_OFFSET, row * BOARD_HEIGHT / 3 + X_OFFSET),
                                 X_LINE_WIDTH)
                pygame.draw.line(self.screen, X_COLOR,
                                 (column * BOARD_WIDTH / 3 + X_OFFSET, row * BOARD_HEIGHT / 3 + X_OFFSET),
                                 ((column + 1) * BOARD_WIDTH / 3 - X_OFFSET, (row + 1) * BOARD_HEIGHT / 3 - X_OFFSET),
                                 X_LINE_WIDTH)
            elif self.board.state[row, column] == O.value:
                pygame.draw.circle(self.screen, O_COLOR,
                                   ((column + 1 / 2) * BOARD_WIDTH / 3, (row + 1 / 2) * BOARD_HEIGHT / 3),
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
                    move = TicTacToeMove(y // (BOARD_HEIGHT / 3), x // (BOARD_WIDTH / 3))
                    if move in self.board.get_possible_moves():
                        input_received = True
                        break

        return move

    def display_winner(self, winner: str):
        # Clear the text area
        board_rect = pygame.Rect(0, BOARD_HEIGHT, BOARD_WIDTH, SCREEN_HEIGHT)
        self.screen.fill(BG_COLOR, board_rect)
        # Display the winner on the screen
        font = pygame.font.Font(None, 72)  # Create a font object
        text = font.render(f'{winner} Wins!', True, (0, 128, 0)) if winner else font.render('Tie Game!', True,
                                                                                            (0, 128, 0))
        text_rect = text.get_rect(center=(BOARD_WIDTH / 2, BOARD_HEIGHT + TEXT_BOX_HEIGHT / 2))
        self.screen.blit(text, text_rect)  # Render the text on the screen
        pygame.display.update()

    def display_message(self, message: str):
        # Clear the text area
        text_area_rect = pygame.Rect(0, BOARD_HEIGHT, BOARD_WIDTH, TEXT_BOX_HEIGHT)
        self.screen.fill(BG_COLOR, text_area_rect)

        font = pygame.font.Font(None, 48)  # Font for the message
        max_line_width = BOARD_WIDTH - 20  # Maximum width for a line, with some margin

        # Split message into lines if it's too long
        words = message.split(' ')
        lines = []
        current_line = ''
        for word in words:
            # Check if adding the next word exceeds the line width
            if font.size(current_line + word)[0] <= max_line_width:
                current_line += word + ' '
            else:
                lines.append(current_line)
                current_line = word + ' '
        lines.append(current_line)  # Add the last line

        # Display each line of the message
        line_height = font.get_height()
        start_y = BOARD_HEIGHT + (TEXT_BOX_HEIGHT - line_height * len(lines)) / 2
        for i, line in enumerate(lines):
            text = font.render(line, True, (0, 0, 128))  # Blue text
            text_rect = text.get_rect(center=(BOARD_WIDTH / 2, start_y + i * line_height))
            self.screen.blit(text, text_rect)

        pygame.display.update()

        # Wait for half a second
        pygame.time.delay(500)

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
