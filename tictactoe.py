class TicTacToe:
    def __init__(self):
        self.board = [' ' for _ in range(9)]  # 3x3 board
        self.curr = 'X'

    def choice(self, index):
        if self.board[index] == ' ':
            self.board[index] = self.curr
        else:
            return "Square has already been chosen!"

        if self.curr == 'X':
            self.curr = '0'
        else:
            self.curr = 'X'

    def get_board(self):
        return self.board