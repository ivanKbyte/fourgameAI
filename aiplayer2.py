import random

rows = 6
cols = 7

def collumn_check(board, col):
    if board[rows-1][col] == 0:
        return True
    else:
        return False
    
def possible_moves(board):
    pos_moves = []
    for c in range(cols):
        if collumn_check(board, c):
            pos_moves.append(c)
    return pos_moves

# To find where circle should be put so it won't be floating in air
def landing_place(board, col):
    for r in range(rows):
        if board[r][col] == 0:  #starts from buttom and first empty section will be the landing spot
            return r
    return -1


# Checking if three colors are in the row, col or diagonal
def win_move(board, piece):
    for c in range(cols):
        for r in range(rows - 3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True
    for r in range(rows):
        for c in range(cols - 3):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True

    for r in range(3, rows):
        for c in range(cols - 3):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True
    for r in range(rows - 3):
        for c in range(cols - 3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True
    return False


# Finding move that can end the game in one move
def searching_win_move(board, moves, me, opp):
    for c in moves:
        r = landing_place(board, c)
        if r == -1:
            continue
        
        #making clone of board for move simulation
        board_clone = [row[:] for row in board]
        board_clone[r][c] = me

        #Finding this win move
        if win_move(board_clone, me):
            return c        
    return -1


# it finds combination and gives score depending on combination of four it have
def score_section(window, me, opp):
    score = 0 
    if window.count(me) == 4:
        score = score + 100000
    elif window.count(me) == 3 and window.count(0) == 1:
        score = score + 30
    elif window.count(me) == 2 and window.count(0) == 2:
        score = score + 10
    if window.count(opp) == 3 and window.count(0) == 1:
        score = score - 60
    return score

def score_position(board, me, opp):
    score = 0

    # Counts how many pieces are in the center column because it is best position
    center_col = cols // 2
    center_count = 0
    for r in range(rows):
        if board[r][center_col] == me:
            center_count += 1
    score = score + center_count * 3

    # We check all possible groups of four and rate them
    #Horizontal
    for r in range(rows):
        for c in range(cols - 3):
            window = []
            for i in range(4): 
                window.append(board[r][c + i])
            score = score + score_section(window, me, opp)

    #Vertical
    for c in range(cols):
        for r in range(rows - 3):
            window = []
            for i in range(4): 
                window.append(board[r + i][c])
            score = score + score_section(window, me, opp)

    #diagonal right
    for r in range(rows - 3):
        for c in range(cols - 3):
            window = []
            for i in range(4):
                window.append(board[r + i][c + i])
            score = score + score_section(window, me, opp)

    #diagonal left
    for r in range(3, rows):
        for c in range(cols - 3):
            window = []
            for i in range(4):
                window.append(board[r - i][c + i])
            score = score + score_section(window, me, opp)

    return score


# check if game is finished
def is_terminal(board, me, opp):
    if win_move(board, me):
        return True
    if win_move(board, opp):
        return True
    if len(possible_moves(board)) == 0:
        return True
    return False


# minimax with alpha-beta pruning
def alphabeta(board, depth, alpha, beta, maximizing, me, opp):
    moves = possible_moves(board)

    # when we reach end of search or game is over
    if depth == 0 or is_terminal(board, me, opp):
        if win_move(board, me):
            return None, 999999  # big positive score if I win
        elif win_move(board, opp):
            return None, -999999 # big negative score if opponent wins
        else:
            return None, score_position(board, me, opp)  # normal evaluation

    # if it is my turn (maximize my result)
    if maximizing:
        best_val = -999999
        best_col = random.choice(moves)  # start with random column
        for col in moves:
            r = landing_place(board, col)
            if r == -1:
                continue
            board[r][col] = me
            _, value = alphabeta(board, depth-1, alpha, beta, False, me, opp)
            board[r][col] = 0
            if value > best_val:
                best_val = value
                best_col = col
            if best_val > alpha:
                alpha = best_val
            if alpha >= beta:
                break   # cut branch
        return best_col, best_val

    # if it is opponent turn (minimize my result)
    else:
        best_val = 999999
        best_col = random.choice(moves)
        for col in moves:
            r = landing_place(board, col)
            if r == -1:
                continue
            board[r][col] = opp
            _, value = alphabeta(board, depth-1, alpha, beta, True, me, opp)
            board[r][col] = 0
            if value < best_val:
                best_val = value
                best_col = col
            if best_val < beta:
                beta = best_val
            if alpha >= beta:
                break   # cut branch
        return best_col, best_val


def aiplayer1(board):
    moves = possible_moves(board)
    if len(moves) == 0:
        return 0

    # Find out if I am player 1 or player 2
    num1 = 0
    for r in range(rows):
        for c in range(cols):
            if board[r][c] == 1:
                num1 = num1 + 1

    num2 = 0
    for r in range(rows):
        for c in range(cols):
            if board[r][c] == 2:
                num2 = num2 + 1

    if num1 <= num2:
        me = 1
        opp = 2
    else:
        me = 2
        opp = 1

    # Find out if game can be ended in the next move
    victory_move = searching_win_move(board, moves, me, opp)
    if victory_move != -1:
        return victory_move
    block_move = searching_win_move(board, moves, opp, me)
    if block_move != -1:
        return block_move

    col, _ = alphabeta(board, depth=4, alpha=-9999999, beta=9999999, 
                     maximizing=True, me=me, opp=opp)
    return col if col is not None else random.choice(moves)
