import tkinter as tk
from tkinter import messagebox, OptionMenu
from GameRepresentation import GameBoard
from Player import Player
from ComputerAI import Computer
from Move import Move

class OthelloGUI:
    def __init__(self, master):
        self.master = master
        master.title("Othello Game")
        master.geometry("850x900")
        master.config(bg="#0e2137")  # Dark blue background color

        self.game = GameBoard()
        self.current_player = None
        self.computer_player = None
        self.is_player_turn = True  # By default, player starts
        self.move = Move(self.game.board)
        self.game_over = False

        self.color_label = tk.Label(master, text="Choose Your Color:", font=("Helvetica", 30), bg="#0e2137", fg="white")
        self.color_label.grid(row=0, column=0, padx=20, pady=10, sticky="ew")

        self.difficulty_label = tk.Label(master, text="Choose Your Difficulty Level:", font=("Helvetica", 30), bg="#0e2137", fg="white")
        self.difficulty_label.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

        self.color_var = tk.StringVar(master)
        self.color_var.set("Black")
        self.color_menu = OptionMenu(master, self.color_var, "Black", "White")
        self.color_menu.config(font=("Helvetica", 24), bg="#0e2137", fg="white", width=10)  # Large dropdown items
        self.color_menu.grid(row=0, column=1, padx=20, pady=10, sticky="ew")

        self.difficulty_var = tk.StringVar(master)
        self.difficulty_var.set("Medium")
        self.difficulty_menu = OptionMenu(master, self.difficulty_var, "Easy", "Medium", "Hard")
        self.difficulty_menu.config(font=("Helvetica", 24), bg="#0e2137", fg="white", width=10)  # Large dropdown items
        self.difficulty_menu.grid(row=1, column=1, padx=20, pady=10, sticky="ew")

        self.submit_button = tk.Button(master, text="Start Game", command=self.start_game, font=("Helvetica", 24))
        self.submit_button.grid(row=2, column=0, columnspan=2, padx=20, pady=10, sticky="ew")

        self.board_canvas = tk.Canvas(master, width=800, height=800, bg="#0e2137")  # Dark blue table color
        self.board_canvas.grid(row=3, column=0, columnspan=2, padx=20, pady=10, sticky="nsew")
        self.board_buttons = [[None] * 8 for _ in range(8)]
        self.available_moves = []  # List to store the IDs of available move indicators

        self.info_label = tk.Label(master, text="", font=("Helvetica", 24), bg="#0e2137", fg="white")
        self.info_label.grid(row=4, column=0, columnspan=2, padx=20, pady=10, sticky="ew")

        # Hide the board initially
        self.board_canvas.grid_remove()

    def start_game(self):
        color_choice = self.color_var.get()
        difficulty_choice = self.difficulty_var.get()

        if color_choice == "Black":
            self.current_player = Player("B")
            self.computer_player = Computer("W")
        else:
            self.current_player = Player("W")
            self.computer_player = Computer("B")

        if difficulty_choice == "Hard":
            self.computer_player.set_depth(5)
        elif difficulty_choice == "Medium":
            self.computer_player.set_depth(3)
        elif difficulty_choice == "Easy":
            self.computer_player.set_depth(1)

        if self.current_player == Player("W"):
            self.is_player_turn = False

        # Remove color and difficulty selection widgets
        self.color_label.grid_remove()
        self.color_menu.grid_remove()
        self.difficulty_label.grid_remove()
        self.difficulty_menu.grid_remove()
        self.submit_button.grid_remove()

        # Show the game board
        self.board_canvas.grid()

        self.create_board_buttons()

        self.update_board_display()
        if not self.is_player_turn:
            self.computer_play()

    def create_board_buttons(self):
        cell_size = 100
        for row in range(8):
            for col in range(8):
                x0, y0 = col * cell_size, row * cell_size
                x1, y1 = x0 + cell_size, y0 + cell_size
                self.board_canvas.create_rectangle(x0, y0, x1, y1, outline="black", fill="#0e2137")
                self.board_buttons[row][col] = self.board_canvas.create_oval(x0 + 5, y0 + 5, x1 - 5, y1 - 5, fill="#0e2137")
                self.board_canvas.tag_bind(self.board_buttons[row][col], "<Button-1>",
                                        lambda event, row=row, col=col: self.make_move(row, col))

    def make_move(self, row, col):
        if self.is_player_turn:
            if self.move.is_valid_move(row, col, self.current_player):
                self.move.move(row, col, self.current_player)
                self.is_player_turn = False
                self.update_board_display()
                self.check_game_over()
                if not self.game_over:
                    self.computer_play()
            else:
                self.show_alert("Invalid move. Try again.")

    def computer_play(self):
        if not self.game.is_game_over():
            coords = self.computer_player.play(self.game)
            if coords is not None:
                row, col = coords
                self.move.move(row, col, self.computer_player)
                self.is_player_turn = True
                self.update_board_display()
                self.check_game_over()
                if not self.game_over and not self.move.get_available_moves(self.current_player):
                    self.show_alert("You have no valid moves. Skipping turn.")
                    self.computer_play()
            else:
                self.show_alert("Computer has no valid moves. Skipping turn.")
                self.is_player_turn = True
                self.update_board_display()
                self.check_game_over()

    def check_game_over(self):
        if self.game.is_game_over() or (not self.move.get_available_moves(self.current_player) and not self.move.get_available_moves(self.computer_player)):
            self.game_over = True
            self.disable_board_buttons()
            winner = self.game.get_winner()
            if winner == "Draw":
                self.show_alert("It's a draw!")
            elif winner == self.current_player.color:
                self.show_alert("YOU'RE THE WINNER!")
            else:
                self.show_alert("COMPUTER IS THE WINNER!")

    def disable_board_buttons(self):
        self.board_canvas.unbind("<Button-1>")

    def update_board_display(self):
        # Reset available moves
        for move_id in self.available_moves:
            self.board_canvas.delete(move_id)
        self.available_moves = []

        for row in range(8):
            for col in range(8):
                if self.game.board[row][col] == "B":
                    self.board_canvas.itemconfig(self.board_buttons[row][col], fill="black")
                elif self.game.board[row][col] == "W":
                    self.board_canvas.itemconfig(self.board_buttons[row][col], fill="white")
                else:
                    self.board_canvas.itemconfig(self.board_buttons[row][col], fill="#0e2137")  # Dark blue for empty cells

        # Highlight available moves
        available_moves = self.move.get_available_moves(self.current_player)
        for move in available_moves:
            row, col = move
            x, y = col * 100, row * 100
            radius = 40  # Adjust the radius of the circle
            move_id = self.board_canvas.create_oval(x + 50 - radius, y + 50 - radius, x + 50 + radius, y + 50 + radius,
                                                    outline="dark gray", width=5)  # Change the color and width here
            self.available_moves.append(move_id)

    def update_info_label(self, message):
        self.info_label.config(text=message)

    def show_alert(self, message):
        messagebox.showinfo("Alert", message)

root = tk.Tk()
othello_gui = OthelloGUI(root)
root.mainloop()
