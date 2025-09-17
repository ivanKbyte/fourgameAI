import random
import math

# I have referenced three web sources for three of the concepts used in this algoritmh for the AI player. Although no code was copied directly, I have used these sources to understand the concepts and implement them in my own way!

# custom constants for cleaner code
ROWS_COUNT = 6
COLUMNS_COUNT = 7
DEPTH_OF_SEARCH = 6 # can always be changed!!
CENTERCOLUMN_BOOST = 8

def determine_current_player(board):
    """A small helper function that identifies which player's turn it is based on the piece count"""
    player1_pieces = (board == 1).sum()
    player2_pieces = (board == 2).sum()
    
    if player1_pieces == player2_pieces:
        return 1, 2  # player 1's turn, opponent is player 2
    elif player1_pieces == player2_pieces + 1:
        return 2, 1  # player 2's turn, opponent is player 1
    else:
        return 1, 2  # default case just in case of an incorrect board status

def find_next_row(board, col):
    """Find the next available row in a column"""
    for r in range(ROWS_COUNT):  # check from bottom - row 0, to top - row 5
        if board[r][col] == 0:
            return r
    return None

def place_piece(board, row, col, piece):
    """Create new board state with the piece placed"""
    new_board = board.copy()  # make a duplicate such that original board is not modified
    new_board[row][col] = piece
    return new_board

def check_win(board, piece):
    """
    Check if a player has won the game
    The foundtion for the win logic was taken from Stack Overflow: https://stackoverflow.com/questions/7033165/connect-four-checking-for-a-win; although no code from it was used directly, I got the inspiration from here.
    """
    # go through all positions on the board
    for r in range(ROWS_COUNT):
        for c in range(COLUMNS_COUNT):
            if board[r][c] == piece:
                # check four directions: right, down, negative and positive diagonal
                move_directions = [(0,1), (1,0), (1,1), (1,-1)]
                for dr, dc in move_directions:
                    # check if 4 consecutive pieces exist in that direction
                    if all(0 <= r+i*dr < ROWS_COUNT and 0 <= c+i*dc < COLUMNS_COUNT and 
                          board[r+i*dr][c+i*dc] == piece for i in range(4)):
                        return True
    return False

def evaluate(board, my_piece, enemy_piece):
    """Evaluate the current board position"""
    # check for immediate wins/losses first
    if check_win(board, my_piece):
        return 10000  # if AI wins then maximum score
    if check_win(board, enemy_piece):
        return -10000  # if opponent wins then minimum score
    
    position_score = 0

    # prefer the center column as center pieces create more connection opportunities
    center_pieces = int((board[:, 3] == my_piece).sum())
    position_score += center_pieces * CENTERCOLUMN_BOOST
    
    # evaluate all possible 4-piece sequences for patterns:
    # horizontal sequence (4 consecutive horizontal positions)
    for r in range(ROWS_COUNT):
        for c in range(COLUMNS_COUNT - 3):
            pattern_window = [board[r][c+i] for i in range(4)]
            position_score += rate_window(pattern_window, my_piece, enemy_piece)
    
    # vertical sequence (4 consecutive vertical positions)
    for r in range(ROWS_COUNT - 3):
        for c in range(COLUMNS_COUNT):
            pattern_window = [board[r+i][c] for i in range(4)]
            position_score += rate_window(pattern_window, my_piece, enemy_piece)
    
    # positive diagonal sequence (bottom-left to top-right)
    for r in range(ROWS_COUNT - 3):
        for c in range(COLUMNS_COUNT - 3):
            pattern_window = [board[r+i][c+i] for i in range(4)]
            position_score += rate_window(pattern_window, my_piece, enemy_piece)
    
    # negative diagonal sequence (top-left to bottom-right)
    for r in range(3, ROWS_COUNT):
        for c in range(COLUMNS_COUNT - 3):
            pattern_window = [board[r-i][c+i] for i in range(4)]
            position_score += rate_window(pattern_window, my_piece, enemy_piece)
    
    return position_score

def rate_window(pattern_window, my_piece, enemy_piece):
    """Rate the current four-piece window for evaluation"""
    window_score = 0
    my_count = pattern_window.count(my_piece)
    enemy_count = pattern_window.count(enemy_piece)
    
    # score AI's potential in this window (only if opponent isn't blocking)
    if enemy_count == 0:
        if my_count == 4:
            window_score += 1000    # four in a row should be caught by check_win
        elif my_count == 3:
            window_score += 100     # three in a row evaluates to very strong
        elif my_count == 2:
            window_score += 12      # two in a row evaluates to good potential
    
    # penalize opponent's potential in this window (only if AI isn't blocking)
    if my_count == 0:
        if enemy_count == 4:
            window_score -= 1000    # opponent four in a row
        elif enemy_count == 3:
            window_score -= 120     # opponent three in a row evaluates to urgent threat
        elif enemy_count == 2:
            window_score -= 8       # opponent two in a row evaluates to minor threat
    
    return window_score

def minimax(board, depth, alpha, beta, maximizing, my_piece, enemy_piece):
    """
    Minimax search algorithm with alpha-beta pruning
    Some concepts from the base algorithm concept referenced from GeeksforGeeks minimax tutorial: https://www.geeksforgeeks.org/minimax-algorithm-in-game-theory-set-1-introduction/
    """
    # find all valid moves
    available_moves = [c for c in range(COLUMNS_COUNT) if board[ROWS_COUNT-1][c] == 0]
    game_ended = check_win(board, my_piece) or check_win(board, enemy_piece) or len(available_moves) == 0
    
    # base case when the maximum depth is reached or game over
    if depth == 0 or game_ended:
        if game_ended:
            if check_win(board, my_piece):
                return 10000 - depth, None  # quicker wins preferred
            elif check_win(board, enemy_piece):
                return -10000 + depth, None  # later losses preferred (opponent can mess up)
            else:
                return 0, None  # draw
        else:
            # when the depth limit is reached, the evaluation function is used
            return evaluate(board, my_piece, enemy_piece), None
    
    # move ordering heuristic: try center columns first for better pruning and more options
    # center moves tend to be stronger, so they're likely to cause cutoffs
     # alpha-beta pruning optimization concept from Wikipedia alpha-beta pruning article: https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning

    ordered_moves = sorted(available_moves, key=lambda x: abs(x - 3))
    optimal_move = ordered_moves[0]  # default to first valid move
    
    if maximizing:  # AI's turn - maximize score
        best_value = -math.inf
        for col in ordered_moves:
            row = find_next_row(board, col)
            if row is not None: # ensure that the column is not full
                # pretend to make this move
                test_board = place_piece(board, row, col, my_piece)
                # check recusrively what happens after the opponent responds
                move_value, _ = minimax(test_board, depth-1, alpha, beta, False, my_piece, enemy_piece)
                
                # update best move if this we found a better one
                if move_value > best_value:
                    best_value = move_value
                    optimal_move = col
                
                # alpha-beta pruning (skipping branches that won't matter)
                alpha = max(alpha, move_value)
                if beta <= alpha:  # beta cutoff - opponent won't allow this path
                    break
        return best_value, optimal_move
    
    else:  # opponent's turn - minimize score
        worst_value = math.inf
        for col in ordered_moves:
            row = find_next_row(board, col)
            if row is not None: # ensure that the column is not full
                # pretend that opponent puts their piece here
                test_board = place_piece(board, row, col, enemy_piece)
                # check recusrively what happens after that move
                move_value, _ = minimax(test_board, depth-1, alpha, beta, True, my_piece, enemy_piece)
                
                # opponent wants the lowest score so we keep track of the best move
                if move_value < worst_value:
                    worst_value = move_value
                    optimal_move = col
                
                # alpha-beta pruning (skipping branches that won't matter)
                beta = min(beta, move_value)
                if beta <= alpha:  # beta cutoff - the AI won't allow this path
                    break
        return worst_value, optimal_move

def aiplayer1(board):
    """This is where the AI determines the best move"""
    # validation of the input board format & values
    if board.shape != (ROWS_COUNT, COLUMNS_COUNT) or not ((board >= 0) & (board <= 2)).all():
        raise ValueError("Incorrect board shape or values")
    
    # determine which player the AI is using helper function
    current_player, opposing_player = determine_current_player(board)
    
    # find columns that aren't full yet (checks if top row has space)
    valid_moves = [c for c in range(COLUMNS_COUNT) if board[ROWS_COUNT-1][c] == 0]
    
    # this shouldn't happen in a real game but preferable for error checking
    if not valid_moves:
        raise ValueError("There are no valid moves available")
    
    # tactical check before deep thinking for imrpoved performance
    blocking_move = None # we first check whether we need to block our enemy player
    for col in valid_moves: # each valid move is verified
        row = find_next_row(board, col)
        if row is not None:
            # check for immediate win first
            if check_win(place_piece(board, row, col, current_player), current_player):
                return col
            # check for necessary block
            if check_win(place_piece(board, row, col, opposing_player), opposing_player):
                blocking_move = col
    
    # if AI need to block, do it
    if blocking_move is not None:
        return blocking_move
        
    # run the thinking algorithm to pick the best move
    final_score, best_choice = minimax(board, DEPTH_OF_SEARCH, -math.inf, math.inf, True, current_player, opposing_player) # in short here we run the minimax function and the params are the board, depth, alpha, beta, maximizing player boolean, AI piece, opponent piece
    
    # make sure a valid move is returned (safety check)
    return best_choice if best_choice in valid_moves else valid_moves[0]