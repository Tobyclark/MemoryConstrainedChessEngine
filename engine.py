import chess
import chess.engine


# Piece value tables for evaluation
# each table is a 8x8 array, where the index is the value of the given piece on that square
PAWN_TABLE = [
    0,  0,  0,  0,  0,  0,  0,  0,
    50, 50, 50, 50, 50, 50, 50, 50,
    10, 10, 20, 30, 30, 20, 10, 10,
    5,  5, 10, 25, 25, 10,  5,  5,
    0,  0,  0, 20, 20,  0,  0,  0,
    5, -5,-10,  0,  0,-10, -5,  5,
    5, 10, 10,-20,-20, 10, 10,  5,
    0,  0,  0,  0,  0,  0,  0,  0
]

KNIGHTS_TABLE = [
    -50,-40,-30,-30,-30,-30,-40,-50,
    -40,-20,  0,  0,  0,  0,-20,-40,
    -30,  0, 10, 15, 15, 10,  0,-30,
    -30,  5, 15, 20, 20, 15,  5,-30,
    -30,  0, 15, 20, 20, 15,  0,-30,
    -30,  5, 10, 15, 15, 10,  5,-30,
    -40,-20,  0,  5,  5,  0,-20,-40,
    -50,-40,-30,-30,-30,-30,-40,-50
]

BISHOPS_TABLE = [
    -20,-10,-10,-10,-10,-10,-10,-20,
    -10,  0,  0,  0,  0,  0,  0,-10,
    -10,  0,  5, 10, 10,  5,  0,-10,
    -10,  5,  5, 10, 10,  5,  5,-10,
    -10,  0, 10, 10, 10, 10,  0,-10,
    -10, 10, 10, 10, 10, 10, 10,-10,
    -10,  5,  0,  0,  0,  0,  5,-10,
    -20,-10,-10,-10,-10,-10,-10,-20
]

ROOKS_TABLE = [
    0,  0,  0,  0,  0,  0,  0,  0,
    5, 10, 10, 10, 10, 10, 10,  5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    0,  0,  0,  5,  5,  0,  0,  0
]

QUEENS_TABLE = [
    -20,-10,-10, -5, -5,-10,-10,-20,
    -10,  0,  0,  0,  0,  0,  0,-10,
    -10,  0,  5,  5,  5,  5,  0,-10,
    -5,  0,  5,  5,  5,  5,  0, -5,
    0,  0,  5,  5,  5,  5,  0, -5,
    -10,  5,  5,  5,  5,  5,  0,-10,
    -10,  0,  5,  0,  0,  0,  0,-10,
    -20,-10,-10, -5, -5,-10,-10,-20
]

KINGS_TABLE = [
    -50,-40,-30,-20,-20,-30,-40,-50,
    -30,-20,-10,  0,  0,-10,-20,-30,
    -30,-10, 20, 30, 30, 20,-10,-30,
    -30,-10, 30, 40, 40, 30,-10,-30,
    -30,-10, 30, 40, 40, 30,-10,-30,
    -30,-10, 20, 30, 30, 20,-10,-30,
    -30,-30,  0,  0,  0,  0,-30,-30,
    -50,-30,-30,-30,-30,-30,-30,-50
]

# evaluation function for the board
# count the value of each piece and add different values for checkmate and stalemate
def evaluate(board):
    boardvalue = 0
    
    wp = len(board.pieces(chess.PAWN, chess.WHITE))
    bp = len(board.pieces(chess.PAWN, chess.BLACK))
    wn = len(board.pieces(chess.KNIGHT, chess.WHITE))
    bn = len(board.pieces(chess.KNIGHT, chess.BLACK))
    wb = len(board.pieces(chess.BISHOP, chess.WHITE))
    bb = len(board.pieces(chess.BISHOP, chess.BLACK))
    wr = len(board.pieces(chess.ROOK, chess.WHITE))
    br = len(board.pieces(chess.ROOK, chess.BLACK))
    wq = len(board.pieces(chess.QUEEN, chess.WHITE))
    bq = len(board.pieces(chess.QUEEN, chess.BLACK))
    
    pawn_sum = sum([PAWN_TABLE[i] for i in board.pieces(chess.PAWN, chess.WHITE)])
    pawn_sum = pawn_sum + sum([-PAWN_TABLE[chess.square_mirror(i)] for i in board.pieces(chess.PAWN, chess.BLACK)])
    knight_sum = sum([KNIGHTS_TABLE[i] for i in board.pieces(chess.KNIGHT, chess.WHITE)])
    knight_sum = knight_sum + sum([-KNIGHTS_TABLE[chess.square_mirror(i)] for i in board.pieces(chess.KNIGHT, chess.BLACK)])
    bishop_sum = sum([BISHOPS_TABLE[i] for i in board.pieces(chess.BISHOP, chess.WHITE)])
    bishop_sum = bishop_sum + sum([-BISHOPS_TABLE[chess.square_mirror(i)] for i in board.pieces(chess.BISHOP, chess.BLACK)])
    rook_sum = sum([ROOKS_TABLE[i] for i in board.pieces(chess.ROOK, chess.WHITE)]) 
    rook_sum = rook_sum + sum([-ROOKS_TABLE[chess.square_mirror(i)] for i in board.pieces(chess.ROOK, chess.BLACK)])
    queens_sum = sum([QUEENS_TABLE[i] for i in board.pieces(chess.QUEEN, chess.WHITE)]) 
    queens_sum = queens_sum + sum([-QUEENS_TABLE[chess.square_mirror(i)] for i in board.pieces(chess.QUEEN, chess.BLACK)])
    kings_sum = sum([KINGS_TABLE[i] for i in board.pieces(chess.KING, chess.WHITE)]) 
    kings_sum = kings_sum + sum([-KINGS_TABLE[chess.square_mirror(i)] for i in board.pieces(chess.KING, chess.BLACK)])

    material = 100 * (wp - bp) + 300 * (wn - bn) + 300 * (wb - bb) + 500 * (wr - br) + 900 * (wq - bq)
    
    boardvalue = material + pawn_sum + knight_sum + bishop_sum + rook_sum + queens_sum + kings_sum
    
    return boardvalue

# determine the best move in a given position using minimax with a given depth
def _determine_best_move(board, is_white, depth = 6):
    best_move = -100000 if is_white else 100000
    best_final = None
    for move in board.legal_moves:
        board.push(move)
        value = minimax(depth - 1, board, -10000, 10000, not is_white)
        board.pop()
        if (is_white and value > best_move) or (not is_white and value < best_move):
            best_move = value
            best_final = move
    return best_final

def minimax(depth, board, alpha, beta, is_maximizing):
    if depth <= 0 or board.is_game_over():
        return evaluate(board)
    
    # Null move pruning
    if depth >= 2 and not is_maximizing:  # Only apply for minimizing player
        board.push(chess.Move.null())
        value = -minimax(depth - 1 - 2, board, -beta, -beta + 1, not is_maximizing)  # Depth reduced by an extra one
        board.pop()
        if value >= beta:
            return beta

    if is_maximizing:
        best_move = -100000
        for move in board.legal_moves:
            board.push(move)
            value = minimax(depth - 1, board, alpha, beta, False)
            board.pop()
            best_move = max(best_move, value)
            alpha = max(alpha, best_move)
            if beta <= alpha:
                break
        return best_move
    else:
        best_move = 100000
        for move in board.legal_moves:
            board.push(move)
            value = minimax(depth - 1, board, alpha, beta, True)
            board.pop()
            best_move = min(best_move, value)
            beta = min(beta, best_move)
            if beta <= alpha:
                break
        return best_move

# run a REPL loop to play chess against the engine
if __name__ == '__main__':
    board = chess.Board()

    is_white = input('Will you be playing as white or black (white/black)? ').lower()[0] == "w"

    print(f'The board is:')
    print(board)

    if is_white:
        while not board.is_game_over():
            print()
            while True:
                try:
                    move = board.parse_san(input('Enter your move: '))
                except ValueError:
                    print(f'That move is not valid')
                    continue
                break
            board.push(move)

            move = _determine_best_move(board, False)
            board.push(move)

            print(f'Black made the move: {move}')
            print(f'= Board State =')
            print(board)
    else:
        while not board.is_game_over():
            move = _determine_best_move(board, True)
            board.push(move)

            print(f'White made the move: {move}' )
            print(f'= Board State =')
            print(board)
            while True:
                try:
                    move = board.parse_san(input('Enter your move: '))
                except ValueError:
                    print(f'That is not a valid move!')
                    continue
                break
            board.push(move)

    print(f'The game is over!')
