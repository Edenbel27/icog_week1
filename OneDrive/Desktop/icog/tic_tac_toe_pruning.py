def print_board(board):
    for i in range(0, 9, 3):
        print(board[i], "|", board[i+1], "|", board[i+2])


def check_winner(board, player):
    winning_patterns = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # columns
        [0, 4, 8], [2, 4, 6]              # diagonals
    ]
    
    for pattern in winning_patterns:
        if all(board[i] == player for i in pattern):
            return True
    return False

def is_draw(board):
    return all(cell != " " for cell in board)


# Node counters for diagnostics
nodes_prune = 0
nodes_plain = 0


def minimax_prune(board, is_maximizing, alpha, beta):

    if check_winner(board, "X"):
        return -1
    if check_winner(board, "O"):
        return 1
    if is_draw(board):
        return 0
    
    global nodes_prune
    nodes_prune += 1

    if is_maximizing:
        best_score = float('-inf')
        for i in range(9):
            if board[i] == " ":
                board[i] = "O"
                score = minimax_prune(board, False, alpha, beta)
                board[i] = " "
                best_score = max(best_score, score)
                alpha = max(alpha, best_score)
                if beta <= alpha:
                    break

        return best_score

    else:
        best_score = float('inf')
        for i in range(9):
            if board[i] == " ":
                board[i] = "X"
                score = minimax_prune(board, True, alpha, beta)
                board[i] = " "
                best_score = min(best_score, score)
                beta = min(beta, best_score)
                if beta <= alpha:
                    break

        return best_score


def minimax_plain(board, is_maximizing):

    if check_winner(board, "X"):
        return -1
    if check_winner(board, "O"):
        return 1
    if is_draw(board):
        return 0

    global nodes_plain
    nodes_plain += 1

    if is_maximizing:
        best_score = float('-inf')
        for i in range(9):
            if board[i] == " ":
                board[i] = "O"
                score = minimax_plain(board, False)
                board[i] = " "
                best_score = max(best_score, score)
        return best_score
    else:
        best_score = float('inf')
        for i in range(9):
            if board[i] == " ":
                board[i] = "X"
                score = minimax_plain(board, True)
                board[i] = " "
                best_score = min(best_score, score)
        return best_score


def best_move(board):

    global nodes_prune, nodes_plain
    
    nodes_prune = 0
    nodes_plain = 0

    best_score = float('-inf')
    move = -1

    for i in range(9):
        if board[i] == " ":
            board[i] = "O"            
            score_prune = minimax_prune(board, False, float('-inf'), float('inf'))  
            score_plain = minimax_plain(board, False)
            board[i] = " "
            if score_prune > best_score:
                best_score = score_prune
                move = i

    return move, nodes_prune, nodes_plain

guide = [0, 1, 2, 3, 4, 5, 6, 7, 8]
board = [" "] * 9

print("Welcome to Tic Tac Toe!")
print("You are X and the AI is O.")
print("Here's the board guide:")
print_board(guide)
print("_" * 13)
while True:
    print_board(board)
    try:
        user = int(input("Enter your move (0-8): "))
    except ValueError:
        print("Invalid input. Enter a number 0-8.")
        continue
    if user < 0 or user > 8:
        print("Invalid move. Try again.")
        continue
    if board[user] == " ":
        board[user] = "X"
    else:
        print("That square is already taken. Try again.")
        continue

    if check_winner(board, "X"):
        print_board(board)
        print("You win!")
        break

    if is_draw(board):
        print_board(board)
        print("It's a draw!")
        break

    move, nodes_prune, nodes_plain = best_move(board)
    board[move] = "O"
    print(f"AI choose move {move} \n Nodes_alpha_beta: {nodes_prune}, Nodes_plain: {nodes_plain}")
    if check_winner(board, "O"):
        print_board(board)
        print("AI wins!")
        break

    if is_draw(board):
        print_board(board)
        print("It's a draw!")
        break

    if nodes_prune < nodes_plain:
        print("Pruning was effective in reducing the number of nodes evaluated.")