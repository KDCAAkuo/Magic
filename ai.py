import math

BLACK = 1
WHITE = 2

# 6×6の初期ボード
board = [
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 1, 2, 0, 0],
    [0, 0, 2, 1, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
]

# 評価関数用の重み (corner, edge, and center values)
evaluation_weights = [
    [100, -20, 10, 10, -20, 100],
    [-20, -50, 1, 1, -50, -20],
    [10, 1, 5, 5, 1, 10],
    [10, 1, 5, 5, 1, 10],
    [-20, -50, 1, 1, -50, -20],
    [100, -20, 10, 10, -20, 100],
]

def can_place_x_y(board, stone, x, y):
    if board[y][x] != 0:
        return False

    opponent = 3 - stone
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        found_opponent = False

        while 0 <= nx < len(board[0]) and 0 <= ny < len(board) and board[ny][nx] == opponent:
            nx += dx
            ny += dy
            found_opponent = True

        if found_opponent and 0 <= nx < len(board[0]) and 0 <= ny < len(board) and board[ny][nx] == stone:
            return True

    return False

def make_move(board, stone, x, y):
    """ボードに石を置き、ひっくり返す処理を行う。
    """
    board[y][x] = stone
    opponent = 3 - stone
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        flippable_positions = []

        while 0 <= nx < len(board[0]) and 0 <= ny < len(board) and board[ny][nx] == opponent:
            flippable_positions.append((nx, ny))
            nx += dx
            ny += dy

        if flippable_positions and 0 <= nx < len(board[0]) and 0 <= ny < len(board) and board[ny][nx] == stone:
            for fx, fy in flippable_positions:
                board[fy][fx] = stone

def evaluate_board(board, stone):
    """現在のボードの評価値を計算する。
    """
    score = 0
    mobility = len(get_valid_moves(board, stone))
    opponent_mobility = len(get_valid_moves(board, 3 - stone))

    for y in range(len(board)):
        for x in range(len(board[0])):
            if board[y][x] == stone:
                score += evaluation_weights[y][x]
            elif board[y][x] == (3 - stone):
                score -= evaluation_weights[y][x]

    return score + mobility * 5 - opponent_mobility * 5

def get_valid_moves(board, stone):
    """現在のボード上で石を置ける全ての場所を返す。
    """
    moves = []
    for y in range(len(board)):
        for x in range(len(board[0])):
            if can_place_x_y(board, stone, x, y):
                moves.append((x, y))
    return moves

def minimax(board, stone, depth, maximizing_player, alpha, beta):
    """ミニマックスアルゴリズム + アルファベータ枝划り
    """
    valid_moves = get_valid_moves(board, stone)

    if depth == 0 or not valid_moves:
        return evaluate_board(board, stone), None

    if maximizing_player:
        max_eval = -float('inf')
        best_move = None
        for x, y in valid_moves:
            temp_board = [row[:] for row in board]
            make_move(temp_board, stone, x, y)
            eval, _ = minimax(temp_board, 3 - stone, depth - 1, False, alpha, beta)
            if eval > max_eval:
                max_eval = eval
                best_move = (x, y)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval, best_move
    else:
        min_eval = float('inf')
        best_move = None
        for x, y in valid_moves:
            temp_board = [row[:] for row in board]
            make_move(temp_board, stone, x, y)
            eval, _ = minimax(temp_board, 3 - stone, depth - 1, True, alpha, beta)
            if eval < min_eval:
                min_eval = eval
                best_move = (x, y)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval, best_move

class MagicAI(object):
    def face(self):
        return "🪄"

    def place(self, board, stone):
        # Dynamic depth adjustment
        empty_squares = sum(row.count(0) for row in board)
        depth = 4 if empty_squares > 12 else 6
        _, move = minimax(board, stone, depth=depth, maximizing_player=True, alpha=-float('inf'), beta=float('inf'))
        return move

from kogi_canvas import play_othello
play_othello(MagicAI())
