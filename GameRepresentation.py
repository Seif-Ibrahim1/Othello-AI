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
                    print(".", end=" ")
                elif self.board[i][j] == "W":
                    print("W", end=" ")
                else:
                    print("B", end=" ")
            print()

    def move(self, x, y, Player):
        if self.is_valid_move(x, y, Player):
            self.board[x][y] = Player.color
            flipped_pieces = self.getFlippedPieces(x , y , Player)
            self.flip_pieces(x , y , flipped_pieces , Player)
            return True
        else:
            return False

    def is_game_over(self):
        # if all the cells are filled
        if "-" not in self.board:
            return True
        # if the both of player has score of 0
        if self.player1.get_score() == 0 and self.player2.get_score() == 0:
            return True

        return False

    def is_valid_move(self, x, y, Player):
        if x < 0 or x > 7 or y < 0 or y > 7:
            return False

        if self.board[x][y] != "-":
            return False

        availableMoves = self.getAvailableMoves(Player)
        if (x, y) not in availableMoves:
            return False

        return True

    def check_direction(self, x, y, Player):
        # This function checks if there are any opponent pieces that can be flipped in any direction
        opponent = "W" if Player.color == "B" else "B"
        for x_distance, y_distance in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            x_temp, y_temp = x + x_distance, y + y_distance
            if 0 <= x_temp < 8 and 0 <= y_temp < 8 and self.board[x_temp][y_temp] == opponent:
                while 0 <= x_temp < 8 and 0 <= y_temp < 8 and self.board[x_temp][y_temp] == opponent:
                    x_temp += x_distance
                    y_temp += y_distance
                    if 0 <= x_temp < 8 and 0 <= y_temp < 8 and self.board[x_temp][y_temp] == Player.color:
                        return True
        return False

    def getAvailableMoves(self, Player):
        availableMoves = []
        for i in range(8):
            for j in range(8):
                if self.check_direction(i, j, Player):
                    availableMoves.append((i, j))
        return availableMoves

    def getFlippedPieces(self, x, y, Player):
        flipped_pieces = []
        opponent = "W" if Player.color == "B" else "B"
        for x_distance, y_distance in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            x_temp, y_temp = x + x_distance, y + y_distance
            temp_flipped = []
            if 0 <= x_temp < 8 and 0 <= y_temp < 8 and self.board[x_temp][y_temp] == opponent:
                while 0 <= x_temp < 8 and 0 <= y_temp < 8 and self.board[x_temp][y_temp] == opponent:
                    temp_flipped.append((x_temp, y_temp))
                    x_temp += x_distance
                    y_temp += y_distance
                    if 0 <= x_temp < 8 and 0 <= y_temp < 8 and self.board[x_temp][y_temp] == Player.color:
                        flipped_pieces.extend(temp_flipped)
        return flipped_pieces

    def flip_pieces(self, x, y, flipped_pieces, Player):
        self.board[x][y] = Player.color
        for x_temp, y_temp in flipped_pieces:
            self.board[x_temp][y_temp] = Player.color
