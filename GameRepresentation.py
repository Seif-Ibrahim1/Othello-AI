import numpy as np


class GameBoard:
    # This is the initial version of the board
    # Having the 4 initial pieces in the middle
    def __init__(self):
        self.board = np.full((8, 8), "-")
        self.board[3][3] = "W"
        self.board[4][4] = "W"
        self.board[3][4] = "B"
        self.board[4][3] = "B"

    def print_board(self):
        print(self.board)

    def check_boundary(self, x, y, player):
        # This condition is for ensuring that the move is inside the board
        # and the cell is empty
        if self.board[x][y] != "-":
            return False
        return True

    def check_direction(self, x, y, player):
        opponent = "W" if player == "B" else "B"
        # This checks 4 directions around the cell up, down, left, right
        for x_distance, y_distance in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            # This is the initial position of the next cell
            x_temp = x + x_distance
            y_temp = y + y_distance
            if self.board[x_temp][y_temp] == opponent:
                # This loop is for ensuring that the recent move direction is passed by the opponent pieces
                # and the 2 pieces on the borders of them are the player pieces
                while self.board[x_temp][y_temp] == opponent:
                    x_temp += x_distance
                    y_temp += y_distance
                    if self.board[x_temp][y_temp] == player:
                        return True
        return False

    def check_move(self, x, y, player):
        if not self.check_boundary(x, y, player):
            return False
        if not self.check_direction(x, y, player):
            return False
        return True

    def make_move(self, x, y, player):
        if not self.check_move(x, y, player):
            return False
        self.board[x][y] = player
        return True

    def get_score(self):
        score = {"B": 0, "W": 0}
        for x in range(8):
            for y in range(8):
                if self.board[x][y] != "-":
                    score[self.board[x][y]] += 1
        return score

    def get_winner(self):
        score = self.get_score()
        if score["B"] > score["W"]:
            return "B"
        elif score["B"] < score["W"]:
            return "W"
        return "Draw"

    def can_make_move(self, player):
        for x in range(8):
            for y in range(8):
                if self.check_move(x, y, player):
                    return True
        return False

    def is_over(self):
        return not self.can_make_move('B') and not self.can_make_move('W')

    def get_result(self):
        if self.is_over():
            return self.get_winner()
