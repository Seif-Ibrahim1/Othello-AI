import random

from GameRepresentation import GameBoard
from Player import Player


class Controller:
    def __init__(self):
        self.game = GameBoard()
        self.current_player = Player
        self.computer_player = Player
        self.is_player_turn = True
        self.difficulty_level = "medium"

    def color_and_difficulty(self):
        while True:
            color_choice = input("Choose Your Color ('B' or 'W'): ").upper()
            if color_choice in ["B", "W"]:
                self.current_player = Player(color_choice)
                self.computer_player = Player("W") if color_choice == "B" else Player("B")
            else:
                print("Invalid Color Choice!")

            difficulty_choice = input("Choose Your Difficulty Level ('easy' or 'medium' or 'hard'): ").lower()
            if difficulty_choice in ["easy", "medium", "hard"]:
                self.difficulty_level = difficulty_choice
                break
            else:
                print("Invalid Difficulty Choice!")

    def get_user_move(self):
        while True:
            try:
                row = int(input("Enter row (0-7): "))
                col = int(input("Enter column (0-7): "))
                if self.game.is_valid_move(row, col, self.current_player):
                    return row, col
                else:
                    print("Invalid move. Try again.")
            except ValueError:
                print("Invalid move. Try again.")

    def get_computer_move(self):
        while True:
            if self.difficulty_level == "easy":
                return self.get_easy_move()
            elif self.difficulty_level == "medium":
                return self.get_medium_move()
            elif self.difficulty_level == "hard":
                # by using alpha-beta code
                return self.get_hard_move()

    def get_easy_move(self):
        valid_moves = []
        for x in range(8):
            for y in range(8):
                if self.game.is_valid_move(x, y, self.computer_player):
                    valid_moves.append((x, y))
        # select any random valid move
        return random.choice(valid_moves) if valid_moves else None

    def get_medium_move(self):
        valid_moves = []
        for x in range(8):
            for y in range(8):
                if self.game.is_valid_move(x, y, self.current_player):
                    valid_moves.append((x, y))
        # will add heuristic function
        return valid_moves[0] if valid_moves else None

    def play(self):
        print("Welcome To Othello Game!")
        # first choose the color and the difficulty level
        self.color_and_difficulty()
        print("The Initial Board:")
        self.game.print_board()
        # then start the game
        while not self.game.is_game_over():
            if self.is_player_turn:
                print(f"Your Turn :")
                row, col = self.get_user_move()
                self.game.move(row, col, self.current_player)
            else:
                print(f"Computer's Turn :")
                row, col = self.get_computer_move()
                self.game.move(row, col, self.computer_player)

            # Display the updated board
            print("Updated Board:")
            self.game.print_board()
            print("Scores :")
            score = self.game.get_score()
            print(f"Black Score = {score["B"]}\nWhite Score = {score['W']}")

            # change turns
            self.is_player_turn = not self.is_player_turn

        # game is over
        winner = self.game.get_winner()
        if winner == "Draw":
            print("It's a Draw!")
        else:
            if self.current_player == "W" and winner == "W":
                print("YOU'RE THE WINNER!")
            elif self.current_player == "B" and winner == "B":
                print("YOU'RE THE WINNER!")
            else:
                print("COMPUTER IS THE WINNER!")


controller = Controller()
controller.play()
