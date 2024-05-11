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
            return True
        else:
            return False

    def is_game_over(self):
        # if all the cells are filled
        if "-" not in self.board:
            print("Game is finished!")
            return True
        # if the both of player has score of 0
        if self.player1.get_score() == 0 and self.player2.get_score() == 0:
            print("Game is finished!")
            return True

        # if the both of player are stuck
        if not self.can_make_move(self.player1.color) and not self.can_make_move(self.player2.color):
            print("Game is finished!")
            return True

        return False

    def is_valid_move(self, x, y, Player):
        if x < 0 or x > 7 or y < 0 or y > 7:
            print("Invalid coordinates!, out of range")
            return False

        if self.board[x][y] != "-":
            print("It is not an empty cell!")
            return False

        if not self.check_direction(x, y, Player):
            print("Invalid Position")
            return False

        return True

    def can_make_move(self, Player):
        for i in range(8):
            for j in range(8):
                if self.is_valid_move(i, j, Player):
                    return True
        return False

    def check_direction(self, x, y, Player):
        # create an empty list to store the coordinates of the cells that will be flipped
        flipped_pieces = []
        opponent = "W" if Player.color == "B" else "B"
        # This checks 4 directions around the cell up, down, left, right
        for x_distance, y_distance in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            # This is the initial position of the next cell
            x_temp = x + x_distance
            y_temp = y + y_distance
            if 0 <= x_temp < 8 and 0 <= y_temp < 8 and self.board[x_temp][y_temp] == opponent:
                # This loop is for ensuring that the recent move direction is passed by the opponent pieces
                # and the 2 pieces on the borders of them are the player pieces
                while 0 <= x_temp < 8 and 0 <= y_temp < 8 and self.board[x_temp][y_temp] == opponent:
                    x_temp += x_distance
                    y_temp += y_distance
                    if 0 <= x_temp < 8 and 0 <= y_temp < 8 and self.board[x_temp][y_temp] == Player.color:
                        # This loop is for adding the coordinates of the opponent pieces to the list
                        while True:
                            x_temp -= x_distance
                            y_temp -= y_distance
                            if x_temp == x and y_temp == y:
                                break
                            flipped_pieces.append((x_temp, y_temp))
        if len(flipped_pieces) > 0:
            self.flip_pieces(x, y, flipped_pieces, Player)
            return True

        return False

    def flip_pieces(self, x, y, flipped_pieces, Player):
        self.board[x][y] = Player.color
        for x_temp, y_temp in flipped_pieces:
            self.board[x_temp][y_temp] = Player.color
