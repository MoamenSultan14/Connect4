import random

ROWS = 6
COLS = 7
WINNING_LENGTH = 4

# Create the game board
board = [[' ' for _ in range(COLS)] for _ in range(ROWS)]

# Checks if a move is valid in the specified column. (True/False)
def is_valid_move(column):
    return board[0][column] == ' '

# Makes a move for the specified player in the given column.
def make_move(column, player):
    for row in range(ROWS-1, -1, -1):
        if board[row][column] == ' ':
            board[row][column] = player
            return row

# Checks if the specified player has won the game (True/False)
def check_win(row, column, player):
    # Check for horizontal win
    for c in range(COLS - WINNING_LENGTH + 1):
        if all(board[row][c+i] == player for i in range(WINNING_LENGTH)):
            return True

    # Check for vertical win
    for r in range(ROWS - WINNING_LENGTH + 1):
        if all(board[r+i][column] == player for i in range(WINNING_LENGTH)):
            return True

    # Check for diagonal win (top-left to bottom-right)
    for r in range(ROWS - WINNING_LENGTH + 1):
        for c in range(COLS - WINNING_LENGTH + 1):
            if all(board[r+i][c+i] == player for i in range(WINNING_LENGTH)):
                return True

    # Check for diagonal win (bottom-left to top-right)
    for r in range(WINNING_LENGTH - 1, ROWS):
        for c in range(COLS - WINNING_LENGTH + 1):
            if all(board[r-i][c+i] == player for i in range(WINNING_LENGTH)):
                return True

    return False

# Checks if the game board is completely filled (True/False)
def is_board_full():
    for row in board:
        if ' ' in row:
            return False
    return True

# Returns a list of valid moves that can be made on the current board
def get_valid_moves():
    return [col for col in range(COLS) if is_valid_move(col)]

# Score a subset of cells for the specified player
def score_subset(subset, player):
    score = 0
    opponent = 'O' if player == 'X' else 'X'

    if subset.count(player) == WINNING_LENGTH:
        score += 10000  # Increase the score for AI's winning move
    elif subset.count(player) == WINNING_LENGTH - 1 and subset.count(' ') == 1:
        score += 1000
    elif subset.count(player) == WINNING_LENGTH - 2 and subset.count(' ') == 2:
        score += 1

    if subset.count(opponent) == WINNING_LENGTH:
        score -= 100
    elif subset.count(opponent) == WINNING_LENGTH - 1 and subset.count(' ') == 1:
        score -= 5
        
    return score

# Considering the centrality of pieces
def score_central_column(board, player):
    central_column_index = int(COLS / 2)  # Get the central column index
    central_column = [row[central_column_index] for row in board]  # Get the central column
    return central_column.count(player) * 3  # Score it


# Score the position of the board for the specified player
def score_position(board, player):
    score = 0

    # Score horizontal
    for r in range(ROWS):
        for c in range(COLS - WINNING_LENGTH + 1):
            subset = board[r][c:c+WINNING_LENGTH]
            score += score_subset(subset, player)

    # Score vertical
    for c in range(COLS):
        for r in range(ROWS - WINNING_LENGTH + 1):
            subset = [board[r+i][c] for i in range(WINNING_LENGTH)]
            score += score_subset(subset, player)

    # Score diagonal (top-left to bottom-right)
    for r in range(ROWS - WINNING_LENGTH + 1):
        for c in range(COLS - WINNING_LENGTH + 1):
            subset = [board[r+i][c+i] for i in range(WINNING_LENGTH)]
            score += score_subset(subset, player)

    # Score diagonal (bottom-left to top-right)
    for r in range(WINNING_LENGTH - 1, ROWS):
        for c in range(COLS - WINNING_LENGTH + 1):
            subset = [board[r-i][c+i] for i in range(WINNING_LENGTH)]
            score += score_subset(subset, player)

    if difficulty == 'hard':    
        # Add central column bonus
        score += score_central_column(board, player)
        
    return score

# Minimax algorithm
def minimax(board, depth, alpha, beta, maximizing_player, row, column):
    valid_moves = get_valid_moves()
    
    if row is not None and column is not None:
        terminal_node = is_board_full() or depth == 0 or check_win(row, column, 'O') or check_win(row, column, 'X')
    else:
            
        terminal_node = is_board_full() or depth == 0

    if terminal_node:
        if check_win(row, column, 'O'):
            return (None, 100000000000000)  # Computer wins
        elif check_win(row, column, 'X'):
            return (None, -10000000000000)  # player wins
        elif depth == 0:  # Maximum search depth reached
            return (None, score_position(board, 'O') - score_position(board, 'X'))  # Evaluate the position
        else:
            return (None, 0)  # Tie game

    if maximizing_player:
        max_score = float('-inf')
        best_move = random.choice(valid_moves)
        
        for move in valid_moves:
            row = make_move(move, 'O')
            score = minimax(board, depth - 1, alpha, beta, False, row, move)[1]
            board[row][move] = ' '

            if score > max_score:
                max_score = score
                best_move = move

            alpha = max(alpha, score)
            if alpha >= beta:
                break

        return best_move, max_score
    else:
        min_score = float('inf')
        best_move = random.choice(valid_moves)

        for move in valid_moves:
            row = make_move(move, 'X')
            score = minimax(board, depth - 1, alpha, beta, True, row, move)[1]
            board[row][move] = ' '

            if score < min_score:
                min_score = score
                best_move = move

            beta = min(beta, score)
            if alpha >= beta:
                break

        return best_move, min_score

# Computer move based on minimax
def computer_move():
    return minimax(board, depth, float('-inf'), float('inf'), True, None, None)[0]


import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
import sys

# Create the GUI
root = tk.Tk()
root.withdraw() 

# Create labels to display the scores
player_score = 0
player2_score = 0
computer_score = 0

# Set initial turn to the player
player_turn = random.choice([True, False])

game_over = False 
fair_turn = not player_turn # Who play's next

# Class to display a dialog for choosing the game mode.
class GameModeDialog(tk.simpledialog.Dialog):
    def __init__(self, parent):
        super().__init__(parent)

    def body(self, master):
        self.title("Game Mode")
        tk.Label(master, text="Choose Game Mode").pack()
        tk.Button(master, text='Player vs Player', command=lambda: self.set_and_exit('pvp')).pack()
        tk.Button(master, text='Player vs Computer', command=lambda: self.set_and_exit('pvc') ).pack()
        self.geometry('300x120')

    def set_and_exit(self, value):
        self.result = value
        self.destroy()

# Class to display a dialog for choosing the difficulty level.
class DifficultyDialog(tk.simpledialog.Dialog):
    def __init__(self, parent):
        super().__init__(parent)

    def body(self, master):
        self.title("Difficulty")
        tk.Label(master, text="Choose Difficulty").pack()
        tk.Button(master, text='Easy', command=lambda: self.set_and_exit('easy'), padx=20).pack()
        tk.Button(master, text='Medium', command=lambda: self.set_and_exit('medium'), padx=9).pack()
        tk.Button(master, text='Hard', command=lambda: self.set_and_exit('hard'), padx=18).pack()
        self.geometry('300x150')

    def set_and_exit(self, value):
        self.result = value
        self.destroy()

# Function to prompt the user to choose the game mode using the GameModeDialog class.
def choose_game_mode():
    game_mode = GameModeDialog(root).result
    if game_mode is None:
        sys.exit(0)  # Stop execution
    return game_mode.lower()

# Function to prompt the user to choose the difficulty level using the DifficultyDialog class.
def choose_difficulty():
    difficulty = DifficultyDialog(root).result
    if difficulty is None:
        sys.exit(0) 
    return difficulty.lower()

# Initialize the game mode
game_mode = choose_game_mode()

difficulty = None
depth = None

# Set depth based on game mode    
if game_mode == 'pvc':   
    # Initialize the game and choose difficulty
    difficulty = choose_difficulty()
    if difficulty == 'easy':
        depth = 1
    elif difficulty == 'medium':
        depth = 3
    elif difficulty == 'hard':
        depth = 5


root.title("Connect4") # Title
# Create a canvas to draw the game board
canvas = tk.Canvas(root, width=700, height=600, bg="blue")
canvas.pack()

# Player score label
player_score_label = tk.Label(root, text="Player score: 0")
player_score_label.pack(side=tk.LEFT)

# Show opponent score label based on the game mode
if game_mode == 'pvc':
    opponent_score_label = tk.Label(root, text="Computer score: 0")
    opponent_score_label.pack(side=tk.RIGHT)
else:
    opponent_score_label = tk.Label(root, text="Player2 score: 0")
    opponent_score_label.pack(side=tk.RIGHT)
    
# Variables to handle the turn timeout
turn_timeout_id = None
player_turn_time_left = 10
player_steps = 0  # Variable to track player's steps
# Create the timer label
timer_label = tk.Label(root, text="")
timer_label.pack(side = tk.BOTTOM)

# Generate a random cell at the start of each game
special_row, special_col = random.randint(0, ROWS-4), random.randint(0, COLS-1)
# Add a variable to keep track of if the player landed on the green cell
landed_on_green = False

# Function to draw the Connect 4 game board on the canvas
def draw_board():
    # Draw the board
    for r in range(ROWS):
        for c in range(COLS):
            color = "black"
            if board[r][c] == 'X':
                color = "red"
            elif board[r][c] == 'O':
                color = "yellow"
            if difficulty == 'medium':    
                if r == special_row and c == special_col:
                    color = "green"  # Special cell color    

            x1 = c * 100
            y1 = r * 100
            x2 = x1 + 100
            y2 = y1 + 100

            canvas.create_oval(x1, y1, x2, y2, fill=color)
# Draw the board
draw_board()

# The computer make its move
def computer():
    
    global computer_score, player_turn, game_over, special_col, special_row
    
    if(player_turn == False):
        
        x = computer_move()
        row = make_move(x, 'O')
        draw_board()

        # Update the GUI immediately
        root.update_idletasks()
        
        if game_mode == 'pvc' and row == special_row and x == special_col:
            special_row, special_col = None, None  # So that no one else can land on the green cell again
            draw_board()  # To remove the green cell from the board
                 

        # Check if the computer has won
        if check_win(row, x, 'O'):
            messagebox.showinfo("Game Over", "Computer wins!")
            game_over = True
            computer_score += 1
            opponent_score_label['text'] = f"Computer score: {computer_score}"
            reset_game()
            return

        # Check if the game is a tie
        elif is_board_full():
            messagebox.showinfo("Game Over", "It's a tie!")
            game_over == True
            reset_game()
            return
        
        # Give the turn to the player
        player_turn = True
        # In hard mode start the timer
        if difficulty == 'hard':           
            start_turn_timer()


# Function to handle the turn timeout
def on_turn_timeout():
    global game_over, computer_score
    global player_turn_time_left, player_turn
    player_turn_time_left -= 1
    if player_turn_time_left <= 0 and not is_board_full():
        
        messagebox.showinfo("Timeout", "You took too long to move. The computer won this round :(")
        game_over = True
        computer_score += 1
        opponent_score_label['text'] = f"Computer score: {computer_score}"
        reset_game()

    elif not player_turn:  # If the player has won the game
        pass
    else:
        update_timer_label()

# Update the timer label with the remaining time for the player's turn
def update_timer_label():
    global turn_timeout_id
    timer_label['text'] = f"Time left: {player_turn_time_left}s"
    turn_timeout_id = root.after(1000, on_turn_timeout)  # Schedule the next call

# Start the timer for the player's turn
def start_turn_timer():
    global player_turn_time_left, turn_timeout_id
    player_turn_time_left = 10
    if turn_timeout_id:
        root.after_cancel(turn_timeout_id)  # Cancel the previous timer
    update_timer_label()
    

if game_mode == 'pvc':
    computer()


# Function to handle player's click on the board
def on_click(event):
    global player_score, computer_score, player_turn, game_over, game_mode, player2_score, player_steps, landed_on_green, special_row, special_col
    x = event.x // 100

    if is_valid_move(x) and player_turn:
        row = make_move(x, 'X')
        draw_board()

        # Check if the player landed on the green cell
        if game_mode == 'pvc' and row == special_row and x == special_col:
            landed_on_green = True  # The player gets another turn
            special_row, special_col = None, None  # So that no one else can land on the green cell again
            draw_board()  # To remove the green cell from the board

        # Update the GUI immediately
        root.update_idletasks()

        # Check if the player has won
        if check_win(row, x, 'X'):
            
            if difficulty == 'hard':                
                root.after_cancel(turn_timeout_id)  # Cancel the timer when game ends
                
            messagebox.showinfo("Game Over", "Player win!!")
            game_over = True
            player_score += 1
            player_score_label['text'] = f"Player score: {player_score}"
            reset_game()
            return

        # Check if the game is a tie
        elif is_board_full():
            
            if difficulty == 'hard':                
                root.after_cancel(turn_timeout_id)  # Cancel the timer when game ends
                
            messagebox.showinfo("Game Over", "It's a tie!")
            game_over == True
            reset_game()
            return

        # Give the turn to the computer/Player2
        player_turn = False

        if landed_on_green and game_mode == 'pvc' and difficulty == 'medium':           
            player_turn = True
            landed_on_green = False

        elif game_mode == 'pvc':
            if difficulty == 'hard' and turn_timeout_id:
                root.after_cancel(turn_timeout_id)  # Cancel the timer
            computer()
            return               
                             
        
    # Handle Player2 move in Player vs. Player mode         
    elif is_valid_move(x) and not player_turn:
        row = make_move(x, 'O')
        draw_board()

        # Update the GUI immediately
        root.update_idletasks()

        # Check if the player has won
        if check_win(row, x, 'O'):
            
            messagebox.showinfo("Game Over", "Player2 win!!")
            game_over = True
            player2_score += 1
            opponent_score_label['text'] = f"Player2 score: {player2_score}"
            reset_game()
            return

        # Check if the game is a tie
        elif is_board_full():
                          
            messagebox.showinfo("Game Over", "It's a tie!")
            game_over == True
            reset_game()
            return

        player_turn = True
        

# Bind the click event to the canvas
canvas.bind("<Button-1>", on_click)

# Reset the game
def reset_game():
    
    global board, player_turn, game_over, fair_turn, player_steps, special_row, special_col
    board = [[' ' for _ in range(COLS)] for _ in range(ROWS)]
    draw_board()  # Redraw the board

    # Who play's next
    if game_over == True:       
        player_turn = fair_turn
        fair_turn = not fair_turn
        game_over = False
        # Generate a random cell at the start of each game
        special_row, special_col = random.randint(0, ROWS-4), random.randint(0, COLS-1)
        draw_board()
    else:
        # Don't change the turn if the game did't end
        player_turn = not fair_turn      
    # In hard mode start the timer
    if player_turn == True and difficulty == 'hard':
        start_turn_timer()
        
    if game_mode == 'pvc':
        # If computer turn make a move        
        computer()


# Create a restart button
reset_button = tk.Button(root, text="Restart", command=reset_game)
reset_button.pack()
root.deiconify()
root.mainloop()

