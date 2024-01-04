# Tic Tac Toe game with AI using the minimax algorithm
# Developed by RebberChicken

import tkinter as tk
from tkinter import ttk, messagebox
from ttkthemes import ThemedStyle

def is_winner(board, player):
    """Checks if a player has won the game."""
    for i in range(3):
        if all(board[i][j] == player for j in range(3)) or \
           all(board[j][i] == player for j in range(3)):
            return True # Check rows and columns
    if all(board[i][i] == player for i in range(3)) or \
       all(board[i][2 - i] == player for i in range(3)):
        return True # Check diagonals
    return False # No winner

def is_board_full(board):
    """Checks if the game board is full."""
    return all(board[i][j] != ' ' for i in range(3) for j in range(3))

def get_empty_cells(board):
    """Gets a list of empty cells on the game board."""
    return [(i, j) for i in range(3) for j in range(3) if board[i][j] == ' ']

def minimax(board, depth, maximizing_player):
    """Minimax algorithm for the AI to make optimal moves."""
    if is_winner(board, 'O'): # AI wins
        return -1
    if is_winner(board, 'X'): # Player wins
        return 1
    if is_board_full(board): # Tie
        return 0

    if maximizing_player:
        max_eval = float('-inf')
        for i, j in get_empty_cells(board): # Try all possible moves
            board[i][j] = 'X' # Make move
            eval = minimax(board, depth + 1, False) # Opponent's turn
            board[i][j] = ' ' # Undo move
            max_eval = max(max_eval, eval) # Choose the maximum value
        return max_eval # Return the maximum value
    else: # Minimizing player
        min_eval = float('inf')
        for i, j in get_empty_cells(board):
            board[i][j] = 'O' # Make move
            eval = minimax(board, depth + 1, True) # Player's turn
            board[i][j] = ' ' # Undo move
            min_eval = min(min_eval, eval) # Choose the minimum value
        return min_eval # Return the minimum value

def get_best_move(board):
    """Gets the best move for the AI using the minimax algorithm."""
    best_val = float('-inf')
    best_move = None
    for i, j in get_empty_cells(board):
        board[i][j] = 'X'
        move_val = minimax(board, 0, False)
        board[i][j] = ' '
        if move_val > best_val:
            best_move = (i, j)
            best_val = move_val
    return best_move

class TicTacToeApp:
    def __init__(self, master):
        self.master = master
        master.title("Tic Tac Toe")

        # Set theme
        style = ThemedStyle(master)
        style.set_theme("plastik")
 
        self.buttons = [[None for _ in range(3)] for _ in range(3)] # Create 3x3 grid for buttons

        for i in range(3): # Create buttons
            for j in range(3):
                self.buttons[i][j] = ttk.Button(master, text='', command=lambda row=i, col=j: self.make_move(row, col))
                self.buttons[i][j].grid(row=i, column=j, sticky='nsew', ipadx=40, ipady=80)

        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.player_turn = True  # True for Player, False for AI

        # Configures grid weights
        for i in range(3):
            master.grid_rowconfigure(i, weight=1)
            master.grid_columnconfigure(i, weight=1)

        # Set button font
        style.configure("TButton", font=('Helvetica', 16)) 

    def make_move(self, row, col):
        """Handle a player's move and the AI's response."""
        if self.board[row][col] == ' ' and self.player_turn: # Check if the move is valid
            self.board[row][col] = 'O' # Player's move
            self.buttons[row][col].config(text='O', state=tk.DISABLED) # Disable button
            self.player_turn = not self.player_turn # Switch turns

            if is_winner(self.board, 'O'): # Check for a winner
                self.show_message("Congratulations! You win!") # Show game over message
                self.reset_game()
            elif is_board_full(self.board): # Check for a tie
                self.show_message("It's a tie!")
                self.reset_game()
            else: # AI's turn
                self.ai_move()

    def ai_move(self):
        """Make the AI's move."""
        ai_row, ai_col = get_best_move(self.board) # Get the AI's move
        self.board[ai_row][ai_col] = 'X' # Make the move
        self.buttons[ai_row][ai_col].config(text='X', state=tk.DISABLED) # Disable button
        self.player_turn = not self.player_turn # Switch turns

        if is_winner(self.board, 'X'): # Check for a winner
            self.show_message("AI wins! Better luck next time.")
            self.reset_game()
        elif is_board_full(self.board): # Check for a tie
            self.show_message("It's a tie!")
            self.reset_game()

    def show_message(self, message): # Show a message box
        """Display a game over message."""
        messagebox.showinfo("Game Over", message)

    def reset_game(self): # Resets the game
        """Reset the game state.""" 
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text='', state=tk.NORMAL)
                self.board[i][j] = ' '
        self.player_turn = True

if __name__ == "__main__": # Run the game
    root = tk.Tk()
    app = TicTacToeApp(root)
    root.mainloop()

