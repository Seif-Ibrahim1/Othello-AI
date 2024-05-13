import math
from GameRepresentation import GameBoard
from Player import Player
class Computer(Player):
    def __init__(self, color, depth=3):
        super().__init__(color)
        self.depth = depth
        self.played = None

    def alpha_beta(self, board, depth, alpha, beta, maximizing):
        if depth == 0 or board.is_game_over():
            if maximizing:
                return board.get_utility(self)
            else:
                return board.get_utility(board.player1 if self.color == board.player2.color else board.player2)    # return valuation of position

        if maximizing:
            maxVal = -math.inf
            available_moves = board.getAvailableMoves(self)
            print("Available moves: ", available_moves)
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

            if maxVal != -math.inf:  
                self.played = played_moves.get(maxVal, None)
            return maxVal
    
        else:
            otherPlayer = board.player1 if self.color == board.player2.color else board.player2
            minVal = math.inf
            available_moves = board.getAvailableMoves(otherPlayer)
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
        
    def set_depth(self, depth):
        self.depth = depth
        
    def play(self, board):
        tmpBoard = GameBoard()
        tmpBoard.board = board.board.copy()
        tmpBoard.player1 = board.player1
        tmpBoard.player2 = board.player2

        self.alpha_beta(tmpBoard, self.depth, -math.inf, math.inf, True)
        print("Computer played: ", self.played)
        return self.played