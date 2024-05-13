import math
from GameRepresentation import GameBoard
from Player import Player
class Computer(Player):
    def __init__(self, color, depth=1):
        super().__init__(color)
        self.depth = depth

    def alpha_beta(self, board, depth, alpha, beta, maximizing):
        if depth == 0 or board.is_game_over():
            return 1     # return valuation of position

        if maximizing:
            maxVal = -math.inf
            available_moves = []
            for i in range(8):
                for j in range(8):
                    if board.is_valid_move(i, j, self):
                        available_moves.append((i, j))

            played_moves = {}
            for move in available_moves:
                tmpBoard = GameBoard()
                tmpBoard = board
                # copy the ND array by value
                tmpBoard.board = board.board.copy()
                tmpBoard.move(move[0], move[1], self)
                val = self.alpha_beta(tmpBoard, depth - 1, alpha, beta, False)
                played_moves[val] = move
                maxVal = max(maxVal, val)
                alpha = max(alpha, val)
                if beta <= alpha:
                    break
            self.played = move
            return maxVal
    
        else:
            otherPlayer = board.player1 if self.color == board.player2.color else board.player2
            minVal = math.inf
            available_moves = []
            for i in range(8):
                for j in range(8):
                    if self.board.is_valid_move(i, j, otherPlayer):
                        available_moves.append((i, j))
            for move in available_moves:
                tmpBoard = GameBoard()
                tmpBoard = board
                # copy the ND array by value
                tmpBoard.board = board.board.copy()
                tmpBoard.move(move[0], move[1], otherPlayer)
                val = self.alpha_beta(tmpBoard, depth - 1, alpha, beta ,True)
                minVal = min(minVal, val)
                beta = min(beta, val)
                if beta <= alpha:
                    break
            return minVal
        
    def play(self, board):
        self.alpha_beta(board, self.depth, -math.inf, math.inf, True)
        return self.played