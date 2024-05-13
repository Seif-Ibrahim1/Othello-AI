import numpy as np

from Player import Player


class GameBoard:
    # This is the initial version of the board
    # Having the 4 initial pieces in the middle
    def __init__(self):
        self.player1 = Player("B")
        self.player2 = Player("W")
        self.board = np.full((8, 8), "-")
        self.board[3][3] = "W"
        self.board[4][4] = "W"
        self.board[3][4] = "B"
        self.board[4][3] = "B"

    def print_board(self):
        print("  0 1 2 3 4 5 6 7")
        for i in range(8):
            print(i, end=" ")
            for j in range(8):
                if self.board[i][j] == "-":
                    print("-", end=" ")
                elif self.board[i][j] == "W":
                    print("W", end=" ")
                else:
                    print("B", end=" ")
            print()

    def is_game_over(self):
        # if all the cells are filled
        if "-" not in self.board:
            return True
        # if one of th players has score of 0
        if self.player1.get_score() == 0 or self.player2.get_score() == 0:
            return True

        return False

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

    def get_utility(self, player):
        score = self.get_score()
        if player == "B":
            return score["B"] - score["W"]
        else:
            return score["W"] - score["B"]
