import random

from GameRepresentation import GameBoard
from Player import Player
from ComputerAI import Computer
from Move import Move


class Controller:
    def __init__(self):
        self.game = GameBoard()
        self.current_player = Player
        self.computer_player = Computer
        self.is_player_turn = True
        self.difficulty_level = "medium"
        self.move = Move(self.game.board)

    def color_and_difficulty(self):
        while True:
            color_choice = input("Choose Your Color ('B' or 'W'): ").upper()
            if color_choice in ["B", "W"]:
                self.current_player = Player(color_choice)
                self.computer_player = Computer("W") if color_choice == "B" else Computer("B")

                difficulty_choice = input("Choose Your Difficulty Level ('easy' or 'medium' or 'hard'): ").lower()
                if difficulty_choice in ["easy", "medium", "hard"]:
                    if difficulty_choice == "hard":
                        self.computer_player.set_depth(3)
                    elif difficulty_choice == "medium":
                        self.computer_player.set_depth(2)
                    elif difficulty_choice == "easy":
                        self.computer_player.set_depth(1)
                    
                    break
                else:
                    print("Invalid Difficulty Choice!")
            else:
                print("Invalid Color Choice!")

    def get_user_move(self):
        while True:
            try:
                row = int(input("Enter row (0-7): "))
                col = int(input("Enter column (0-7): "))
                if self.move.is_valid_move(row, col, self.current_player):
                    return row, col
                else:
                    print("Invalid move. Try again.")
            except ValueError:
                print("Invalid move. Try again.")


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
                self.move.move(row, col, self.current_player)
            else:
                print(f"Computer's Turn :")
                coords = self.computer_player.play(self.game)
                if coords is None:
                    print("Computer has no valid moves. Skipping turn.")
                    self.is_player_turn = not self.is_player_turn
                    continue

                row, col = coords
                self.move.move(row, col, self.computer_player)

            # Display the updated board
            print("Updated Board:")
            self.game.print_board()
            print("Scores :")
            score = self.game.get_score()
            # print(f"Black Score = {score["B"]}\nWhite Score = {score['W']}")

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
