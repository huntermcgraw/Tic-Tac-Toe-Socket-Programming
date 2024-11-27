class TicTacToe:
    def __init__(self):
        self.board = ['' for _ in range(9)]
        self.curr = 'X'

    def get_board(self):
        return self.board
