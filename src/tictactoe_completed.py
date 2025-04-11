import pygame

# Initialize Pygame.
pygame.init()
# Initialize the screen.
WIDTH, HEIGHT = 600, 600
pygame.display.set_caption('Tic-Tac-Toe')
screen = pygame.display.set_mode((WIDTH, HEIGHT))
# Constants for drawing.
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (200, 0, 0)
LINE_WIDTH = 5
MARGIN = 32
GRID_SIZE = (WIDTH - MARGIN * 2) // 3
# Images for pieces.
x_img = pygame.image.load('x.png')
o_img = pygame.image.load('o.png')
# Scale them to fit inside the grid squares nicely.
x_img = pygame.transform.smoothscale(x_img, (GRID_SIZE - MARGIN, GRID_SIZE - MARGIN))
o_img = pygame.transform.smoothscale(o_img, (GRID_SIZE - MARGIN, GRID_SIZE - MARGIN))
# Initialize the font.
font = pygame.font.SysFont('PixelBasic', 32)

board = [[None] * 3 for _ in range(3)]
choice = None


def reset():
    """Resets the board and choice to their initial states."""
    # Task 1:

    # Declare global variables.
    global board, choice
    # Reset the variables.
    board = [[None] * 3 for _ in range(3)]
    choice = None


def draw_game():
    """Draws the current state of the board (the Xs and Os)."""
    # Task 2:

    # For each row and column, draw an X or O as needed.
    for r in range(3):
        for c in range(3):
            if board[r][c] == 'X':
                draw_x(r, c)
            elif board[r][c] == 'O':
                draw_o(r, c)


def draw_x(row, column):
    """
    Draws an X at the given row and column.

    Parameters:
        row (int): The row to draw X at.
        column (int): The column to draw X at.
    """
    x = column * GRID_SIZE + MARGIN * 1.5
    y = row * GRID_SIZE + MARGIN * 1.5
    screen.blit(x_img, (x, y))


def draw_o(row, column):
    """
    Draws an O at the given row and column.

    Parameters:
        row (int): The row to draw O at.
        column (int): The column to draw O at.
    """
    x = column * GRID_SIZE + MARGIN * 1.5
    y = row * GRID_SIZE + MARGIN * 1.5
    screen.blit(o_img, (x, y))


def user_click():
    """
    Processes a user click. If the game is over, it does nothing. Otherwise, it adds an X
    to the board if the user clicks a valid cell.
    """
    # Task 3:

    # If the game is over, don't process this click.
    if is_game_over(board):
        return
    # Get the position of the mouse and store in x, y.
    x, y = pygame.mouse.get_pos()
    # If the click is within the bounds of the board
    if y > MARGIN and y < HEIGHT - MARGIN and x > MARGIN and x < WIDTH - MARGIN:

        # Min is added here to keep accidental 3s slipping in at the very edges
        row, column = min((y - MARGIN) // GRID_SIZE, 2), min((x - MARGIN) // GRID_SIZE, 2)

        # Check if that cell is empty
        if board[row][column] is None:
            # Set the cell to an X.
            board[row][column] = 'X'
            # If the game is not over, tell the computer to take its turn.
            if not is_game_over(board):
                computer_turn()


def is_game_over(_board):
    """
    Returns whether the game is over, and who won if it is. Returns the symbol of the winner,
    'T' if it's a tie, and None if the game is not over.

    Parameters:
        _board (list): The board that's being checked.
    Returns:
        String: 'X' if the player wins, 'O' if the computer wins, 'T' if it's a tie, and
        None otherwise.
    """
    # Task 4.1

    # Horizontal check.
    # For each row, if all the values are the same and not None, return the winner.
    for r in range(3):
        if all(_board[r][0] is not None and _board[r][c] == _board[r][0] for c in range(3)):
            return _board[r][0]
    # Vertical check.
    # For each column, if all the values are the same and not None, return the winner.
    for c in range(3):
        if all(_board[0][c] is not None and _board[r][c] == _board[0][c] for r in range(3)):
            return _board[0][c]
    # Diagonal Top-Left to Bottom-Right check.
    # If all the values from (0, 0) to (2, 2) are the same and not None, return the winner.
    if all(_board[0][0] is not None and _board[i][i] == _board[0][0] for i in range(3)):
        return _board[0][0]
    # Diagonal Top-Right to Bottom-Left check.
    # If all the values from (0, 2) to (2, 0) are the same and not None, return the winner.
    if all(_board[0][2] is not None and _board[r][2 - r] == _board[0][2] for r in range(3)):
        return _board[0][2]
    # If there is no winner but all cells are filled, return 'T' for a tie.
    if all(_board[r][c] is not None for r in range(3) for c in range(3)):
        return 'T'
    # Otherwise, the game is not over yet!
    return None


def score(_board):
    """
    Returns the score of the given board: -1 if the player wins, 1 if the computer wins, and
    0 if it's a tie.

    Parameters:
        _board (list): The board that's being scored.
    Returns:
        int: The score of the board.
    """
    # Task 4.2

    result = is_game_over(_board)
    # If the player wins.
    if result == 'X':
        return -1
    # If the computer wins.
    elif result == 'O':
        return 1
    # If it's a tie.
    return 0


def get_new_board(_board, move, symbol):
    """
    Creates a duplicate of the board and adds the given move to the new board.

    Parameters:
        _board (list): The board that's being duplicated
        move (tuple): The move to be added to the new board.
        symbol (str): The symbol of the move, either X or O.
    Returns:
        list: The new board with the added move.
    """
    # Task 4.3

    # Create a new empty board.
    new_board = [[None] * 3 for _ in range(3)]
    # For each row and column, copy the values to the new board.
    for r in range(3):
        for c in range(3):
            new_board[r][c] = _board[r][c]
    # Add the move to the new board.
    r, c = move
    new_board[r][c] = symbol
    # Return the board.
    return new_board


def minimax(_board, depth, is_max):
    """
    Calculates the move that either minimizes or maximizes the score of the board. Minimizing is
    generally done to represent the player's possible choice, while maximizing is done to represent
    the computer's best choice to win.

    Recursively calls minimax on the next possible move until the board's state is game over. Then,
    returns the score of the board, 1 for a computer win, -1 for a player win, and 0 for a tie.
    Updates the choice variable as needed which is used by the computer to determine its next move.

    Parameters:
        _board (list): The board that's currently being simulated.
        depth (int): The depth of the search tree.
        is_max (bool): True if the computer's turn, False if the player's turn.

    Returns:
        int: The score of the board after recursively calling moves until the board's state is
        game over.
    """
    # Task 5.1:

    best_value = 0
    best_move = None
    # Declare global variables.
    global choice
    # If the game is over, return the score of the current board.
    if is_game_over(_board):
        return score(_board)
    # Gather all empty cells, which are potential moves.
    moves = [(r, c) for r in range(3) for c in range(3) if _board[r][c] is None]
    # If maximizing the score.
    if is_max:
        # Set best value to the lowest value possible.
        best_value = -1
        # For each possible move.
        for move in moves:
            # Create the new board with the move added.
            new_board = get_new_board(_board, move, 'O')
            # Call the minimax algorithm that minimizes (representing the player's turn).
            value = minimax(new_board, depth + 1, False)
            # If the value from minimax is better than the current best value, update it.
            # Also update the best move which will be used by the computer as it's choice.
            if value > best_value:
                best_value = value
                best_move = move
        # Update the choice variable to the best move
        choice = best_move
        # Return the best score.
        return best_value
    # If minimizing the score.
    else:
        # Set best value to the highest possible score.
        best_value = 1
        # For each possible move.
        for move in moves:
            # Create the new board with the move added.
            new_board = get_new_board(_board, move, 'X')
            # Call the minimax algorithm that maximizes (representing the opponent's turn).
            value = minimax(new_board, depth + 1, True)
            # If the value from minimax is better than the current best value, update it.
            if value < best_value:
                best_value = value
        # Return the best score.
        return best_value


def computer_turn():
    """Initiates the computer's turn by calling the minimax algorithm, then sets the cell to an O."""
    # Task 5.2:

    # Call the minimax algorithm.
    minimax(board, 0, True)
    # Set the cell the computer chooses to an O if the choice is valid.
    if choice is not None:
        r, c = choice
        board[r][c] = 'O'


### Used to run the game, do not modify past this line! ###

def draw():
    """Draws the current board on the screen."""
    # Redraw the background.
    screen.fill(WHITE)
    # Draw the grid.
    draw_grid()
    # Draw game.
    draw_game()
    # Update the screen.
    pygame.display.flip()

def draw_grid():
    """Draws the grid for the board on the screen."""
    for i in range(1, 3):

        # Draw vertical lines
        pygame.draw.line(screen, BLACK, (i * GRID_SIZE + MARGIN, MARGIN), (i * GRID_SIZE + MARGIN, HEIGHT - MARGIN), LINE_WIDTH)
        # Draw horizontal lines
        pygame.draw.line(screen, BLACK, (MARGIN, i * GRID_SIZE + MARGIN), (WIDTH - MARGIN, i * GRID_SIZE + MARGIN), LINE_WIDTH)

reset()
running = True
while running:

    draw()

    for event in pygame.event.get():

        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:

            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:

            user_click()

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:

            reset()


pygame.quit()

