class Move:
    def __init__(self, board , player):
        self.board = board
        self.player = player

    def move(self, x, y, player):
        if self.is_valid_move(x, y, player):
            self.board.board[x][y] = player.color
            flipped_pieces = self.get_flipped_pieces(x, y, player)
            self.flip_pieces(x, y, flipped_pieces, player)
            return True
        else:
            return False

    def is_valid_move(self, x, y, player):
        if x < 0 or x > 7 or y < 0 or y > 7:
            return False

        if self.board.board[x][y] != "-":
            return False

        available_moves = self.get_available_moves(player)
        if (x, y) not in available_moves:
            return False

        return True

    def check_direction(self, x, y, player):
        # This function checks if there are any opponent pieces that can be flipped in any direction
        opponent = "W" if player.color == "B" else "B"
        for x_distance, y_distance in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            x_temp, y_temp = x + x_distance, y + y_distance
            if 0 <= x_temp < 8 and 0 <= y_temp < 8 and self.board.board[x_temp][y_temp] == opponent:
                while 0 <= x_temp < 8 and 0 <= y_temp < 8 and self.board.board[x_temp][y_temp] == opponent:
                    x_temp += x_distance
                    y_temp += y_distance
                    if 0 <= x_temp < 8 and 0 <= y_temp < 8 and self.board.board[x_temp][y_temp] == player.color:
                        return True
        return False

    def get_available_moves(self, player):
        available_moves = []
        for i in range(8):
            for j in range(8):
                if self.check_direction(i, j, player):
                    available_moves.append((i, j))
        return available_moves

    def get_flipped_pieces(self, x, y, player):
        flipped_pieces = []
        opponent = "W" if player.color == "B" else "B"
        for x_distance, y_distance in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            x_temp, y_temp = x + x_distance, y + y_distance
            temp_flipped = []
            if 0 <= x_temp < 8 and 0 <= y_temp < 8 and self.board.board[x_temp][y_temp] == opponent:
                while 0 <= x_temp < 8 and 0 <= y_temp < 8 and self.board.board[x_temp][y_temp] == opponent:
                    temp_flipped.append((x_temp, y_temp))
                    x_temp += x_distance
                    y_temp += y_distance
                    if 0 <= x_temp < 8 and 0 <= y_temp < 8 and self.board.board[x_temp][y_temp] == player.color:
                        flipped_pieces.extend(temp_flipped)
        return flipped_pieces

    def flip_pieces(self, x, y, flipped_pieces, player):
        self.board.board[x][y] = player.color
        for x_temp, y_temp in flipped_pieces:
            self.board.board[x_temp][y_temp] = player.color