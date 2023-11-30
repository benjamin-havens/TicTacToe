from enum import Enum

class TicTacToeSquareValues(Enum):
    EMPTY = 0
    X = 1
    O = 2

EMPTY = TicTacToeSquareValues.EMPTY
X = TicTacToeSquareValues.X
O = TicTacToeSquareValues.O

TIC_TAC_TOE_DISPLAY = {TicTacToeSquareValues.EMPTY.value: " ",
                       TicTacToeSquareValues.X.value: "X",
                       TicTacToeSquareValues.O.value: "O"}
